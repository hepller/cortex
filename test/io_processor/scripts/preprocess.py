""" Подготовка данных для обучения модели для I/O процессора.
"""

from argparse import ArgumentParser, Namespace

from core.io_processor.preprocessor import Preprocessor

if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("-ds", "--dataset-size", type=int, help="Dataset size (default: 256)", default=256)
	arg_parser.add_argument("-md", "--model-dir", type=str, help="The path to the model directory (default: ../model)", default="../model")
	arg_parser.add_argument("-df", "--dataset-filename", type=str, help="The path to the dataset (default: ../data/data.json)", default="../data/data.json")

	args: Namespace = arg_parser.parse_args()

	preprocessor: Preprocessor = Preprocessor(args.model_dir, args.dataset_filename)

	preprocessor.preprocess_dataset(args.dataset_size)
