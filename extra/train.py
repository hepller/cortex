""" Обучение модели нейросети.
"""
import os.path

from core.trainer import Trainer
from extra.utils.config import Config

if __name__ == "__main__":
	model_dir_path: str = "model"

	config: Config = Config("../extra/config.yml")
	trainer: Trainer = Trainer(model_dir_path, "Cortex-Test")

	overtrain: bool = os.path.exists(f"{model_dir_path}/model.h5")

	trainer.train_model(epochs_count=config.get_epochs_count(), batch_size=config.get_batch_size(), overtrain=overtrain)
