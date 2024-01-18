import cv2
import requests
import torch

from project import CNN

image_path = "Data/landuse-scene-classification/images/agricultural/agricultural_000001.png"
out_path = "Data/api_images/"
img = cv2.imread(out_path + "image.png")

# class_dict = {
#     0: "agricultural",
#     1: "airplane",
#     2: "baseballdiamond",
#     3: "beach",
#     4: "buildings",
#     5: "chaparral",
#     6: "denseresidential",
#     7: "forest",
#     8: "freeway",
#     9: "golfcourse",
#     10: "intersection",
#     11: "mediumresidential",
#     12: "mobilehomepark",
#     13: "overpass",
#     14: "parkinglot",
#     15: "river",
#     16: "runway",
#     17: "sparseresidential",
#     18: "storagetanks",
#     19: "tenniscourt",
#     20: "harbor",
# }
n = 5
# model = CNN()
# img_tensor = torch.tensor(img, dtype=torch.float32).reshape(torch.Size([1, model.channels, *model.img_dim]))
# logits = model(img_tensor).squeeze()
# pred = torch.argsort(logits, descending=True).squeeze()[:n]
# [logits[el].item() for el in pred]
# [class_dict[el.item()] for el in pred]

files = {"data": (out_path, open(image_path, "rb"), "image/png")}
params = {"out_path": out_path, "n": 7}

# Make the POST request
response = requests.post("http://localhost:8000/cv_model/", files=files, params=params)

# Print the response
print("Response Code:", response.status_code)
# print("Response Content:", response.json())
if response.status_code == 200:
    for class_, prob in response.json()["probability_dictionary"].items():
        print(f"{class_}: {prob:.4f}")
