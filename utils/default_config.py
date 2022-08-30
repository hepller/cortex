""" Стандартная конфигурация.
"""

from utils.config import Config

config: any = Config("../config.yml").get_config()


def get_dataset_size() -> int:
	""" Получает размер датасета.

	:return: Размер датасета.
	"""

	return config["dataset_size"]

def get_epochs_count() -> int:
	""" Получает кол-во эпох.

	:return: Кол-во эпох.
	"""

	return config["epochs_count"]

def get_batch_size() -> int:
	""" Получает кол-во эпох.

	:return: Кол-во эпох.
	"""

	return config["batch_size"]
