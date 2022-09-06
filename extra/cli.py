""" Интерфейс командной строки (CLI).
"""

import os
import sys

from argparse import ArgumentParser, Namespace

# Исправление директории для импорта элементов ядра.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from core.responder import Responder

if __name__ == "__main__":
	arg_parser: ArgumentParser = ArgumentParser()

	arg_parser.add_argument("-md", "--model-dir", type=str, help="The path to the model directory (default: model)", default="model")

	args: Namespace = arg_parser.parse_args()

	responder: Responder = Responder(args.model_dir)

	print("Running Cortex CLI ...")

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(responder.get_response(query))
