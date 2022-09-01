""" Обучение модели нейросети.
"""

from core.trainer import Trainer
from extra.utils.config import Config

if __name__ == "__main__":
	config: Config = Config("../extra/config.yml")
	trainer: Trainer = Trainer("../../model", "Cortex-Test")

	trainer.run_training(config.get_epochs_count(), config.get_batch_size())
