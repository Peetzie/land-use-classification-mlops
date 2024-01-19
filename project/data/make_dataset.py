import opendatasets as od
from logger import LoggerConfigurator

dataset_URL = "https://www.kaggle.com/datasets/apollo2506/landuse-scene-classification"
data_folder = "landuse-scene-classification"
logger_configurator = LoggerConfigurator("Make Dataset")
logger = logger_configurator.get_logger()


def make_dataset():
    """
    Description:
        Downloads the dataset into data and extracts the content using the opendatasets library.
        Important to have the kaggle.json file in the root folder.
    Returns:
        None

    """
    od.download(dataset_URL, data_dir="Data/", unzip=True)
    logger.info("Dataset successfully downloaded")


if __name__ == "__main__":
    make_dataset()
