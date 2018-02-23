from dataset import load_cached
import sys

directory = sys.argv[1]
dataset = load_cached(cache_path='my_dataset.pkl', in_dir=directory)
num_classes = dataset.num_classes
class_names = dataset.class_names
print num_classes
print class_names
