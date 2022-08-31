""" Обработка входящих данных и получения ответа
"""

from keras import Sequential
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from numpy import argmax, ndarray
from numpy.compat import long

from core.train import load_data_dump, create_tokenizer, max_length

# Загрузка модели (весов).
# TODO: Перепис.
model: Sequential = load_model("../model/model.h5")


def word_for_id(integer: long, tokenizer: Tokenizer) -> str | None:
	""" Сопоставляет целое число со словом и возвращает слово из последовательности.

	:param integer: Целое число.
	:param tokenizer: Токенизатор.
	:return: Слово из последовательности слов.
	"""

	for word, index in tokenizer.word_index.items():
		if index == integer:
			return word

	return None


def predict_sequence(model: Sequential, tokenizer: Tokenizer, source: ndarray) -> str:
	""" Генерирует целевую последовательность слов исходя из исходных данных.

	:param model: Модель нейросети.
	:param tokenizer: Токенизатор.
	:param source: Исходные данные в виде N-мерного массива.
	:return: Целевая последовательность слов в виде строки.
	"""

	# prediction: ndarray = model.predict(source, verbose=0)[0] # Старый вариант
	# prediction: ndarray = model(source)[0].numpy()
	prediction: ndarray = model.predict(source, verbose=0)[0]
	integers: list = [argmax(vector) for vector in prediction]
	target: list = list()

	for item in integers:
		word = word_for_id(item, tokenizer)

		if word is None:
			break

		target.append(word)

	return " ".join(target)


def get_output(tokenizer: Tokenizer, model: Sequential, sources: ndarray) -> str:
	""" Получает ответ на запрос.

	:param tokenizer: Токенизатор.
	:param model: Модель нейросети.
	:param sources: N-мерный массив данных.
	"""

	predicted: list = list()
	y_output: str = ""

	# Перебор, перевод закодированного исходного текста и обновление значения переменной ответа.
	for item, source in enumerate(sources):
		source: ndarray = source.reshape((1, source.shape[0]))
		y_output: str = predict_sequence(model, tokenizer, source)

		predicted.append(y_output.split())

	return y_output


def handle_text(model_dir_path: str, text: str) -> str:
	""" Возвращает ответ на входящий текст.

	:param model_dir_path: Путь к директории модели.
	:param text: Входящий текст.
	:return: Ответ на входящий текст.
	"""

	# Загрузка дампа датасета и его решейп.
	dataset = load_data_dump(f"{model_dir_path}/both.pkl")
	reshaped_dataset = dataset.reshape(-1, 1)

	# Подготовка токенизатора.
	tokenizer: Tokenizer = create_tokenizer(reshaped_dataset[:, 0])
	# vocabulary_size: int = len(tokenizer.word_index) + 1
	length: int = max_length(reshaped_dataset[:, 0])

	# # Загрузка модели (весов).
	# model: Sequential = load_model(f"{model_dir_path}/model.h5")

	# Обрезка входящего текста.
	query: list[str] = text.strip().split("\n")

	# Токенизация входящих данных.
	x_input: list[str] = tokenizer.texts_to_sequences(query)
	x_input: ndarray = pad_sequences(x_input, maxlen=length, padding="post")

	return get_output(tokenizer, model, x_input)
