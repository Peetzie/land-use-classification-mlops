import os

import opendatasets as od

dataset_URL = "https://www.kaggle.com/datasets/apollo2506/landuse-scene-classification"
data_folder = "landuse-scene-classification"


def make_dataset():
    """
    Description:
        Downloads the dataset into data and extracts the content using the opendatasets library.
        Important to have the kaggle.json file in the root folder.
    Returns:
        None

    """
    od.download(dataset_URL, data_dir="Data/", unzip=True)


if __name__ == "__main__":
    make_dataset()
