import requests
import cv2

image_path = 'data/landuse-scene-classification/images/agricultural/agricultural_000001.png'
out_path = 'data/api_images/'
img = cv2.imread(out_path + "image.png")
files = {"data": (out_path, open(image_path, "rb"), "image/png")}
params = {"out_path": out_path}

# Make the POST request
response = requests.post("http://localhost:8000/cv_model/",
                         files=files,
                         params=params)

# Print the response
print("Response Code:", response.status_code)
print("Response Content:", response.json())
