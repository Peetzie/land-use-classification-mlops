

if __name__ == '__main__':
    from models import CNN
    from pytorch_lightning import Trainer, loggers
    from pytorch_lightning.callbacks.early_stopping import EarlyStopping

    trainer = Trainer(
        accelerator='cpu',
        precision="32-true",
        profiler="simple",
        max_epochs=10,
        logger=loggers.WandbLogger(project="land-use-classification"),
        callbacks=[EarlyStopping(monitor="val_loss", mode="min")],
    )
    model = CNN()
    trainer.fit(model,
                train_dataloaders=model.train_dataloader(),
                val_dataloaders=model.val_dataloader())

