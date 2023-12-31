import os
import json
import random
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)
import imgaug
import torch
import torch.multiprocessing as mp
import numpy as np
import models
seed = 1234
random.seed(seed)
imgaug.seed(seed)
torch.manual_seed(seed)
torch.cuda.manual_seed_all(seed)
np.random.seed(seed)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False


import torch
import torch.nn as nn
from .segmentation import segmentation
from .utils import load_state_dict_from_url
from collections import OrderedDict


try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    from torch.utils.model_zoo import load_url as load_state_dict_from_url



__all__ = [
    "VGG_mask",
    "vgg19_bn_mask_pretrain",
]

new_dict = ['conv1.weight','conv1.bias',
            'bn1.weight','bn1.bias','bn1.running_mean','bn1.running_var',
            'conv2.weight','conv2.bias',
            'bn2.weight','bn2.bias','bn2.running_mean','bn2.running_var',
            'conv3.weight','conv3.bias',
            'bn3.weight','bn3.bias','bn3.running_mean','bn3.running_var',
            'conv4.weight','conv4.bias',
            'bn4.weight','bn4.bias','bn4.running_mean','bn4.running_var',
            'conv5.weight','conv5.bias',
            'bn5.weight','bn5.bias','bn5.running_mean','bn5.running_var',
            'conv6.weight','conv6.bias',
            'bn6.weight','bn6.bias','bn6.running_mean','bn6.running_var',
            'conv7.weight','conv7.bias',
            'bn7.weight','bn7.bias','bn7.running_mean','bn7.running_var',
            'conv8.weight','conv8.bias',
            'bn8.weight','bn8.bias','bn8.running_mean','bn8.running_var',
            'conv9.weight','conv9.bias',
            'bn9.weight','bn9.bias','bn9.running_mean','bn9.running_var',
            'conv10.weight','conv10.bias',
            'bn10.weight','bn10.bias','bn10.running_mean','bn10.running_var',
            'conv11.weight','conv11.bias',
            'bn11.weight','bn11.bias','bn11.running_mean','bn11.running_var',
            'conv12.weight','conv12.bias',
            'bn12.weight','bn12.bias','bn12.running_mean','bn12.running_var',
            'conv13.weight','conv13.bias',
            'bn13.weight','bn13.bias','bn13.running_mean','bn13.running_var',
            'conv14.weight','conv14.bias',
            'bn14.weight','bn14.bias','bn14.running_mean','bn14.running_var',
            'conv15.weight','conv15.bias',
            'bn15.weight','bn15.bias','bn15.running_mean','bn15.running_var',
            'conv16.weight','conv16.bias',
            'bn16.weight','bn16.bias','bn16.running_mean','bn16.running_var'
            ]

model_urls = {
    "vgg19_bn": "https://download.pytorch.org/models/vgg19_bn-c79401a0.pth",
}


class Trainer(object):
    """base class for trainers"""

    def __init__(self):
        pass    



