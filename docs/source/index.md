## Documentation

### Getting started

#### Creating a virtual enviroment
For development it is recommended seting up a virtual enviroment. To ensure compatibility between packages and keeping the global enviroment clean.

##### Anaconda / Miniconda users
For Anaconda or Miniconda users this can be done by creating a virtual enviroment with the following command. This will create a new conda enviroment with **python=3.10** named **project**.

```
make create_environment
conda activate project
make requirements
```
All set - Skip ahead to [Getting the data](#getting-the-data)
##### Using virtualenv
**NB! Python < 3.11 required**
```
python -m venv venv
```
Activate the enviroment

Windows users:
```
.\venv\Scripts\activate
```

Mac OS and Linux distributions:
```
source venv/bin/activate
```
Finally install the dependencies in the *requirements.txt* file.

```
pip -m install -r requirements.txt
```


#### Getting the data
In order to obtain the dataset either download the dataset from the [source](https://www.kaggle.com/datasets/apollo2506/landuse-scene-classification), and place into a folder Data placed in the root folder.

Alternatively:
Go to your kaggle account, Scroll to API section and Click Expire API Token to remove previous tokens
Click on Create New API Token - It will download kaggle.json file on your machine. Place the JSON file in the root folder of the project.

Finally, use the automated script for downloading the dataset:

```
python project/data/make_dataset.py
```

#### Code structure

Inside the *project* folder you will find several folders, configs, data, logger, models, visualizations.
In data we keep a script for making the dataset see section [Getting the data](#getting-the-data).
Logger contains a Logging class, which has a predefined setup. For any changes to log levels and more please change the settings within there.
Model contains the convolutional neural network used for the training and prediction of land-use.
All parameters for the model are pre-defined in the model so far no configuration file is passed. However using the *train_model.py* file from the project root, we pass in configuration files which are stored in the *configs* folder.

#### Testing the code base
In the project root folder, a tests folder has been created. Utilizing the *pytest* package, the code can be tested.
Current implemented tests focuses on data testing ensureing the correct format and length to be expected from the download, and the model checks that the expected in- and output matches the expectations respectively.


#### Pre-commits
The repository is set up using pre-commit hooks.
Current pre-commit hoocks checks the following:
- Trailing whitespace
- End of file fixer
- Check Yaml
- Check added large files
- Ruff linting with *fix* applied.

For source explanations please check the [pre-commit docs](https://pre-commit.com/hooks.html)
