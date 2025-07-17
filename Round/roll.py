import random

num_sides = 6 #may change later

def roll_dice():
    die = random.randint(1, num_sides)
    return die

print(roll_dice())