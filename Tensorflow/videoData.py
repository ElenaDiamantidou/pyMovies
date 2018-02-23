import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import time
from datetime import timedelta
import os, sys
# Functions and classes for loading and using the Inception model.
import inception
from inception import transfer_values_cache
# We use Pretty Tensor to define the new classifier.
import prettytensor as pt
from dataset import load_cached

#careful with pkl file -< not update

#create dataset for directory
directory = sys.argv[1]
dataset = load_cached(cache_path='my_dataset.pkl', in_dir=directory)
num_classes = dataset.num_classes
class_names = dataset.class_names
print num_classes, class_names
image_paths_train, cls_train, labels_train = dataset.get_training_set()
image_paths_test, cls_test, labels_test = dataset.get_test_set()

print("Size of:")
print("- Training-set:\t\t{}".format(len(image_paths_train)))
print("- Test-set:\t\t{}".format(len(image_paths_test)))
