import math
import random
from collections import namedtuple
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.optim as optim
from ReplayMemory import ReplayMemory
from envr import envr
from DQN import DQN
from HelperMethods import *

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
steps_done = 0
Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward') )
memory = ReplayMemory(10000)

policy_net = DQN(8, 4).to(device)
target_net = DQN(8, 4).to(device)
target_net.load_state_dict(policy_net.state_dict())

env = envr()

EPS_START = 0.99         # starting value of epsilon
EPS_END = 0.05          # final value of epsilon
EPS_DECAY = 5000        # rate of decay, higher = slower

BATCH_SIZE = 128        # number of transitions sampled from the replay buffer
LR = 1e-4               # learning rate of the AdamW optimizer
GAMMA = 0.99            # discount factor
TAU = 0.005             # update rate of the target network

def select_action(state):
    global env
    global device
    global policy_net
    global EPS_START
    global EPS_END
    global EPS_DECAY
    global steps_done
    # as we train our model, the probability of using our policy net to make decisions increases

    sample = random.random()
    eps_threshold = EPS_END + (EPS_START - EPS_END) * \
        math.exp(-1. * steps_done / EPS_DECAY)
    steps_done += 1
    if sample > eps_threshold:
        with torch.no_grad():
            # picks action with the largest expected reward
            return policy_net(state).max(1)[1].view(1, 1)
    else:
        return torch.tensor([[env.sample()]], device=device, dtype=torch.long)

def optimize_model():
    global Transition
    global memory
    global policy_net
    global target_net
    global BATCH_SIZE
    global LR
    global GAMMA
    optimizer = optim.AdamW(policy_net.parameters(), lr=LR, amsgrad=True)
    if len(memory) < BATCH_SIZE:
        return
    print("1")
    transitions = memory.sample(BATCH_SIZE)
    # Transpose the batch (see https://stackoverflow.com/a/19343/3343043 for
    # detailed explanation). This converts batch-array of Transitions
    # to Transition of batch-arrays.
    batch = Transition(*zip(*transitions))
    # Compute a mask of non-final states and concatenate the batch elements
    # (a final state would've been the one after which simulation ended)
    non_final_mask = torch.tensor(tuple(map(lambda s: s is not None,
                                          batch.next_state)), device=device, dtype=torch.bool)
    non_final_next_states = torch.cat([s for s in batch.next_state
                                                if s is not None])
    state_batch = torch.cat(batch.state)
    action_batch = torch.cat(batch.action)
    reward_batch = torch.cat(batch.reward)
    # Compute Q(s_t, a) - the model computes Q(s_t), then we select the
    # columns of actions taken. These are the actions which would've been taken
    # for each batch state according to policy_net
    state_action_values = policy_net(state_batch).gather(1, action_batch)
    # Compute V(s_{t+1}) for all next states.
    # Expected values of actions for non_final_next_states are computed based
    # on the "older" target_net; selecting their best reward with max(1)[0].
    # This is merged based on the mask, such that we'll have either the expected
    # state value or 0 in case the state was final.
    next_state_values = torch.zeros(BATCH_SIZE, device=device)
    with torch.no_grad():
        next_state_values[non_final_mask] = target_net(non_final_next_states).max(1)[0]
    # Compute the expected Q values
    expected_state_action_values = (next_state_values * GAMMA) + reward_batch
    # Compute Huber loss
    criterion = nn.SmoothL1Loss()
    loss = criterion(state_action_values, expected_state_action_values.unsqueeze(1))
    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    # In-place gradient clipping
    torch.nn.utils.clip_grad_value_(policy_net.parameters(), 100)
    optimizer.step()

def main():
    # if gpu is to be used
    global device, steps_done, TAU

    adp = new_adp()
    replacements = replacement_adp(adp)
    num_drafts = 50
    team_ratings = []

    for i_draft in range(num_drafts):
        draft_slot = random.randint(1, 10)
        print("draft slot = " + str(draft_slot))
        is_cpu = [True, True, True, True, True, True, True, True, True, True]
        is_cpu[draft_slot - 1] = False

        state = env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        for round in range(1,17):
            for cpu in is_cpu:
                if cpu:
                    print("cpu")
                    state = env.cpu_draft()
                else:
                    print("player")
                    action = select_action(state)
                    next_state_temp, reward = env.step(action.item())
                    reward = torch.tensor([reward], device=device)
                    if round == 16:
                        next_state = None
                    else:
                        next_state = torch.tensor(next_state_temp, dtype=torch.float32, device=device).unsqueeze(0)
                    # Store the transition in memory
                    memory.push(state, action, next_state, reward)
                    # Move to the next state
                    state = next_state
                    # Perform one step of the optimization (on the policy network)
                    optimize_model()
                    # Soft update of the target network's weights
                    # θ′ ← τ θ + (1 −τ )θ′
                    target_net_state_dict = target_net.state_dict()
                    policy_net_state_dict = policy_net.state_dict()
                    for key in policy_net_state_dict:
                        target_net_state_dict[key] = policy_net_state_dict[key] * TAU + target_net_state_dict[key] * (1 - TAU)
                    target_net.load_state_dict(target_net_state_dict)

        ai_team = env.get_team()
        power = team_strength(ai_team,replacements)
        team_ratings.append(power)
    #plt.scatter(x=range(1,len(team_ratings) + 1), y=team_ratings)
    #plt.show()

main()


print('Complete')