""" Интерфейс командной строки (CLI) для I/O процессора.
"""

from argparse import ArgumentParser, Namespace

from core.io_processor.responder import Responder

if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("-md", "--model-dir", type=str, help="The path to the model directory (default: ../model)", default="../model")

	args: Namespace = arg_parser.parse_args()

	responder: Responder = Responder(args.model_dir)

	print("Running Cortex CLI ...")

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(responder.get_response(query))
