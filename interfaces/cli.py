""" Интерфейс командной строки (CLI).
"""

from core.handler import handle_text

if __name__ == "__main__":
	model_dir_path: str = "../model"

	while True:
		query: str = input(str("> "))

		if query == "/exit":
			break

		print(handle_text(model_dir_path, query))
