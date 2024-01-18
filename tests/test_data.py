import os

import torch
from torch.utils.data import DataLoader
from torchvision import datasets

from project import CNN
from project.logger.logger import LoggerConfigurator

logger_configurator = LoggerConfigurator("Tests")
logger = logger_configurator.get_logger()


def test_data():
    model = CNN()
    for name, length in zip(["train", "test", "validation"], [7350, 1050, 2100]):
        path = os.path.join("Data", "landuse-scene-classification", "images_train_test_val", f"{name}")
        dataset = datasets.ImageFolder(path, transform=model.image_transform())
        data_loader = DataLoader(dataset, batch_size=model.batch_size, shuffle=True)
        (
            images,
            target,
        ) = iter(data_loader).__next__()
        assert len(dataset.classes) == 21, logger.error(
            f"Unexpected number of classes in the dataset. Got: {dataset.classes}, but expected 21"
        )
        assert len(dataset) == length, logger.error(
            f"The length of the dataset split was not as expected for split: {name}"
        )
        assert len(target) == model.batch_size, logger.error(
            f"Unexpected batch size, Got: {target} but expected: {model.batch_size}"
        )
        assert images.shape == torch.Size(
            [model.batch_size, model.channels, model.img_dim, model.img_dim]
        ), logger.error(
            "Unexpected size of image. Got: {}, expected: {}".format(
                images.shape, torch.Size([model.batch_size, model.channels, model.img_dim, model.img_dim])
            )
        )
        assert (torch.sum(images < 0) == 0).item(), logger.error(
            f"Possible negative RGB value contained in image. This is unexpected"
        )
        assert (torch.sum((length < target) & (target < 0)) == 0).item(), logger.error(
            "Unexpected output of target. Might contain negative values or exceed expected values"
        )
        logger.info(f"All tests passed for split: {name}")
    logger.info("All tests passed for data")
