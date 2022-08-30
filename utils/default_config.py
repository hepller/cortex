""" Стандартная конфигурация.
"""

from utils.config import Config

config: any = Config("../config.yml").get_config()


def get_dataset_size() -> int:
	""" Получает размер датасета.

	:return:
	"""

	return config["dataset_size"]

def get_epochs_count() -> int:
	""" Получает кол-во эпох.

	:return:
	"""

	return config["epochs_count"]
