""" Обучение модели нейросети.
"""

from keras.layers import Dense
from keras.layers import Embedding
from keras.layers import LSTM
from keras.layers import RepeatVector
from keras.layers import TimeDistributed
from keras.models import Sequential
from keras.preprocessing.text import Tokenizer
from keras.utils import to_categorical
from keras.utils.layer_utils import print_summary
from keras_preprocessing.sequence import pad_sequences
from numpy import array, ndarray

from utils.config import Config
from utils.data import load_data_dump, create_tokenizer, get_max_length


class Trainer:
	""" Класс для обучения модели нейросети.
	"""

	def __init__(self, model_dir_path: str, model_name: str):
		""" Обучает модель нейросеть.

		:param model_dir_path: Путь к директории с моделью.
		:param model_name: Имя модели.
		"""

		self.model_dir_path = model_dir_path
		self.model_name = model_name

	@staticmethod
	def encode_sequences(tokenizer: Tokenizer, max_length: int, lines: ndarray) -> ndarray:
		""" Кодирует и заполняет последовательности.

		:param tokenizer: Токенизатор.
		:param max_length: Максимальная длина строки.
		:param lines: N-мерный массив строк.
		:return: Закодированный и заполненный N-мерный массив.
		"""

		# Кодирование последовательностей.
		x_input: list = tokenizer.texts_to_sequences(lines)

		# Заполнение последовательностей с нулевым значением.
		x_input: ndarray = pad_sequences(x_input, maxlen=max_length, padding="post")

		return x_input

	@staticmethod
	def encode_output(sequences: ndarray, vocab_size: int) -> ndarray:
		""" Кодирует целевые данные.

		:param sequences: N-мерный массив целевых данных.
		:param vocab_size: Максимальный размер запаса слов.
		:return: Закодированный N-мерный массив целевых данных.
		"""

		y_list: list = list()

		for sequence in sequences:
			encoded = to_categorical(sequence, num_classes=vocab_size)

			y_list.append(encoded)

		# Создание N-мерного массива и его решейп.
		y_output: ndarray = array(y_list).reshape((sequences.shape[0], sequences.shape[1], vocab_size))

		return y_output

	def define_model(self, vocabulary_size: int, timesteps: int, n_units: int) -> Sequential:
		""" Определяет NMT модель нейросети.

		:param vocabulary_size: Размер запаса слов.
		:param timesteps: Кол-во повторений.
		:param n_units: N-юниты.
		:return: Модель нейросети.
		"""

		model: Sequential = Sequential(name=self.model_name)

		model.add(Embedding(vocabulary_size, n_units, input_length=timesteps, mask_zero=True))
		model.add(LSTM(n_units))
		model.add(RepeatVector(timesteps))
		model.add(LSTM(n_units, return_sequences=True))
		model.add(TimeDistributed(Dense(vocabulary_size, activation="softmax")))

		return model

	def train_model(self, model: Sequential, train: tuple[ndarray, ndarray], test: tuple[ndarray, ndarray], epochs_count: int, batch_size: int) -> None:
		""" Компилирует, обучает и сохраняет модель.

		:param model: Модель.
		:param train: Кортеж из N-мерных массивов данных для обучения (train_x, train_y).
		:param test: Кортеж из N-мерных массивов данных для валидации (test_x, test_y).
		:param epochs_count: Количество эпох.
		:param batch_size: Размер партии примеров (для обновления весов).
		"""

		# Подготавливает модель к обучению.
		model.compile(optimizer="adam", loss="categorical_crossentropy")

		print_summary(model)

		# Получаение данных для обучения и данных для валидации из кортежей.
		train_x, train_y = train
		test_x, test_y = test

		# Обучение и сохранение модели.
		model.fit(train_x, train_y, epochs=epochs_count, batch_size=batch_size, validation_data=(test_x, test_y), verbose=1)
		model.save(f"{self.model_dir_path}/model.h5")

	def run_training(self, epochs_count: int, batch_size: int) -> None:
		""" Запускает обучение модели для нейросети.

		:param epochs_count: Количество эпох.
		:param batch_size: Размер партии примеров (для обновления весов).
		"""

		# Загрузка дампов данных.
		dataset: ndarray = load_data_dump(f"{self.model_dir_path}/both.pkl").reshape(-1, 1)
		train: ndarray = load_data_dump(f"{self.model_dir_path}/train.pkl")
		test: ndarray = load_data_dump(f"{self.model_dir_path}/test.pkl")

		# Подготовка токенизатора.
		tokenizer: Tokenizer = create_tokenizer(dataset[:, 0])
		vocabulary_size: int = len(tokenizer.word_index) + 1
		max_length: int = get_max_length(dataset[:, 0])

		print(f"Vocabulary Size: {vocabulary_size}")
		print(f"Max question length: {max_length}")

		# Подготовка данных для обучения.
		train_x: ndarray = self.encode_sequences(tokenizer, max_length, train[:, 0])
		train_y: ndarray = self.encode_sequences(tokenizer, max_length, train[:, 1])
		train_y: ndarray = self.encode_output(train_y, vocabulary_size)

		# Подготовка данных для валидации.
		test_x: ndarray = self.encode_sequences(tokenizer, max_length, test[:, 0])
		test_y: ndarray = self.encode_sequences(tokenizer, max_length, test[:, 1])
		test_y: ndarray = self.encode_output(test_y, vocabulary_size)

		# Определение модели.
		model: Sequential = self.define_model(vocabulary_size, max_length, 256)

		# Обучение модели.
		self.train_model(model, (train_x, train_y), (test_x, test_y), epochs_count, batch_size)


if __name__ == "__main__":
	config: Config = Config("../config.yml")
	trainer: Trainer = Trainer("../model", "Cortex-Test")

	print("Running model training ...")
	print(f" * Dataset size: {config.get_dataset_size()}")
	print(f" * Epochs count: {config.get_epochs_count()}")
	print(f" * Batch size: {config.get_batch_size()}")

	trainer.run_training(config.get_epochs_count(), config.get_batch_size())