class VGG_mask(nn.Module):
    def __init__(self, in_channels=3, num_classes=1000,init_weights=True):
        super(VGG_mask, self).__init__()
      
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=3, padding=1)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu1 = nn.ReLU(inplace=True)
        self.conv2 = nn.Conv2d(64, 64, kernel_size=3, padding=1)   
        self.bn2 = nn.BatchNorm2d(64)
        self.relu2 = nn.ReLU(inplace=True)
        self.maxp1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.relu3 = nn.ReLU(inplace=True)
        self.conv4 = nn.Conv2d(128, 128, kernel_size=3, padding=1)
        self.bn4 = nn.BatchNorm2d(128)
        self.relu4 = nn.ReLU(inplace=True)
        self.maxp2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv5 = nn.Conv2d(128, 256, kernel_size=3, padding=1)
        self.bn5 = nn.BatchNorm2d(256)
        self.relu5 = nn.ReLU(inplace=True)
        self.conv6 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.bn6 = nn.BatchNorm2d(256)
        self.relu6 = nn.ReLU(inplace=True)
        self.conv7 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.bn7 = nn.BatchNorm2d(256)
        self.relu7= nn.ReLU(inplace=True)
        self.conv8 = nn.Conv2d(256, 256, kernel_size=3, padding=1)
        self.bn8 = nn.BatchNorm2d(256)
        self.relu8 = nn.ReLU(inplace=True)
        self.maxp3 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv9 = nn.Conv2d(256, 512, kernel_size=3, padding=1)
        self.bn9 = nn.BatchNorm2d(512)
        self.relu9 = nn.ReLU(inplace=True)
        self.conv10 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn10 = nn.BatchNorm2d(512)
        self.relu10 = nn.ReLU(inplace=True)
        self.conv11 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn11 = nn.BatchNorm2d(512)
        self.relu11 = nn.ReLU(inplace=True)
        self.conv12 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn12 = nn.BatchNorm2d(512)
        self.relu12 = nn.ReLU(inplace=True)
        self.maxp4 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv13 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn13 = nn.BatchNorm2d(512)
        self.relu13 = nn.ReLU(inplace=True)
        self.conv14 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn14 = nn.BatchNorm2d(512)
        self.relu14 = nn.ReLU(inplace=True)
        self.conv15 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn15 = nn.BatchNorm2d(512)
        self.relu15 = nn.ReLU(inplace=True)
        self.conv16 = nn.Conv2d(512, 512, kernel_size=3, padding=1)
        self.bn16 = nn.BatchNorm2d(512)
        self.relu16 = nn.ReLU(inplace=True)
        self.maxp5 = nn.MaxPool2d(kernel_size=2, stride=2)
    

        self.avgpool = nn.AdaptiveAvgPool2d((7, 7))
        self.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 1000),
        )
        state_dict = load_state_dict_from_url("https://download.pytorch.org/models/vgg19_bn-c79401a0.pth", progress=True)
        tuple_list = list(state_dict.items()) 
        for i in range(len(new_dict)):
            state_dict = OrderedDict([(new_dict[i], v) if k == tuple_list[i][0] else (k, v) for k, v in state_dict.items()])
        self.load_state_dict(state_dict)

        self.seg1 = segmentation(64, 64, depth=1)
        self.seg2 = segmentation(128, 128, depth=1)
        self.seg3 = segmentation(256, 256, depth=1)
        self.seg4 = segmentation(512, 512, depth=1)
        

    def forward(self, x):

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu1(x)        
        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu2(x)
        m = self.seg1(x)
        x = x * (1 + m)
        x = self.maxp1(x)
        x = self.conv3(x)
        x = self.bn3(x)
        x = self.relu3(x)
        x = self.conv4(x)
        x = self.bn4(x)
        x = self.relu4(x)
        m = self.seg2(x)
        x = x * (1 + m)
        x = self.maxp2(x)
        x = self.conv5(x)
        x = self.bn5(x)
        x = self.relu5(x)
        x = self.conv6(x)
        x = self.bn6(x)
        x = self.relu6(x)        
        x = self.conv7(x)
        x = self.bn7(x)
        x = self.relu7(x)
        x = self.conv8(x)
        x = self.bn8(x)
        x = self.relu8(x)
        m = self.seg3(x)
        x = x * (1 + m)
        x = self.maxp3(x)
        x = self.conv9(x)
        x = self.bn9(x)
        x = self.relu9(x)
        x = self.conv10(x)
        x = self.bn10(x)
        x = self.relu10(x)        
        x = self.conv11(x)
        x = self.bn11(x)
        x = self.relu11(x)
        x = self.conv12(x)
        x = self.bn12(x)
        x = self.relu12(x)
        x = self.maxp4(x)
        x = self.conv13(x)
        x = self.bn13(x)
        x = self.relu13(x)
        x = self.conv14(x)
        x = self.bn14(x)
        x = self.relu14(x)        
        x = self.conv15(x)
        x = self.bn15(x)
        x = self.relu15(x)
        x = self.conv16(x)
        x = self.bn16(x)
        x = self.relu16(x)
        m = self.seg4(x)
        x = x * (1 + m)
        x = self.maxp5(x)

  
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.classifier(x)
        return x


def vgg19_bn_mask_pretrain(in_channels=3, num_classes = 1000, progress=True, **kwargs):  

    model = VGG_mask(in_channels, num_classes, progress, **kwargs)      
    model.classifier = nn.Sequential(
        nn.Linear(512 * 7 * 7, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, 4096),
        nn.ReLU(True),
        nn.Dropout(),
        nn.Linear(4096, 7),
    )
    print(model)
    return model



def _vgg(arch, block, layers, pretrained, progress, **kwargs):
    model = VGG_mask(block, layers, **kwargs)
    if pretrained:
         state_dict = load_state_dict_from_url(model_urls[arch],
                                              progress=progress) 
        model.load_state_dict(state_dict) 
    return model


def get_model(configs):
    try:
        return models.__dict__[configs["arch"]]
    except KeyError:
        return segmentation.__dict__[configs["arch"]]

def get_dataset(configs):
    from utils.datasets.fer2013dataset import fer2013
    train_set = fer2013("train", configs)
    val_set = fer2013("val", configs)
    test_set = fer2013("test", configs, tta=True, tta_size=10)
    return train_set, val_set, test_set




