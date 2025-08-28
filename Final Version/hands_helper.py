import json

with open("hands.json", "r") as file:
    output = json.load(file)
for key, value in output.items():
    print(f"{key}: {value['value']} x {value['multiplier']}")
    try:
        len(value["dies"])
        for i in range(len(value["dies"])):
            print(f"Number of same number {i +1}: {value['dies'][i]}")
    except TypeError:
        print(f"Number of same number 1: {value['dies']}")
    