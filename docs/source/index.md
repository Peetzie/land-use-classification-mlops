~~# Documentation

## Getting Started

### Creating a Virtual Environment

For development, it is recommended to set up a virtual environment to ensure compatibility between packages and keep the global environment clean.

**Anaconda / Miniconda users**

For Anaconda or Miniconda users, create a virtual environment with the following command. This will generate a new conda environment with **python=3.10** named **project**.

```bash
make create_environment
conda activate project
make requirements
```

All set! Skip ahead to [Getting the data](#getting-the-data)

**Virtualenv users**
#### NB! Python < 3.11 required
```bash
python -m venv venv
```
Activate the enviroment:

Windows users:
```bash
  .\venv\Scripts\activate
```

Mac OS and Linux Distributions
```bash
source venv/bin/activate
```
Finally, install the depencenies from the *requirements.txt* file
```bash
pip install -r requirements.txt

```

## Getting the Data

To obtain the dataset, either download it from the [source](https://www.kaggle.com/datasets/apollo2506/landuse-scene-classification) and place it into a folder named *Data* in the root directory.

Alternatively:

1. Go to your Kaggle account, scroll to the API section, and click "Expire API Token" to remove previous tokens.
2. Click on "Create New API Token" - it will download the *kaggle.json* file. Place this file in the root folder of the project.

Finally, use the automated script for downloading the dataset:

```bash
python project/data/make_dataset.py
```

### FastAPI~~

The API has one function "cv_model" which takes a path to a local image opened in a byte format:
```python
files = {"data": ("", open(image_path, "rb"), "")}
params = {"n": 2}

response = requests.post("https://app-4-odm3naduba-ez.a.run.app/cv_model/", files=files, params=params)
```
This returns the top n predictions from the model in a dictionay as such:
```python
for class_, prob in response.json()["probability_dictionary"].items():
    print(f"{class_}: {prob:.4f}")
```
