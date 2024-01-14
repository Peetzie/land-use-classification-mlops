import os
import torch
import wandb
from torch import nn
from torch import optim

from torchvision import datasets
import torchvision.transforms as transforms
from torch.nn import Sequential, Conv2d, ReLU, MaxPool2d, BatchNorm2d
from torch.utils.data import DataLoader
from pytorch_lightning import LightningModule
from pytorch_lightning.callbacks.early_stopping import EarlyStopping


class CNN(LightningModule):
    """
    Basic convolutional neural network class.
    The kernel size, first layer's channels and
    the batch size can be specified

    Args:

    """

    def __init__(self,
                 kernel_size=3,
                 channels=3,
                 batch_size=2,
                 lr=1e-4,
                 img_dim=(256, 256)) -> None:
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
            BatchNorm2d(64)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(256, 128),
            nn.Dropout(),
            nn.Linear(128, 21)
        )
        self.loss_function = nn.CrossEntropyLoss()
        self.optimiser = optim.Adam(self.parameters(), lr=lr)
        self.transform = transforms.ToTensor()
        self.batch_size = batch_size
        self.img_dim = img_dim
        self.channels = channels
        self.lr = lr

    def forward(self, x):
        # make sure input tensor is flattened
        return self.classifier(self.conv(x))

    def training_step(self, batch, batch_idx):
        data, target = batch
        preds = self(data)
        loss = self.loss_function(preds, target.squeeze())
        acc = (target.squeeze() == preds.argmax(dim=-1)).float().mean()
        self.log('train_loss', loss)
        self.log('train_acc', acc)
        self.logger.experiment.log({'logits': wandb.Histogram(preds.cpu().detach())})
        return loss

    def validation_step(self, batch, batch_idx):
        data, target = batch
        preds = self(data)
        loss = self.loss_function(preds, target.squeeze())
        acc = (target.squeeze() == preds.argmax(dim=-1)).float().mean()
        self.log('val_loss', loss)
        self.log('val_acc', acc)
        return loss

    def image_transform(self):
        return transforms.Compose([
            transforms.Resize(self.img_dim),
            transforms.ToTensor(),
        ])

    def train_dataloader(self):
        path = os.path.join(os.getcwd(), 'data', 'landuse-scene-classification', 'images_train_test_val', 'train')
        dataset = datasets.ImageFolder(path, transform=self.image_transform())
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=True, )

    def test_dataloader(self):
        path = os.path.join(os.getcwd(), 'data', 'landuse-scene-classification', 'images_train_test_val', 'test')
        dataset = datasets.ImageFolder(path, transform=self.image_transform())
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

    def val_dataloader(self):
        path = os.path.join(os.getcwd(), 'data', 'landuse-scene-classification', 'images_train_test_val', 'validation')
        dataset = datasets.ImageFolder(path, transform=self.image_transform())
        return DataLoader(dataset, batch_size=self.batch_size, shuffle=True)

    def configure_optimizers(self):
        return self.optimiser


if __name__ == '__main__':
    from pytorch_lightning import Trainer, loggers

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
