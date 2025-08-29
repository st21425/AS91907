import json
import random
import urllib.request


class Logic():
    def __init__(self):
        self.github_path = "https://raw.githubusercontent.com/st21425/AS91907/main/Final%20Version/"
        # Declare needed variables
        self.max_hands = 5
        self.played = [0, 0, 0, 0, 0, 0]
        self.money = 0
        self.max_rounds = 5
        self.round = 0
        self.round_requirement = 0
        self.total = 0
        self.dice_locked = {"die1": False, "die2": False,
                            "die3": False, "die4": False, "die5": False, "die6": False}
        self.items_in_shop = []
        self.dice = self.load_json("dice.json")
        self.types = self.load_json("dice_types.json")
        self.dice_score = {}
    # play the current hand

    def play_hand(self):
        print(f"requirement {self.round_requirement}")
        print(f"round {self.round}")
        print(self.played)
        self.roll_dice()
        print(self.played)
        self.calculate_score()
        self.max_hands -= 1

    # get new dice for the shop
    def new_shop_dice(self):
        # load json and pick 2 new random dice
        self.shop_dice = self.load_json("shop_dice.json")
        self.items_in_shop = []
        for i in range(2):
            self.items_in_shop.append(
                self.shop_dice[str(random.randint(0, len(self.shop_dice) - 1))])

        return self.items_in_shop
    # checks if the user has enough money for new dice

    def check_price(self, position):
        self.dice_pos = position
        if self.money >= self.items_in_shop[self.dice_pos]["cost"]:
            print("true")
            return True
        else:
            print("false")
            return False
    # replace current dice with shop dice

    def dice_change(self, dice_number):
        self.dice_to_replace = "die" + str(dice_number)
        self.dice[self.dice_to_replace] = self.items_in_shop[self.dice_pos]
        self.money -= self.items_in_shop[self.dice_pos]["cost"]
        return True

    # checks the hand played
    def check_hand(self):
        self.scoring = []
        self.unscoring = []
        # finds matching dice
        for i in self.played:
            if i in self.scoring:
                self.scoring.append(i)
            elif i in self.unscoring:
                for x in range(2):
                    self.scoring.append(i)
                self.unscoring.remove(i)
            else:
                self.unscoring.append(i)
        # if no matching dice play highest dice
        if len(self.scoring) == 0:
            self.unscoring.sort()
            self.scoring = self.unscoring[-1]

        # adds to dictionary
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

        # adds the values to a list in the format of the json
        self.played_type = []
        for key, value in self.numbers.items():
            self.played_type.append(value)
        # checks hand and compares it to the json
        self.hands = self.load_json("hands.json")
        for hand in self.hands:
            if sorted(self.played_type) == self.hands[hand]["dies"]:
                self.played_hand = hand
                break
        print(self.played_hand)
    # locks the dice

    def lock_dice(self, die_number):
        dice = "die" + str(die_number)
        # if unlocked lock dice and change image
        if self.dice_locked[dice] == False:
            self.dice_locked[dice] = True
        # if locked unlock dice and change image
        else:
            self.dice_locked[dice] = False
        print(f"Die {die_number} locked: {self.dice_locked[dice]}")
        return self.dice_locked
    # rolls the dice

    def roll_dice(self):
        for i in range(len(self.dice_locked)):
            # Skip locked dice
            if self.dice_locked[f"die{i+1}"]:
                continue
            value = random.choice(self.dice[f"die{i+1}"]["sides"])
            self.dice_score[f"die{i+1}"] = value

        self.played = list(self.dice_score.values())
        return self.played
    # calculate the score of the played hand

    def calculate_score(self):
        # check the hand type played and set that as the base for the score
        self.check_hand()
        self.score = self.hands[self.played_hand]["value"]
        self.multiplier = self.hands[self.played_hand]["multiplier"]

        # adds the score of the dice
        try:
            if len(self.scoring) > 1:
                self.score += sum(self.scoring)
        except TypeError:
            self.score += self.scoring

        for i in self.dice:
            dice_type = self.dice[i]["type"]
            properties = self.types[dice_type]
            self.score += properties["score"]
            self.multiplier += properties["+mult"]
            self.multiplier = self.multiplier * properties["xmult"]

        # calculate the score
        self.hand_score = self.score * self.multiplier
        if self.max_hands < 5:
            self.total += self.score * self.multiplier
        print(self.hand_score)
        print(self.total)
        return self.total
    # check if the player beat the round

    def requirement(self):
        # check if the user beats the round requirement
        round_data = self.load_json("round.json")
        self.round_requirement = round_data["Round" +
                                            str(self.round)]["Requirement"]
        # if the user wins give them the reward money and reset the shop
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
    # reset all the values for new game

    def game_reset(self):
        self.round = 1
        round_data = self.load_json("round.json")
        self.round_requirement = round_data["Round" +
                                            str(self.round)]["Requirement"]
        self.dice = self.load_json("dice.json")
        self.dice_locked = {"die1": False, "die2": False,
                            "die3": False, "die4": False, "die5": False, "die6": False}
        self.total = 0
        self.dice_score = {}
        self.played = []
        self.max_hands = 5
        self.roll_dice()
        self.money = 0
    # prepares next round

    def next_round(self):
        if self.round != self.max_rounds + 1:
            self.round += 1
            round_data = self.load_json("round.json")
            self.round_requirement = round_data["Round" +
                                                str(self.round)]["Requirement"]
            self.dice_locked = {"die1": False, "die2": False,
                                "die3": False, "die4": False, "die5": False, "die6": False}
            self.total = 0
            self.dice_score = {}
            self.played = []
            self.max_hands = 5
            self.roll_dice()
            return True
        else:
            print("false i swear")
            return False
    # get info for gui

    def get_gui_data(self):
        self.gui_info = {"requirement": self.round_requirement, "total": self.total, "hands": self.max_hands,
                         "money": self.money, "played": self.played, "shop_dice": self.items_in_shop, "dice": self.dice, "round": self.round}
        return self.gui_info

    def add_dice(self, new_dice):
        self.new_dice = new_dice
        self.shop_dice = self.load_json("shop_dice.json")
        self.shop_dice[str(len(self.shop_dice))] = self.new_dice
        print(self.shop_dice)
        with open("shop_dice.json", "w") as file:
            json.dump(self.shop_dice, file, indent=4)
    # load json

    def load_json(self, json_file):
        try:
            with open(json_file, "r") as file:
                output = json.load(file)
        # If not found, fetch from GitHub
        except (FileNotFoundError, json.JSONDecodeError):
            with urllib.request.urlopen(self.github_path + json_file) as response:
                output = json.load(response)

            # Save locally for next time
            with open(json_file, "w") as file:
                json.dump(output, file, indent=4)
        return output
