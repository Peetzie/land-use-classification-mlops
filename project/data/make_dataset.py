import opendatasets as od
import os

dataset_URL = "https://www.kaggle.com/datasets/apollo2506/landuse-scene-classification"
data_folder = "landuse-scene-classification"


def make_dataset():
    """
    Downloads the dataset into data and extracts the content.asdijsdijasdijasdijasidj
    """
    od.download(dataset_URL, data_dir="data/", unzip=True)


if __name__ == "__main__":
    make_dataset()
