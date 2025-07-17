import json
import random

dies_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}

with open("dice.json", "r") as file: 
    dies = json.load(file)

dice_score = {}


for i in range(len(dies_locked)):
    if dies_locked[f"die{i+1}"] == True:
        continue # Skip locked dice
    elif dies_locked[f"die{i+1}"] == False:
        num_sides = len(dies[f"die{i+1}"])
        die = random.randint(1, num_sides)
        value = dies[f"die{i+1}"][f"side{die}"]["value"]
        dice_score[f"die{i+1}"] = value
    else:
        print("Error: Invalid die state")

played = []

for key, value in dice_score.items():
    played.append(value)
print(played)
