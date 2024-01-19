import requests

for i in range(1, 3):
    print(f'Image {i}:')
    n = 5
    image_path = f"Data/landuse-scene-classification/images/parkinglot/parkinglot_00000{i}.png"

    files = {"data": ("", open(image_path, "rb"), "")}
    params = {"n": 2}

    # Make the POST request
    # response = requests.post("http://localhost:8000/cv_model/", files=files, params=params)
    response = requests.post("https://app-4-odm3naduba-ez.a.run.app/cv_model/", files=files, params=params)

    # Print the response
    print("Response Code:", response.status_code)
    # print("Response Content:", response.json())
    if response.status_code == 200:
        for class_, prob in response.json()["probability_dictionary"].items():
            print(f"{class_}: {prob:.4f}")
        pass
    else:
        pass
