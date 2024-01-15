import os
import torch

from project import CNN
from torchvision import datasets
from torch.utils.data import DataLoader


def test_data():
    model = CNN()
    for name, length in zip(["train", "test", "validation"], [7350, 1050, 2100]):
        path = os.path.join(os.getcwd(), f"data/raw/images_train_test_val/{name}")
        dataset = datasets.ImageFolder(path, transform=model.image_transform())
        data_loader = DataLoader(dataset, batch_size=model.batch_size, shuffle=True)
        (
            images,
            target,
        ) = iter(data_loader).__next__()
        assert len(dataset.classes) == 21
        assert len(dataset) == length
        assert len(target) == model.batch_size
        assert images.shape == torch.Size([model.batch_size, model.channels, *model.img_dim])
        assert (torch.sum(images < 0) == 0).item()
        assert (torch.sum((length < target) & (target < 0)) == 0).item()
