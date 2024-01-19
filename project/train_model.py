# Import necessary modules
import argparse

from models.model import CNN
from omegaconf import OmegaConf
from pytorch_lightning import Trainer, loggers
from pytorch_lightning.callbacks.early_stopping import EarlyStopping


def main(config_path):
    # Load and setup model with the config from file.
    config = OmegaConf.load(config_path)
    model = CNN(
        kernel_size=config.basic.kernel_size,
        channels=config.basic.channels,
        img_dim=config.basic.img_dim,
        batch_size=config.hyperparameters.batch_size,
        lr=config.hyperparameters.learning_rate,
    )

    trainer = Trainer(
        accelerator=config.basic.cunit,
        precision=config.basic.precision,
        profiler=config.basic.profiler,
        max_epochs=config.hyperparameters.epochs,
        logger=loggers.WandbLogger(project=config.logging.name, log_model=config.logging.model),
        callbacks=[EarlyStopping(monitor=config.callbacks.monitor, mode=config.callbacks.mode)],
    )
    trainer.fit(
        model,
        train_dataloaders=model.train_dataloader(),
        val_dataloaders=model.val_dataloader(),
    )


if __name__ == "__main__":
    import wandb

    # Add command line argument for the config file path
    parser = argparse.ArgumentParser(description="Train the model.")
    parser.add_argument(
        "--config", type=str, default="project/configs/basic.yaml", help="Path to the configuration file."
    )

    args = parser.parse_args()

    wandb.login(key="7d4f6c7fcf5702feb08b64a3f24e850a3f66a5b5")
    main(args.config)
