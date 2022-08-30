""" Подготовка данных для обучения.
"""
import json
import os
from pickle import dump

from numpy import ndarray, array
from numpy.random import shuffle

from utils.default_config import get_dataset_size


def load_dataset(path: str) -> ndarray:
	""" Загружает датасет из JSON-файла в массив ndarray.

	:param path: Путь к датасету.
	:return: Датасет в виде ndarray.
	"""

	with open(path, "rb") as json_file:
		data_list: list = []
		json_data: any = json.load(json_file)

		for json_item in json_data:
			data_list.append([json_item["question"], json_item["answer"]])

		return array(data_list)


def save_data_dump(data: ndarray, filename: str) -> None:
	""" Сохраняет данные в pkl-файлы (дамп).

	:param data: Данные (в виде ndarray) для сохранения.
	:param filename: Имя файла.
	"""

	dump(data, open(filename, "wb"))

	print("Saved: %s" % filename)


def save_data(dataset: ndarray, train: ndarray, test: ndarray) -> None:
	""" Сохраняет данные в pkl-файлы.

	:param dataset: Датасет.
	:param train: Данные обучения.
	:param test: Тестовые данные.
	"""

	model_path: str = "../model"

	if not os.path.exists(model_path):
		print("Creating a model directory ...")

		os.mkdir(model_path)

	save_data_dump(dataset, f"{model_path}/both.pkl")
	save_data_dump(train, f"{model_path}/train.pkl")
	save_data_dump(test, f"{model_path}/test.pkl")

	print("All pkl files are saved")


def reformat_dataset(data: ndarray, dataset_size: int) -> ndarray:
	""" Форматирует и перемешивает данные из датасета.

	:param data: Датасет (в виде ndarray массива)
	:param dataset_size: Размер датасета.
	:return: Обрезанный до указанного размера датасет с перемешанными данными.
	"""

	# Обрезание датасета до указанного размера.
	reduced_dataset: ndarray = data[:dataset_size, :]

	# Перетасовка датасета в случайном порядке.
	shuffle(reduced_dataset)

	return reduced_dataset


def preprocess_dataset(dataset_path: str, dataset_size: int) -> None:
	""" Подготавливает данные из датасета для обучения.

	:param dataset_path: Путь к датасету.
	:param dataset_size: Размер датасета (после обрезания).
	"""

	# Загрузка и обрезание датасета.
	raw_dataset = load_dataset(dataset_path)
	reformatted_dataset = reformat_dataset(raw_dataset, dataset_size)

	# Разделения реформатированного датасета на train / test.
	train, test = reformatted_dataset[:dataset_size], reformatted_dataset[dataset_size:]

	# Сохранение данных в pkl-файлы
	save_data(reformatted_dataset, train, test)


if __name__ == "__main__":
	print("Run dataset preprocess ...")

	preprocess_dataset("../data/data.json", get_dataset_size())
