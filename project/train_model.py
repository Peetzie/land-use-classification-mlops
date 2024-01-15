
import os

from omegaconf import OmegaConf

# Import necessary modules
from models import CNN

#loading
config = OmegaConf.load("project/configs/basic.yaml")

def main():
    print(config)
    model = CNN(kernel_size=config.basic.kernel_size, channels=config.basic.channels, img_dim=config.basic.img_dim, batch_size=config.hyperparameters.batch_size, lr=config.hyperparameters.learning_rate)
    print(f"working dir::::::::::::::::::::::{os.getcwd()}")
    train_dl = model.train_dataloader()
    val_dl = model.val_dataloader()
    test_dl = model.test_dataloader()
    print("hi")



if __name__ == "__main__":
    main()
