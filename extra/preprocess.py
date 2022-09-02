""" Подготовка данных для обучения модели.
"""

from core.preprocessor import Preprocessor
from extra.utils.config import Config

if __name__ == "__main__":
	config: Config = Config("config.yml")
	preprocessor: Preprocessor = Preprocessor("model", "data/data.json")

	preprocessor.preprocess_dataset(config.get_dataset_size())
