#Taken from https://github.com/cetinsamet/age-estimation
import sys
import numpy as np
from PIL import Image

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable

from train import twoHiddenNet
from img_to_vec import Img2Vec

import os


MODEL_PATH = os.path.dirname(__file__) + "/misc/age_est_model.pt"

def get_feats(image_path):
    fe = Img2Vec(cuda=False)  # change this if you use Cuda version of the PyTorch.
    img = Image.open(image_path)
    img = img.resize((224, 224))
    feats = fe.get_vec(img).reshape(1, -1)
    return feats

def get_model():
    model = twoHiddenNet()
    model.load_state_dict(torch.load(MODEL_PATH))
    return model


def main(argv):
    global MODEL_PATH

    if len(argv) != 1:
        print("Usage: python3 age_est.py imagepath")
        exit()
    
    curdir = os.path.dirname(__file__)
    if len(curdir) == 0:
        MODEL_PATH = "misc/age_est_model.pt"

    image_path = argv[0]
    image_feats = get_feats(image_path)

    model = get_model()
    estimated_age = model(Variable(torch.from_numpy(image_feats).float()))
    print("Estimated Age : %.1f" % estimated_age.data.cpu().numpy()[0][0])
    return

if __name__ == '__main__':
    main(sys.argv[1:])