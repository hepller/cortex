""" Обучение модели нейросети.
"""

from argparse import ArgumentParser, Namespace

from core.trainer import Trainer

if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("-ec", "--epochs-count", type=int, help="Number of epochs (default: 200)", default=200)
	arg_parser.add_argument("-bs", "--batch-size", type=int, help="Batch size (default: 64)", default=64)
	arg_parser.add_argument("-o", "--overtrain", type=bool, help="Further training of the existing model (default: false)", default=False)
	arg_parser.add_argument("-md", "--model-dir", type=str, help="The path to the model directory (default: ../model)", default="../model")
	arg_parser.add_argument("-mn", "--model-name", type=str, help="Name of the neural network model (default: cortex-test)", default="cortex-test")

	args: Namespace = arg_parser.parse_args()

	trainer: Trainer = Trainer(args.model_dir, args.model_name)

	# overtrain: bool = os.path.exists("../model/model.h5")

	trainer.train_model(epochs_count=args.epochs_count, batch_size=args.batch_size, overtrain=args.overtrain)
