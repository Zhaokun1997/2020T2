# spiral.py
# COMP9444, CSE, UNSW

import torch
import torch.nn as nn
import matplotlib.pyplot as plt


class PolarNet(torch.nn.Module):
    """
    a fully connected neural network with one hidden layer using tanh activation,
    followed by a single output using sigmoid activation
    """

    def __init__(self, num_hid):
        super(PolarNet, self).__init__()
        self.full_connected_1 = nn.Linear(2, num_hid, bias=True)  # [2, num_hid]
        self.full_connected_2 = nn.Linear(num_hid, 1, bias=True)  # [num_hid, 1]
        self.Tanh = nn.Tanh()
        self.Sigmoid = nn.Sigmoid()

    """
    input.shape: [64, 2]
    batch_size: 64 coordinate: (x, y)
    """

    def forward(self, input):
        # step 1: convert to polar coordinates
        # 'fro' represents 2-dimension power
        r_value = torch.norm(input, p="fro", keepdim=False, dim=1)  # r_value.shape: [64]
        a_value = torch.atan2(input[:, 1], input[:, 0])  # r_value.shape: [64]
        r = r_value.unsqueeze(-1)  # r_value.shape: [64， 1]
        a = a_value.unsqueeze(-1)  # r_value.shape: [64， 1]
        x = torch.cat([r, a], -1)  # r_value.shape: [64， 2]

        # step 2: feed polar input into network
        x = self.full_connected_1(x)
        x = self.Tanh(x)
        x = self.full_connected_2(x)
        output = self.Sigmoid(x)

        return output


class RawNet(torch.nn.Module):
    """
    two fully connected hidden layers with tanh activation,
    plus the output layer, with sigmoid activation.
    The number of neurons in both hidden layers should be determined by the parameter num_hid.
    """

    def __init__(self, num_hid):
        super(RawNet, self).__init__()
        self.full_connected_1 = nn.Linear(2, num_hid, bias=True)  # [2, num_hid]
        self.full_connected_2 = nn.Linear(num_hid, num_hid, bias=True)  # [num_hid, num_hid]
        self.full_connected_3 = nn.Linear(num_hid, 1, bias=True)  # [num_hid, 1]
        self.Tanh = nn.Tanh()
        self.Sigmoid = nn.Sigmoid()

    """
    input.shape: [64, 2]
    batch_size: 64 coordinate: (x, y)
    """

    def forward(self, input):
        x = self.full_connected_1(input)
        x = self.Tanh(x)
        x = self.full_connected_2(x)
        x = self.Tanh(x)
        x = self.full_connected_3(x)
        output = self.Sigmoid(x)

        return output


class ShortNet(torch.nn.Module):
    def __init__(self, num_hid):
        super(ShortNet, self).__init__()
        self.full_connected_input_to_hid1 = nn.Linear(2, num_hid, bias=True)
        self.full_connected_input_to_hid2 = nn.Linear(2, num_hid, bias=True)
        self.full_connected_input_to_output = nn.Linear(2, 1, bias=True)
        self.full_connected_hid1_to_hid2 = nn.Linear(num_hid, num_hid, bias=True)
        self.full_connected_hid1_to_output = nn.Linear(num_hid, 1, bias=True)
        self.full_connected_hid2_to_output = nn.Linear(num_hid, 1, bias=True)
        self.Tanh = nn.Tanh()
        self.Sigmoid = nn.Sigmoid()

    def forward(self, input):
        # calculate hid1 output
        x = input
        y_hid1 = self.Tanh(self.full_connected_input_to_hid1(x))

        # calculate hid2 output
        y_hid2_a = self.full_connected_input_to_hid2(x)
        y_hid2_b = self.full_connected_hid1_to_hid2(y_hid1)
        y_hid2 = self.Tanh(y_hid2_a + y_hid2_b)

        # calculate output output
        y_output_a = self.full_connected_input_to_output(x)
        y_output_b = self.full_connected_hid1_to_output(y_hid1)
        y_output_c = self.full_connected_hid2_to_output(y_hid2)
        y_output = self.Sigmoid(y_output_a + y_output_b + y_output_c)

        return y_output


def graph_hidden(net, layer, node):
    plt.clf()
    # INSERT CODE HERE

