import json
import random

class Logic():
    def __init__(self):
        #Declare needed variables
        self.max_hands = 5
        self.played = [0,0,0,0,0,0]
        self.money = 0
        self.max_rounds = 5
        self.round = 0
        self.round_requirement = 0
        self.total = 0
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)
        self.dice_score = {}
    #play the current hand
    def play_hand(self):
        print(f"requirement {self.round_requirement}")
        print(f"round {self.round}")
        print(self.played)
        self.roll_dice()
        print(self.played)
        self.calculate_score()
        self.max_hands -= 1 
           
    #get new dice for the shop
    def new_shop_dice(self):
        #load json and pick 2 new random dice
        with open("shop_dice.json", "r") as file:
            self.shop_dice = json.load(file)
            self.items_in_shop = []
        for i in range(2):
            self.items_in_shop.append(self.shop_dice[str(random.randint(0, len(self.shop_dice) - 1))])
        print(self.items_in_shop)

        return self.items_in_shop
    #checks if the user has enough money for new dice
    def check_price(self, position):
        self.dice_pos = position
        if self.money >= self.items_in_shop[self.dice_pos]["cost"]:
            print("true")
            return True
        else:
            print("false")
            return False
    #replace current dice with shop dice
    def dice_change(self, dice_number):
        self.dice_to_replace = "die" + str(dice_number)
        self.dice[self.dice_to_replace] = self.items_in_shop[self.dice_pos]
        return True

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
        dice = "die" + str(die_number)
        #if unlocked lock dice and change image
        if self.dice_locked[dice] == False:
            self.dice_locked[dice] = True
        #if locked unlock dice and change image
        else:
            self.dice_locked[dice] = False
        print(f"Die {die_number} locked: {self.dice_locked[dice]}")
        return self.dice_locked
    #rolls the dice
    def roll_dice(self):
        for i in range(len(self.dice_locked)):
            # Skip locked dice
            if self.dice_locked[f"die{i+1}"]:
                continue  
            value = random.choice(self.dice[f"die{i+1}"]["sides"])
            self.dice_score[f"die{i+1}"] = value
        
        self.played = list(self.dice_score.values())
        return self.played
    #calculate the score of the played hand
    def calculate_score(self):
        #check the hand type played and set that as the base for the score
        self.check_hand()
        self.score = self.hands[self.played_hand]["value"]
        self.multiplier = self.hands[self.played_hand]["multiplier"]

        #adds the score of the dice
        try:
            if len(self.scoring) > 1:
                self.score += sum(self.scoring)
        except TypeError:
            self.score += self.scoring

        #calculate the score
        self.hand_score = self.score * self.multiplier
        self.total += self.score * self.multiplier
        print(self.hand_score)
        print(self.total)
        return self.total
    #check if the player beat the round
    def requirement(self):
        #check if the user beats the round requirement
        with open("round.json", "r") as file: 
            round_data = json.load(file)
        self.round_requirement = round_data["Round" + str(self.round)]["Requirement"]
        #if the user wins give them the reward money and reset the shop
        if self.total >= self.round_requirement:
            self.win = True
            payout = round_data["Round" + str(self.round)]["Payout"]
            print(f"payout {payout}")
            print(f"money {self.money}")
            self.money += payout
            self.new_shop_dice()
        else:
            self.win = False
        return self.win
    #reset all the values for new game
    def game_reset(self):
        self.round = 1
        with open("round.json", "r") as file: 
            round_data = json.load(file)
        self.round_requirement = round_data["Round" + str(self.round)]["Requirement"]
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        self.total = 0
        self.dice_score = {}
        self.played = []
        self.max_hands = 5
        self.roll_dice()
        self.money = 0
    #prepares next round
    def next_round(self):
        self.round += 1
        with open("round.json", "r") as file: 
            round_data = json.load(file)
        self.round_requirement = round_data["Round" + str(self.round)]["Requirement"]
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        self.total = 0
        self.dice_score = {}
        self.played = []
        self.max_hands = 5
        self.roll_dice()
    #get info for gui
    def get_gui_data(self):
        self.gui_info = {"requirement": self.round_requirement, "total": self.total,"hands": self.max_hands,"money": self.money, "played": self.played, "shop_dice": self.items_in_shop}
        return self.gui_info
