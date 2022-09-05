""" Подготовка данных для обучения модели.
"""

import os
import sys

# Исправление директории для импорта элементов ядра.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from argparse import ArgumentParser, Namespace
from core.preprocessor import Preprocessor

if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("-ds", "--dataset-size", type=int, help="Dataset size (default: 250)", default=250)

	args: Namespace = arg_parser.parse_args()

	preprocessor: Preprocessor = Preprocessor("model", "data/data.json")

	preprocessor.preprocess_dataset(args.dataset_size)
