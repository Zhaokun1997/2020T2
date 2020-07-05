# kuzu.py
# COMP9444, CSE, UNSW

from __future__ import print_function
import torch
import torch.nn as nn
import torch.nn.functional as F

# hyper-parameters
channel = 1
Height = 28
Width = 28


class NetLin(nn.Module):
    # linear function followed by log_softmax
    """
    Linear(784) -> logSoftmax
    """

    def __init__(self):
        super(NetLin, self).__init__()

        # define each layer
        # if bias set to false, the layer will not learn an additive bias
        self.linear = nn.Linear(channel * Height * Width, 10, bias=True)
        self.log_softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        # deploy each layer using functions
        # x.shape = [64, 1, 28, 28]
        # batch_size(64) x picture_channel(1) x Herght(28) x Width(28)
        # x: [64, 1, 28, 28]
        x_0 = x.view(x.shape[0], -1)  # x_0: [64, 784]
        x_1 = self.linear(x_0)  # x_1: [64, 10]
        output = self.log_softmax(x_1)

        return output


class NetFull(nn.Module):
    # two fully connected tanh layers followed by log softmax
    """
    Linear(784) -> (784) hidenNeuron (n) -> Tanh(n) -> (n) output (10)
    """

    def __init__(self):
        super(NetFull, self).__init__()

        # hyper-parameters
        num_hid = 80
        # define each layer
        # if bias set to false, the layer will not learn an additive bias
        self.full_connected_1 = nn.Linear(channel * Height * Width, num_hid, bias=True)  # [784, num_hid]
        self.full_connected_2 = nn.Linear(num_hid, 10, bias=True)  # [num_hid, 10]
        self.Tanh = nn.Tanh()
        self.log_softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x_0 = x.view(x.shape[0], -1)  # x_0: [64, 784]
        x_1 = self.full_connected_1(x_0)  # x_1: [64, num_hid]
        x_2 = self.Tanh(x_1)  # x_2: [64, num_hid]
        x_3 = self.full_connected_2(x_2)  # x_3: [num_hid, 10]
        output = self.log_softmax(x_3)
        return output


class NetConv(nn.Module):
    # two convolutional layers and one fully connected layer,
    # all using relu, followed by log_softmax
    def __init__(self):
        super(NetConv, self).__init__()
        """
        :parameter in_channels: the # of channels of input image 
        :parameter out_channels: the # kinds of filters in conv layer
        :parameter _channels: the height/width of every filter
        """
        # initially: 1 channel, 16 filters, 3x3 filter size
        num_hid = 90
        self.conv2d_1 = nn.Conv2d(in_channels=1, out_channels=24, kernel_size=4, stride=1, padding=0, bias=True, padding_mode='zeros')
        self.conv2d_2 = nn.Conv2d(in_channels=24, out_channels=36, kernel_size=3, stride=1, padding=0, bias=True, padding_mode='zeros')
        self.max_pool2d = nn.MaxPool2d(kernel_size=2)
        self.full_connected_1 = nn.Linear(900, num_hid, bias=True)
        self.full_connected_2 = nn.Linear(num_hid, 10, bias=True)
        self.ReLU = nn.ReLU(inplace=False)
        self.log_softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x = self.conv2d_1(x)
        x = self.ReLU(x)
        x = self.max_pool2d(x)
        x = self.conv2d_2(x)
        x = self.ReLU(x)  # somevalues * somevalues * 32
        x = self.max_pool2d(x)
        hiden_input_x = x.view(x.shape[0], -1)
        x = self.full_connected_1(hiden_input_x)
        x = self.ReLU(x)
        x = self.full_connected_2(x)
        output = self.log_softmax(x)
        return output
