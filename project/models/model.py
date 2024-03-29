import os
import torch
import torchvision.transforms as transforms
from logger import LoggerConfigurator
from pytorch_lightning import LightningModule
from pytorch_lightning.callbacks.early_stopping import EarlyStopping
from torch import nn, optim
from torch.nn import BatchNorm2d, Conv2d, MaxPool2d, ReLU, Sequential
from torch.utils.data import DataLoader
from torchvision import datasets

import wandb

logger_configurator = LoggerConfigurator("Model output")
logger = logger_configurator.get_logger()


class CNN(LightningModule):
    """
    Basic convolutional neural network class.
    The kernel size, first layer's channels and
    the batch size can be specified

    Args:
        kernel_size (int): Kernel size for the convolutional layers
        channels (int): Number of channels for the first convolutional layer
        batch_size (int): Batch size for the data loader
        lr (float): Learning rate for the optimizer
        img_dim (tuple): Image dimensions for the image transformer

    Return: CNN -> LightningModule

    """

    def __init__(
        self,
        kernel_size: int = 3,
        channels: int = 3,
        batch_size: int = 2,
        lr: float = 1e-4,
        img_dim: int = 256,
    ) -> None:
        super().__init__()

        self.conv = Sequential(
            Conv2d(in_channels=channels, out_channels=32, kernel_size=kernel_size),
            ReLU(),
            MaxPool2d(kernel_size=2),
            BatchNorm2d(32),
            Conv2d(in_channels=32, out_channels=64, kernel_size=kernel_size),
            ReLU(),
            MaxPool2d(kernel_size=2),
            BatchNorm2d(64),
            Conv2d(in_channels=64, out_channels=64, kernel_size=kernel_size),
            ReLU(),
            MaxPool2d(kernel_size=2),
            BatchNorm2d(64),
            Conv2d(in_channels=64, out_channels=64, kernel_size=kernel_size),
            ReLU(),
            MaxPool2d(kernel_size=2),
            BatchNorm2d(64),
            Conv2d(in_channels=64, out_channels=64, kernel_size=kernel_size),
            ReLU(),
            MaxPool2d(kernel_size=2),
            BatchNorm2d(64),
            Conv2d(in_channels=64, out_channels=64, kernel_size=kernel_size),
            ReLU(),
            MaxPool2d(kernel_size=2),
            BatchNorm2d(64),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(256, 128), nn.Dropout(), nn.Linear(128, 21), nn.Softmax(dim=-1)
        )
        self.loss_function = nn.CrossEntropyLoss()
        self.optimiser = optim.Adam(self.parameters(), lr=lr)
        self.transform = transforms.ToTensor()
        self.batch_size = batch_size
        self.img_dim = img_dim
        self.channels = channels
        self.lr = lr

    def forward(self, x) -> torch.Tensor:
        # make sure input tensor is flattened
        return self.classifier(self.conv(x))

    def training_step(self, batch, batch_idx):
        """
        Performs a training step

                Parameters:
                        batch (<Type>): The batch of data and labels
                        batch_idx (int): Index of the current batch in the batchloader.

                Returns:
                       loss (float): The avagerage loss for that training step
        """
        data, target = batch
        preds = self(data)
        loss = self.loss_function(preds, target.squeeze())
        acc = (target.squeeze() == preds.argmax(dim=-1)).float().mean()
        logger.info("Current training loss: {:.4f} and accuracy".format(loss, acc))
        self.logger.experiment.log({"logits": wandb.Histogram(preds.cpu().detach())})
        return loss

    def validation_step(self, batch, batch_idx):
        """
        Performs a Validation step

                Parameters:
                        batch (<Type>): The batch of data and labels
                        batch_idx (int): Index of the current batch in the batchloader.

                Returns:
                       loss (float): The avagerage loss for that validation step
        """
        data, target = batch
        preds = self(data)
        loss = self.loss_function(preds, target.squeeze())
        acc = (target.squeeze() == preds.argmax(dim=-1)).float().mean()
        logger.info("Current training loss: {:.4f} and accuracy".format(loss, acc))
        return loss

    def image_transform(self):
        """
        Helper transformer to ensure image dimensionality to the specified requirements during intialization.
        Converts the images to tensor objects.

        Returns:
            transforms.Compose: Composed transformer object
        """

        return transforms.Compose(
            [
                transforms.Resize((self.img_dim, self.img_dim)),
                transforms.ToTensor(),
            ]
        )

    def train_dataloader(self):
        """
        Loads the training data from the specified path and applies the image transformer.
        Sets the dataloader's num_workers according to the number of available CPU
        cores.

        Returns:
            DataLoader: The training data loader
        """
        path = os.path.join(
            os.getcwd(),
            "Data",
            "landuse-scene-classification",
            "images_train_test_val",
            "train",
        )
        dataset = datasets.ImageFolder(path, transform=self.image_transform())
        return DataLoader(
            dataset,
            batch_size=self.batch_size,
            shuffle=True,
        )

    def test_dataloader(self):
        """
        Loads the testing data from the specified path and applies the image transformer.
        Sets the dataloader's num_workers according to the number of available CPU
        cores.

        Returns:
            DataLoader: The test data loader
        """
        path = os.path.join(
            os.getcwd(),
            "Data",
            "landuse-scene-classification",
            "images_train_test_val",
            "test",
        )
        dataset = datasets.ImageFolder(path, transform=self.image_transform())
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        """
        Loads the valdation data from the specified path and applies the image transformer.
        Sets the dataloader's num_workers according to the number of available CPU
        cores.

        Returns:
            DataLoader: The validation data loader
        """
        path = os.path.join(
            os.getcwd(),
            "Data",
            "landuse-scene-classification",
            "images_train_test_val",
            "validation",
        )
        dataset = datasets.ImageFolder(path, transform=self.image_transform())
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

    def configure_optimizers(self):
        return self.optimiser

    def load(self, filepath):
        self.load_state_dict(torch.load(filepath))


if __name__ == "__main__":
    from pytorch_lightning import Trainer, loggers

    trainer = Trainer(
        accelerator="cpu",
        precision="32-true",
        profiler="simple",
        max_epochs=100,
        logger=loggers.WandbLogger(project="land-use-classification", log_model="all"),
        callbacks=[EarlyStopping(monitor="val_loss", mode="min")],
    )
    model = CNN()
    trainer.fit(
        model,
        train_dataloaders=model.train_dataloader(),
        val_dataloaders=model.val_dataloader(),
    )
