""" Интерфейс командной строки (CLI).
"""

import os
import sys

# Исправление директории для импорта элементов ядра.
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from core.responder import Responder

if __name__ == "__main__":
	responder: Responder = Responder("model")

	print("Running Cortex CLI ...")

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(responder.get_response(query))
