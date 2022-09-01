""" Обработка входящих данных и получения ответа.
"""

from keras import Sequential
from keras.saving.save import load_model
from keras.utils import pad_sequences
from keras_preprocessing.text import Tokenizer
from numpy import ndarray, argmax

from utils.data import load_data_dump, get_max_length, create_tokenizer


class Cortex:
	""" Класс для обработки запросов и получения ответа.
	"""

	def __init__(self, model_dir_path: str) -> None:
		""" Инициализирует нейросеть.

		:param model_dir_path: Путь к директории с моделью.
		"""

		self.model_dir_path: str = model_dir_path

		self.model: Sequential = load_model(f"{model_dir_path}/model.h5")
		self.dataset: ndarray = load_data_dump(f"{model_dir_path}/both.pkl").reshape(-1, 1)
		self.tokenizer: Tokenizer = create_tokenizer(self.dataset[:, 0])
		self.max_length: int = get_max_length(self.dataset[:, 0])

	def word_for_id(self, integer: int) -> str | None:
		""" Сопоставляет целое число со словом и возвращает слово из последовательности.

		:param integer: Целое число.
		:return: Слово из последовательности слов.
		"""

		for word, index in self.tokenizer.word_index.items():
			if index == integer:
				return word

		return None

	def predict_sequence(self, source: ndarray) -> str:
		""" Генерирует целевую последовательность слов исходя из исходных данных.

		:param source: Исходные данные в виде N-мерного массива.
		:return: Целевая последовательность слов в виде строки.
		"""

		prediction: ndarray = self.model.predict(source, verbose=0)[0]
		integers: list = [argmax(vector) for vector in prediction]
		target: list = list()

		for item in integers:
			word = self.word_for_id(item)

			if word is None:
				break

			target.append(word)

		return " ".join(target)

	def get_output(self, sources: ndarray) -> str:
		""" Получает ответ на запрос.

		:param sources: N-мерный массив данных.
		"""

		predicted: list = list()
		y_output: str = ""

		# Перебор, перевод закодированного исходного текста и обновление значения переменной ответа.
		for item, source in enumerate(sources):
			source: ndarray = source.reshape((1, source.shape[0]))
			y_output: str = self.predict_sequence(source)

			predicted.append(y_output.split())

		return y_output

	def handle_text(self, text: str) -> str:
		""" Возвращает ответ на входящий текст.

		:param text: Входящий текст.
		:return: Ответ на входящий текст.
		"""

		# Обрезка входящего текста.
		query: list[str] = text.strip().split("\n")

		# Токенизация входящих данных.
		x_input: list[str] = self.tokenizer.texts_to_sequences(query)
		x_input: ndarray = pad_sequences(x_input, maxlen=self.max_length, padding="post")

		return self.get_output(x_input)
