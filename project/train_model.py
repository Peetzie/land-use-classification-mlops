# Import necessary modules
from models.model import CNN
from omegaconf import OmegaConf
from pytorch_lightning import Trainer, loggers
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

# loading config
config = OmegaConf.load("project/configs/basic.yaml")


def main():
    # Print current config for user
    # Load and setup model with the config from file.
    model = CNN(
        kernel_size=config.basic.kernel_size,
        channels=config.basic.channels,
        img_dim=config.basic.img_dim,
        batch_size=config.hyperparameters.batch_size,
        lr=config.hyperparameters.learning_rate,
    )

    trainer = Trainer(
        accelerator="cpu",
        precision="32-true",
        profiler="simple",
        max_epochs=config.hyperparameters.epochs,
        logger=loggers.WandbLogger(project="land-use-classification", log_model="all"),
        callbacks=[EarlyStopping(monitor="val_loss", mode="min")],
    )
    trainer.fit(
        model,
        train_dataloaders=model.train_dataloader(),
        val_dataloaders=model.val_dataloader(),
    )


if __name__ == "__main__":
    import wandb

    wandb.login(key="7d4f6c7fcf5702feb08b64a3f24e850a3f66a5b5")
    main()
