""" Вспомогательные функции.
"""

from pickle import load

from keras_preprocessing.text import Tokenizer
from numpy import ndarray


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
