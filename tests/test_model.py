import torch
from pytorch_lightning import Callback, Trainer, loggers
from pytorch_lightning.callbacks.early_stopping import EarlyStopping

from project import CNN
from project.logger.logger import LoggerConfigurator

logger_configurator = LoggerConfigurator("Tests")
logger = logger_configurator.get_logger()


class MetricTracker(Callback):
    def __init__(self):
        self.collection = []

    def on_validation_batch_end(
        self,
        trainer,
        module,
        outputs,
        batch,
        batch_idx: int,
        dataloader_idx: int = 0,
    ):
        vacc = outputs["val_acc"]  # you can access them here
        self.collection.append(vacc)  # track them

    def on_validation_epoch_end(self, trainer, module):
        elogs = trainer.logged_metrics  # access it here
        self.collection.append(elogs)
        # do whatever is needed


def test_in_out():
    model = CNN()
    test_batch = torch.rand([model.batch_size, model.channels, model.img_dim, model.img_dim])

    pred = model(test_batch)
    assert pred.shape == torch.Size((model.batch_size, 21)), logger.error(
        "Unexpected output shape. Expected: {}, got: {}".format(torch.Size((model.batch_size, 21)), pred.shape)
    )
    logger.info("All tests passed for the model")
