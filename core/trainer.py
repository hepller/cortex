""" Компонент для обучения модели нейросети.
"""

from keras import losses, optimizers
from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.losses import CategoricalCrossentropy
from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import Adam
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras_preprocessing.sequence import pad_sequences
from numpy import array, ndarray

from utils.data import load_data_dump, create_tokenizer, get_max_length


class Trainer:
	""" Класс для обучения модели нейросети.
	"""

	def __init__(self, model_dir_path: str, model_name: str):
		""" Инициализирует класс для обучения нейросети.

		:param model_dir_path: Путь к директории с моделью.
		:param model_name: Имя модели.
		"""

		self.model_dir_path = model_dir_path
		self.model_name = model_name

		# Загрузка дампов данных.
		self.dataset: ndarray = load_data_dump(f"{self.model_dir_path}/both.pkl").reshape(-1, 1)
		self.train_data: ndarray = load_data_dump(f"{self.model_dir_path}/train.pkl")
		self.validation_data: ndarray = load_data_dump(f"{self.model_dir_path}/test.pkl")

		# Подготовка токенизатора и словаря.
		self.tokenizer: Tokenizer = create_tokenizer(self.dataset[:, 0])
		self.vocabulary_size: int = len(self.tokenizer.word_index) + 1
		self.max_length: int = get_max_length(self.dataset[:, 0])

		# Определение модели.
		self.model: Sequential = self.define_model(256)

		# Подготовка данных для обучения.
		self.train_x: ndarray = self.encode_sequences(self.train_data[:, 0])
		self.train_y: ndarray = self.encode_output(self.encode_sequences(self.train_data[:, 1]))

		# Подготовка данных для валидации.
		self.validate_x: ndarray = self.encode_sequences(self.validation_data[:, 0])
		self.validate_y: ndarray = self.encode_output(self.encode_sequences(self.validation_data[:, 1]))

	def encode_sequences(self, lines: ndarray) -> ndarray:
		""" Кодирует и заполняет последовательности.

		:param lines: N-мерный массив строк.
		:return: Закодированный и заполненный N-мерный массив.
		"""

		# Кодирование последовательностей.
		x_input: list = self.tokenizer.texts_to_sequences(lines)

		# Заполнение последовательностей с нулевым значением.
		x_input: ndarray = pad_sequences(x_input, maxlen=self.max_length, padding="post")

		return x_input

	def encode_output(self, sequences: ndarray) -> ndarray:
		""" Кодирует целевые данные.

		:param sequences: N-мерный массив целевых данных.
		:return: Закодированный N-мерный массив целевых данных.
		"""

		y_list: list = list()

		for sequence in sequences:
			encoded = to_categorical(sequence, num_classes=self.vocabulary_size)

			y_list.append(encoded)

		# Создание N-мерного массива и его решейп.
		y_output: ndarray = array(y_list).reshape((sequences.shape[0], sequences.shape[1], self.vocabulary_size))

		return y_output

	def define_model(self, n_units: int) -> Sequential:
		""" Определяет NMT модель нейросети.

		:param n_units: N-юниты.
		:return: Модель нейросети.
		"""

		model: Sequential = Sequential(name=self.model_name)

		model.add(Embedding(self.vocabulary_size, n_units, input_length=self.max_length, mask_zero=True))
		model.add(LSTM(n_units))
		model.add(RepeatVector(self.max_length))
		model.add(LSTM(n_units, return_sequences=True))
		model.add(TimeDistributed(Dense(self.vocabulary_size, activation="softmax")))

		return model

	def train_model(self, epochs_count: int = 1000, batch_size: int = 64, optimizer: optimizers = Adam(), loss_function: losses = CategoricalCrossentropy(), overtrain: bool = False) -> None:
		""" Запускает обучение модели для нейросети.

		:param epochs_count: Количество эпох (по умолчанию: 1000).
		:param batch_size: Размер партии примеров для обновления весов (по умолчанию: 64).
		:param optimizer: Оптимизатор (Keras).
		:param loss_function: Функция потерь (Keras).
		:param overtrain: Будет ли дообучена существующая модель, вместо обучения новой.
		"""

		# Загрузка существующей модели (при включенном дообучении).
		if overtrain:
			self.model: Sequential = load_model(f"{self.model_dir_path}/model.h5")

		# Подготавливает модель к обучению.
		self.model.compile(optimizer=optimizer, loss=loss_function)

		# print_summary(self.model)

		print(f"Running \"{self.model.name}\" model training (overtrain: {overtrain}) ...")
		print(f" * Epochs count: {epochs_count}")
		print(f" * Batch size: {batch_size}")
		print(f" * Vocabulary Size: {self.vocabulary_size}")
		print(f" * Max question length: {self.max_length}")
		print("")

		# Обучение модели.
		self.model.fit(self.train_x, self.train_y, epochs=epochs_count, batch_size=batch_size, validation_data=(self.validate_x, self.validate_y), verbose=1)
		self.model.save(f"{self.model_dir_path}/model.h5")
