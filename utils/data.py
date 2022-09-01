""" Вспомогательные функции.
"""

from pickle import dump, load

from keras_preprocessing.text import Tokenizer
from numpy import ndarray


def save_data_dump(data: ndarray, filename: str) -> None:
	""" Сохраняет данные в pkl-файл (дамп).

	:param data: Данные для сохранения (в виде N-мерного массива).
	:param filename: Имя файла.
	"""

	dump(data, open(filename, "wb"))

	print("Saved: %s" % filename)


def load_data_dump(filename: str) -> ndarray:
	""" Загружает данные из pkl-файла (дампа).

	:param filename: Имя pkl-файла
	:return: Данные из дампа (в виде N-мерного массива).
	"""

	return load(open(filename, "rb"))


def create_tokenizer(lines: ndarray, char_level: bool = False) -> Tokenizer:
	""" Создает токенизатор на основе текста.

	:param lines: Строки текст для создания словаря.
	:param char_level: Уровень символов (если значение True, то каждый символ будет рассматриваться как токен).
	:return: Токенизатор со словарем из указанного текста.
	"""

	tokenizer: Tokenizer = Tokenizer(char_level=char_level)
	tokenizer.fit_on_texts(lines)

	return tokenizer


def get_max_length(lines: ndarray) -> int:
	""" Получает максимальную длину строки среди линий текста.

	:param lines: Список текста.
	:return: Максимальная длина строки.
	"""

	return max(len(line.split()) for line in lines)
