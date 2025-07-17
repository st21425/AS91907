import json
import random

with open("dice.json", "r") as file: 
    dies = json.load(file)

played = []

for i in range(6):
    num_sides = len(dies[f"die{i+1}"])
    die = random.randint(1, num_sides)
    value = dies[f"die{i+1}"][f"side{die}"]["value"]
    played.append(value)

