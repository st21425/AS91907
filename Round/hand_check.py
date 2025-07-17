import json

played = [7,7,1,1,1,7]# Example played dice

#makes list of scoring and unscoring dies
scoring = []
unscoring = []
for i in played: 
    if i in scoring:
        scoring.append(i)
    elif i in unscoring:
        for x in range(2):
            scoring.append(i)
        unscoring.remove(i)
    else:
        unscoring.append(i)
if len(scoring) == 0:
    scoring = [0]

#counts how many of each die is played
numbers = {}
for i in scoring:
    if i in numbers:
        numbers[i] += 1
    else:
        numbers[i] = 1

#format it in a way that can be compared to the json
played_type = []
for key, value in numbers.items():
    played_type.append(value)

#loads json
with open("hands.json", "r") as file: 
    hands = json.load(file)

#checks what hand is played
for hand in hands: 
    if sorted(played_type) == hands[hand]["dies"]:
        print(hand)