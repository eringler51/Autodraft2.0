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

policy_net = DQN(12, 4).to(device)
target_net = DQN(12, 4).to(device)
target_net.load_state_dict(policy_net.state_dict())

env = envr()

num_drafts = 1000

EPS_START = 0.99         # starting value of epsilon
EPS_END = 0.05          # final value of epsilon
EPS_DECAY = 100        # rate of decay, higher = slower

BATCH_SIZE = 128        # number of transitions sampled from the replay buffer
LR = 1e-5               # learning rate of the AdamW optimizer
GAMMA = 0.99            # discount factor
TAU = 0.005             # update rate of the target network

def random_action():
    return torch.tensor([[env.sample()]], device=device, dtype=torch.long)

def select_action(state):
    global policy_net
    #print("Used Policy Net")
    a = policy_net(state)
    b = a.max(1)[1]
    c = b.view(1, 1)
    return c
    # return policy_net(state).max(1)[1].view(1, 1)

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
    #print("Optimizing")
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
    global device, steps_done, TAU, num_drafts

    adp = new_adp()
    replacements = replacement_adp(adp)
    team_ratings = []

    best_rating = -1000
    best_team = 0
    worst_rating = 1000
    worst_team = 0

    for i_draft in range(num_drafts):
        print(str(i_draft))
        draft_slot = random.randint(1, 10)
        #print("draft slot = " + str(draft_slot))
        is_cpu = [True, True, True, True, True, True, True, True, True, True]
        is_cpu[draft_slot - 1] = False

        eps_threshold = EPS_END + (EPS_START - EPS_END) * \
                        math.exp(-1. * steps_done / EPS_DECAY)
        steps_done += 1
        #print("eps threshold = " + str(eps_threshold))
        sample = random.random()
        #print("sample = " + str(sample))

        state = env.reset()
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
        for round in range(1,17):
            for cpu in is_cpu:
                if cpu:
                    #print("cpu")
                    state = env.cpu_draft()
                    state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)
                else:
                    #print("player")
                    if sample > eps_threshold:
                        #print("Policy Net")
                        action = select_action(state)
                    else:
                        #print("Random Action")
                        action = random_action()
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
        #if sample > eps_threshold:
        team_ratings.append(power)

        final_team = env.get_team()
        #print("final_team: " + str(final_team))
        final_power = env.get_power()
        print("final_power: " + str(final_power))
        #team_ratings.append(final_power)

        if final_power > best_rating:
            best_team = final_team
            best_rating = final_power
        if final_power < worst_rating:
            worst_team = final_team
            worst_rating = final_power

    plt.scatter(x=range(1,len(team_ratings) + 1), y=team_ratings)
    plt.xlabel("draft number")
    plt.ylabel("power rating")
    plt.show()

    print("best team")
    print(best_team)
    print("worst team")
    print(worst_team)

main()

print('Complete')