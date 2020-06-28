# kuzu.py
# COMP9444, CSE, UNSW

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F


class NetLin(nn.Module):
    # linear function followed by log_softmax
    """
    Linear(784) -> logSoftmax
    """

    def __init__(self):
        super(NetLin, self).__init__()
        # INSERT CODE HERE
        self.linear = nn.Linear(784, 10)

    def forward(self, x):
        # CHANGE CODE HERE
        output = self.linear(x.view(x.shape[0], -1))
        output = F.log_softmax(output, dim=1)
        return output


class NetFull(nn.Module):
    # two fully connected tanh layers followed by log softmax
    """
    Linear(784) -> (784) hidenNeuron (n) -> Tanh(n) -> (n) output (10)
    """

    def __init__(self):
        super(NetFull, self).__init__()
        # INSERT CODE HERE
        self.main = nn.Sequential(
            nn.Linear(784, 70),
            nn.Tanh(),
            nn.Linear(70, 10),
        )

    def forward(self, x):
        # CHANGE CODE HERE
        output = self.main(x.view(x.shape[0], -1))
        output = F.log_softmax(output, dim=1)
        return output


class NetConv(nn.Module):
    # two convolutional layers and one fully connected layer,
    # all using relu, followed by log_softmax
    def __init__(self):
        super(NetConv, self).__init__()
        # INSERT CODE HERE

    def forward(self, x):
        return 0  # CHANGE CODE HERE
