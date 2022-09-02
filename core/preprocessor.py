""" Компонент для подготовки данных для обучения модели.
"""

import json
import os
from pickle import dump

from numpy import ndarray, array
from numpy.random import shuffle


class Preprocessor:
	""" Класс для подготовки нейросети к обучению.
	"""

	def __init__(self, model_dir_path: str, dataset_path: str):
		""" Инициализирует препроцессор.

		:param model_dir_path: Путь к директории с моделью.
		:param dataset_path: Путь к датасету.
		"""

		self.model_dir_path: str = model_dir_path
		self.dataset_path: str = dataset_path

	def load_json_dataset(self) -> ndarray:
		""" Загружает датасет из JSON-файла в N-мерный массив.

		:return: Датасет в виде N-мерного массива.
		"""

		with open(self.dataset_path, "rb") as json_file:
			data_list: list = []
			json_data: any = json.load(json_file)

			for json_item in json_data:
				data_list.append([json_item["question"], json_item["answer"]])

			return array(data_list)

	@staticmethod
	def save_data_dump(data: ndarray, filename: str) -> None:
		""" Сохраняет данные в pkl-файл (дамп).

		:param data: Данные для сохранения (в виде N-мерного массива).
		:param filename: Имя файла.
		"""

		dump(data, open(filename, "wb"))

		print(f" * Saved: \"{filename}\"")

	def save_pickle_data(self, dataset: ndarray, train: ndarray, test: ndarray) -> None:
		""" Сохраняет данные в pkl-файлы.

		:param dataset: Датасет.
		:param train: Данные обучения.
		:param test: Тестовые данные.
		"""

		if not os.path.exists(self.model_dir_path):
			print("Creating a model directory ...")

			os.mkdir(self.model_dir_path)

		print("")
		print("Saving pickle files ...")

		self.save_data_dump(dataset, f"{self.model_dir_path}/both.pkl")
		self.save_data_dump(train, f"{self.model_dir_path}/train.pkl")
		self.save_data_dump(test, f"{self.model_dir_path}/test.pkl")

		print("")
		print("All pickle files are saved")

	@staticmethod
	def reformat_dataset(data: ndarray, dataset_size: int) -> ndarray:
		""" Форматирует и перемешивает данные из датасета.

		:param data: Датасет (в виде N-мерного массива).
		:param dataset_size: Размер датасета после обрезания.
		:return: Обрезанный до указанного размера датасет с перемешанными данными.
		"""

		# Обрезание датасета до указанного размера.
		reduced_dataset: ndarray = data[:dataset_size, :]

		# Перетасовка датасета в случайном порядке.
		shuffle(reduced_dataset)

		return reduced_dataset

	def preprocess_dataset(self, dataset_size: int = 500) -> None:
		""" Подготавливает данные из датасета для обучения.

		:param dataset_size: Размер датасета после обрезания (по умолчанию: 500).
		"""

		# Загрузка и обрезание датасета.
		raw_dataset: ndarray = self.load_json_dataset()
		reformatted_dataset: ndarray = self.reformat_dataset(raw_dataset, dataset_size)

		# Разделения реформатированного датасета на train / test.
		train, test = reformatted_dataset[:dataset_size], reformatted_dataset[dataset_size:]

		print(f"Running dataset preprocessing ...")
		print(f" * Dataset size: {dataset_size}")

		# Сохранение данных в pkl-файлы.
		self.save_pickle_data(reformatted_dataset, train, test)
