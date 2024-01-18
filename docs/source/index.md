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

Finally use the automated script for downloading the dataset:

```
python project/data/make_dataset.py
```
