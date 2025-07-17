import json

played = [1,1]
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

with open("hands.json", "r") as file: 
    hands = json.load(file)
for hand in hands:
    if sorted(scoring) == hands[hand]["dies"]:
        print(hand)