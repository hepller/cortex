import json
from pickle import dump

import numpy
from numpy.random import shuffle

from utils import config_utils

config = config_utils.get_config("../config.yml")

# save a list of clean sentences to file
def save_clean_data(sentences, filename):
  dump(sentences, open(filename, "wb"))
  print("Saved: %s" % filename)

# Загрузка датасета
with open("../data.json", "rb") as json_file:
  data = []
  json_data = json.load(json_file)

  for json_item in json_data:
    data.append([json_item["question"], json_item["answer"]])

  data = numpy.array(data)

# reduce dataset size
dataset_size = config["dataset_size"] # 29
n_sentences = dataset_size
dataset = data[:n_sentences, :]

# random shuffle
shuffle(dataset)

# split into train/test
train, test = dataset[:dataset_size], dataset[dataset_size:]

# save
save_clean_data(dataset, "../model/both.pkl")
save_clean_data(train, "../model/train.pkl")
save_clean_data(test, "../model/test.pkl")
