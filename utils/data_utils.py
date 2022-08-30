""" Утилита для работы с данными.
"""

from pickle import load


def load_data_dump(filename: str) -> any:
	""" Загружает данные из pkl-файлов (дампа).

	:param filename: Имя файла.
	:return: Данные из дампа.
	"""

	return load(open(filename, "rb"))
