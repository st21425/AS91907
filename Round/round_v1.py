import json
import random

class Round():
    def __init__(self, round):
        #Declare values
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)
        self.dice_score = {}
        self.played = []
        self.total = 0
        self.round = round
        self.round += 1
        self.max_hands = 4

        #start round
        for i in range(self.max_hands):
            self.roll_dice()
            self.check_hand()
            self.calculate_score()
        self.requirement()


    #checks the hand played
    def check_hand(self):
        self.scoring = []
        self.unscoring = []
        #finds matching dice
        for i in self.played: 
            if i in self.scoring:
                self.scoring.append(i)
            elif i in self.unscoring:
                for x in range(2):
                    self.scoring.append(i)
                self.unscoring.remove(i)
            else:
                self.unscoring.append(i)
        #if no matching dice play highest dice
        if len(self.scoring) == 0:
            self.unscoring.sort()
            self.scoring = self.unscoring[-1]
        
        #adds to dictionary
        self.numbers = {}
        try:
            if len(self.scoring) > 1:
                for i in self.scoring:
                    if i in self.numbers:
                        self.numbers[i] += 1
                    else:
                        self.numbers[i] = 1
        except TypeError:
            self.numbers[self.scoring] = 1

        #adds the values to a list in the format of the json
        self.played_type = []
        for key, value in self.numbers.items():
            self.played_type.append(value)
        #checks hand and compares it to the json
        with open("hands.json", "r") as file: 
            self.hands = json.load(file)
        for hand in self.hands:
            if sorted(self.played_type) == self.hands[hand]["dies"]:
                self.played_hand = hand
                break
        print(self.played_hand)
    
    #locks the dice
    def lock_dice(self, die_number):
        dice = "die" + die_number
        if self.dice_locked[dice] == False:
            self.dice_locked[dice] = True
        else:
            self.dice_locked[dice] = False

    #rolls the dice
    def roll_dice(self):
        #rolls the unlocked dice
        for i in range(len(self.dice_locked)):
            if self.dice_locked[f"die{i+1}"]:
                continue  # Skip locked dice
            num_sides = len(self.dice[f"die{i+1}"])
            die = random.randint(1, num_sides)
            value = self.dice[f"die{i+1}"][f"side{die}"]["value"]
            self.dice_score[f"die{i+1}"] = value
        self.played = list(self.dice_score.values())
        print(self.played)
    
    def calculate_score(self):
        self.check_hand()
        score = self.hands[self.played_hand]["value"]
        multiplier = self.hands[self.played_hand]["multiplier"]

        try:
            if len(self.scoring) > 1:
                score += sum(self.scoring)
        except TypeError:
            score += self.scoring

        self.hand_score = score * multiplier
        self.total += score * multiplier
        print(self.hand_score)
        print(self.total)
        return self.total
    
    def requirement(self):
        with open("round.json", "r") as file: 
            round_data = json.load(file)
        self.requirement = round_data["Round" + str(self.round)]["Requirement"]
        if self.total >= self.requirement:
            self.win = True
            print("win")
        else:
            self.win = False
            print("lose")
        return self.win
    
Round(0)