import torch
import torch.nn as nn
import torch.nn.functional as F

# Input: state of roster
# Output: expected return for choosing each of the 4 options

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 64)
        self.layer2 = nn.Linear(64, 128)
        self.layer3 = nn.Linear(128,64)
        self.layer4 = nn.Linear(64, n_actions)
        self.batchNorm64 = torch.nn.BatchNorm1d(64)
        self.batchNorm128 = torch.nn.BatchNorm1d(128)
    # Called with either one element to determine next action, or a batch
    # during optimization. Returns tensor([[left0exp,right0exp]...]).
    def forward(self, input):
        x = self.layer1(input)
        # x = self.batchNorm64(x)
        x = F.relu(x)

        x = self.layer2(x)
        # x = self.batchNorm128(x)
        x = F.relu(x)

        x = self.layer3(x)
        # x = self.batchNorm64(x)
        x = F.relu(x)

        output = self.layer4(x)
        return output