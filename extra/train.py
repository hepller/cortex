""" Обучение модели нейросети.
"""

import os
import sys
from argparse import ArgumentParser, Namespace

# Исправление директории для импорта элементов ядра.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from core.trainer import Trainer

if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("-ec", "--epochs-count", type=int, help="Number of epochs (default: 200)", default=200)
	arg_parser.add_argument("-bs", "--batch-size", type=int, help="Batch size (default: 50)", default=50)
	arg_parser.add_argument("-o", "--overtrain", type=bool, help="Further training of the existing model (default: False)", default=False)

	args: Namespace = arg_parser.parse_args()

	trainer: Trainer = Trainer("model", "cortex-test")

	# overtrain: bool = os.path.exists("model/model.h5")

	trainer.train_model(epochs_count=args.epochs_count, batch_size=args.batch_size, overtrain=args.overtrain)
