""" Обучение модели для нейросети.
"""

from pickle import load

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


def load_data_dump(filename: str) -> ndarray:
	""" Загружает данные из pkl-файла (дампа).

	:param filename: Имя pkl-файла
	:return: Данные из дампа.
	"""

	return load(open(filename, "rb"))


def create_tokenizer(lines: ndarray) -> Tokenizer:
	""" Создает токенизатор на основе текста.

	:param lines: Строки текст для создания словаря.
	:return: Токенизатор со словарем из указанного текста.
	"""

	tokenizer: Tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)

	return tokenizer


def max_length(lines: ndarray) -> int:
	""" Получает максимальную длину строки среди линий текста.

	:param lines: Список текста.
	:return: Максимальная длина строки.
	"""

	return max(len(line.split()) for line in lines)


def encode_sequences(tokenizer: Tokenizer, length: int, lines: ndarray) -> ndarray:
	""" Кодирует и заполняет последовательности.

	:param tokenizer: Токенизатор.
	:param length: Максимальная длина строки.
	:param lines: N-мерный массив строк.
	:return: Закодированный и заполненный N-мерный массив.
	"""

	# Кодирование последовательностей.
	x: list = tokenizer.texts_to_sequences(lines)

	# Заполнение последовательностей с нулевым значением.
	x: ndarray = pad_sequences(x, maxlen=length, padding="post")

	return x


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
	y: ndarray = array(y_list).reshape((sequences.shape[0], sequences.shape[1], vocab_size))

	return y


def define_model(name: str, vocab: int, timesteps: int, n_units: int) -> Sequential:
	""" Определяет NMT модель нейросети.

	:param name: Имя модели.
	:param vocab: Размер запаса слов.
	:param timesteps: Кол-во повторений.
	:param n_units: N-юниты.
	:return: Модель нейросети.
	"""

	model: Sequential = Sequential(name=name)

	model.add(Embedding(vocab, n_units, input_length=timesteps, mask_zero=True))
	model.add(LSTM(n_units))
	model.add(RepeatVector(timesteps))
	model.add(LSTM(n_units, return_sequences=True))
	model.add(TimeDistributed(Dense(vocab, activation="softmax")))

	return model


def train_model(model: Sequential, train: tuple[ndarray, ndarray], test: tuple[ndarray, ndarray], epochs_count: int, batch_size: int, model_path: str) -> None:
	""" Компилирует, обучает и сохраняет модель.

	:param model: Модель.
	:param train: Кортеж из N-мерных массивов данных для обучения (train_x, train_y).
	:param test: Кортеж из N-мерных массивов данных для валидации (test_x, test_y).
	:param epochs_count: Количество эпох.
	:param batch_size: Размер партии примеров (для обновления весов).
	:param model_path: Путь к модели.
	"""

	# Компиляции модели.
	model.compile(optimizer="adam", loss="categorical_crossentropy")

	print_summary(model)

	# Получаение данных для обучения и данных для валидации из кортежей.
	train_x, train_y = train
	test_x, test_y = test

	# Обучение и сохранение модели.
	model.fit(train_x, train_y, epochs=epochs_count, batch_size=batch_size, validation_data=(test_x, test_y), verbose=1)
	model.save(model_path)


def run_training(model_dir_path: str, model_name: str, epochs_count: int, batch_size: int) -> None:
	""" Запускает обучение модели для нейросети.

	:param model_dir_path: Путь к директории модели.
	:param model_name: Имя модели.
	:param epochs_count: Количество эпох.
	:param batch_size: Размер партии примеров (для обновления весов).
	"""

	# Загрузка данных.
	dataset: ndarray = load_data_dump(f"{model_dir_path}/both.pkl").reshape(-1, 1)
	train: ndarray = load_data_dump(f"{model_dir_path}/train.pkl")
	test: ndarray = load_data_dump(f"{model_dir_path}/test.pkl")

	# Подготовка токенизатора.
	tokenizer: Tokenizer = create_tokenizer(dataset[:, 0])
	vocabulary_size: int = len(tokenizer.word_index) + 1
	length: int = max_length(dataset[:, 0])

	print(f"Vocabulary Size: {vocabulary_size}")
	print(f"Max question length: {length}")

	# Подготовка данных для обучения.
	train_x: ndarray = encode_sequences(tokenizer, length, train[:, 0])
	train_y: ndarray = encode_sequences(tokenizer, length, train[:, 1])
	train_y: ndarray = encode_output(train_y, vocabulary_size)

	# Подготовка данных для валидации.
	test_x: ndarray = encode_sequences(tokenizer, length, test[:, 0])
	test_y: ndarray = encode_sequences(tokenizer, length, test[:, 1])
	test_y: ndarray = encode_output(test_y, vocabulary_size)

	# Определение модели.
	model: Sequential = define_model(vocabulary_size, length, 256)

	# Обучение модели.
	train_model(model, (train_x, train_y), (test_x, test_y), epochs_count, batch_size, f"{model_dir_path}/model.h5")


if __name__ == "__main__":
	config = Config("../config.yml")

	print("Running model training ...")
	print(f"- Dataset size: {config.get_dataset_size()}")
	print(f"- Epochs count: {config.get_epochs_count()}")
	print(f"- Batch size: {config.get_batch_size()}")

	run_training("../model", "Cortex-A", config.get_epochs_count(), config.get_batch_size())
