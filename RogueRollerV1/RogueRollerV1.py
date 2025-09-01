#Version 1
#Rogue roller is a roguelike yahtzee game
#Version 1: There is dice rolling, locking, scoring, game rounds
#and a dice shop to buy new dice
from tkinter import *
import json
import random

class Round():
    def __init__(self):
        #Declare needed variables
        self.max_hands = 5
        self.played = [0,0,0,0,0,0]
        
        #start the gui
        self.root = Tk()
        self.root.title("Rogue Roller")
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        #set money using stringvar
        self.money = 0
        self.money_var = StringVar()
        self.money_var.set(f"Money: {self.money}")

        #load images
        self.dice_image = PhotoImage(file="green_dice1.png")
        self.locked_dice_image = PhotoImage(file="green_dice_locked1.png")
        self.shop_dice_image = self.dice_image.subsample(2)

        #open window in fullscreen
        self.root.state('zoomed')

        #declare colours and fonts
        self.button_colour = "#B6AADD"
        self.bg_colour = "#746aff"
        self.sidebar_colour = "#46444D"
        self.sidebar_box_colour = "#5A5A6D"
        self.sidebar_text = "#FFFFFF"

        self.font = "Cascadia-code  12"
        self.large_font = "Copperplate_Gothic 30"

        #create the containter
        self.container = Frame(self.root)
        self.container.grid(row=0, column=0, sticky="nsew")
        self.container.rowconfigure(0, weight=1)
        #make a column for the sidebar and main content
        self.container.columnconfigure(0, weight=0)
        self.container.columnconfigure(1, weight=1)

        #make the sidebar and put it in the first column of the container
        self.sidebar_frame = self.sidebar(self.container)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")

        #declare used frames
        self.frames = {}
        self.frames["MainMenu"] = self.menu()
        self.frames["ShopMenu"] = self.shop()
        self.frames["GameMenu"] = self.game()
        self.frames["LossScreen"] = self.game_lose()
        self.frames["ReplaceDice"] = self.replace_dice()

        self.font = "Arial 16"
        self.large_font = "Arial 30"

        self.show_frames("MainMenu")
        self.max_rounds = 5
        self.round = 0
    #set up the show frame function
    def show_frames(self, container):

        for frame_name, frame_instance in self.frames.items():
            #hide all frames
            frame_instance.grid_remove()

        #make the correct frame
        frame_to_show = self.frames[container]

        if container in ["MainMenu", "LossScreen"]:
            #for the menus we hide the sidebar and show only the menu
            self.sidebar_frame.grid_remove()
            frame_to_show.grid(row=0, column=0, sticky="nsew", columnspan=2)
            frame_to_show.tkraise()
        else:
            #anythinhg else shows the sidebar and content
            self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
            frame_to_show.grid(row=0, column=1, sticky="nsew")
            frame_to_show.tkraise()
    #create the main menu
    def menu(self):
        frame = Frame(self.container)
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        self.title_label = Label(frame, font =self.large_font, text = "Rogue Roller", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font=self.font, command=lambda: [self.game_reset(), self.show_frames("GameMenu")])
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font=self.font, command=self.quit)
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    #make the shop menu
    def shop(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)

        dice_frame = self.current_dice(frame)
        dice_frame.grid(row=0, column=1, sticky="nsew")

        shop_frame = self.shop_content(frame)
        shop_frame.grid(row=1, column=1, sticky="nsew")

        return frame
    #make the game menu
    def game(self):
        self.update_sidebar()
        #Declare values
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)

        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        game_frame = self.game_content(frame)
        game_frame.grid(row=0, column=1, sticky="nsew")

        return frame
    #make the game over menu
    def game_lose(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        self.title_label = Label(frame, font =self.large_font, text = "Game Over", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font=self.font, command=lambda: [self.game_reset(), self.show_frames("GameMenu")])
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font=self.font, command=self.quit)
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    #make the sidebar
    def sidebar(self, master):
        frame = Frame(master, width=600)
        frame.configure(bg=self.sidebar_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        ####### PLACEHOLDERS #######
        self.score = 0
        self.mult = 0
        self.round_requirement = 0
        self.total = 0

        #make the labels for the sidebar
        self.requirement_label = Label(frame, font = self.font, text = f"Requirement: {self.round_requirement}", bg=self.sidebar_colour, fg=self.sidebar_text)
        self.requirement_label.grid(padx=100, pady=10, sticky=EW)

        self.total_label = Label(frame, font = self.font, text = f"Total: {self.total}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.total_label.grid(padx=75, pady=5, sticky=EW)

        self.scoring_label = Label(frame, font = self.font, text = f"Remaining Hands: {self.max_hands}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.scoring_label.grid(padx=75, pady=5, sticky=EW)

        self.money_label = Label(frame, font=self.font, textvariable=self.money_var, bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.money_label.grid(padx=75, pady=5, sticky=EW)

        self.menu_button = Button(frame, text="Menu", bg=self.sidebar_box_colour, fg=self.sidebar_text, font=self.font, command=lambda: self.show_frames("MainMenu"))
        self.menu_button.grid(padx=75, pady=15, sticky=EW)

        

        return frame
    #content of the game menu
    def game_content(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(3)), weight=1)

        self.dice_buttons = []

        #make the dice in a 2x3 grid
        for y in range(2):
            for x in range(3):
                print(x +1 + y*3)
                self.dice_button = Button(frame, image=self.dice_image, text=self.played[x*2 + y], bg="black", font=self.large_font, compound=CENTER, borderwidth=0, command=lambda value=(x +1 + y*3): self.lock_dice(value))
                self.dice_button.grid(row=y, column=x, padx=100)
                self.dice_buttons.append(self.dice_button)
        
        play_button = Button(frame, text="Play Hand", bg=self.button_colour, font=self.large_font, compound=CENTER, borderwidth=0, command=self.play_hand)
        play_button.grid(row=2, column=1)
        
        return frame
    #current dice for the shop menu
    def current_dice(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(7)), weight=1)

        self.current_dice_label = Label(frame, font =self.large_font, text = "Current Dice", bg=self.bg_colour)
        self.current_dice_label.grid(padx=1, pady=15,sticky = NSEW, row=0, columnspan=7)

        #make the current dice in a line
        for x in range(6):
                self.dice_button = Button(frame, image=self.shop_dice_image, text= f"Dice {x + 1}", bg="black", font=self.font, compound=CENTER, borderwidth=0)
                self.dice_button.grid(column=x, row=1, padx=10)
        return frame
    #play the current hand
    def play_hand(self):
        print(f"requirement {self.round_requirement}")
        print(f"round {self.round}")
        self.roll_dice()
        self.calculate_score()
        self.max_hands -= 1 
        self.update_sidebar() 
        
        if self.max_hands <= 0:
            self.requirement()
            self.update_sidebar() 
    #makes the content for the new dice in the shop
    def shop_content(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(7)), weight=1)
        
        self.shop_label = Label(frame, font =self.large_font, text = "Shop", bg=self.bg_colour)
        self.shop_label.grid(padx=1, pady=15,sticky = NSEW, row=2, columnspan=7)

        #load the shop dice from the json
        with open("shop_dice.json", "r") as file:
            self.shop_dice = json.load(file)
            self.items_in_shop = []
        #pick 2 random dice for the shop
        for i in range(2):
            self.items_in_shop.append(self.shop_dice[str(random.randint(0, len(self.shop_dice) - 1))])
            print(self.items_in_shop)

        #make the buttons for the dice in shop
        self.shop_dice_buttons = []
        for i in range(len(self.items_in_shop)):
            self.shop_dice_button = Button(frame, text=f"{self.items_in_shop[i]['name']} \nCost: {self.items_in_shop[i]['cost']}", bg="black", font=self.font, compound=CENTER, borderwidth=0,image=self.dice_image, command = lambda value=i: self.check_price(value))
            self.shop_dice_button.grid(row=3, column=i, padx=10)
            self.shop_dice_buttons.append(self.shop_dice_button)

        self.next_round_button = Button(frame, text="Next Round", bg=self.button_colour, font=self.large_font, command=lambda: self.next_round())
        self.next_round_button.grid(row=3, column=3, padx=10, pady=10)

        return frame       
    #get new dice for the shop
    def new_shop_dice(self):
        #load json and pick 2 new random dice
        with open("shop_dice.json", "r") as file:
            self.shop_dice = json.load(file)
            self.items_in_shop = []
        for i in range(2):
            self.items_in_shop.append(self.shop_dice[str(random.randint(0, len(self.shop_dice) - 1))])
        print(self.items_in_shop)

        #update buttons and costs
        self.dice_costs = []
        for i in range(len(self.shop_dice_buttons)):
            self.dice_costs.append(self.items_in_shop[i]['cost'])
            self.button_to_update = self.shop_dice_buttons[i]
            self.button_to_update.config(text=f"{self.items_in_shop[i]['name']} \nCost: {self.items_in_shop[i]['cost']}")
        print(self.dice_costs)
    #checks if the user has enough money for new dice
    def check_price(self, position):
        self.dice_pos = position
        if int(self.money_var.get().split(" ")[1]) >= self.dice_costs[self.dice_pos]:
            self.show_frames("ReplaceDice")
        else:
            print("not enough money")
    #pick a dice to replace for new dice
    def replace_dice(self):
        frame = Frame(self.container)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(3)), weight=1)
        frame.columnconfigure(list(range(2)), weight=1)
        
        self.current_dice_label = Label(frame, font =self.large_font, text = "Select a dice to replace", bg=self.bg_colour)
        self.current_dice_label.grid(padx=1, pady=15,sticky = NSEW, row=0, columnspan=7)

        #display current dice in a 2x3 grid
        for y in range(2):
            for x in range(3):
                die = "die" + str(x +1 + y*3)
                dice = self.dice[die]
                faces = dice["sides"]
                self.dice_button = Button(frame, image=self.dice_image, text= f"Dice {x +1 + y*3} \nFaces: {faces}", bg="black", font=self.font, compound=CENTER, borderwidth=0, wraplength=150, justify=CENTER, command = lambda value=(x +1 + y*3): self.dice_change(value))
                self.dice_button.grid(row=y+1, column=x, padx=100)

        return frame
    #replace current dice with shop dice
    def dice_change(self, dice_number):
        self.dice_to_replace = "die" + str(dice_number)
        self.dice[self.dice_to_replace] = self.items_in_shop[self.dice_pos]
        print(self.dice)
        self.show_frames("ShopMenu")
    #run the game
    def run(self):
        self.root.mainloop()
    #end the game
    def quit(self):
        self.root.destroy()
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
            self.button_update = self.dice_buttons[die_number -1]
            self.button_update.config(image=self.locked_dice_image)
        #if locked unlock dice and change image
        else:
            self.dice_locked[dice] = False
            self.button_update = self.dice_buttons[die_number -1]
            self.button_update.config(image=self.dice_image)
        print(f"Die {die_number} locked: {self.dice_locked[dice]}")
    #rolls the dice
    def roll_dice(self):
        for i in range(len(self.dice_locked)):
            # Skip locked dice
            if self.dice_locked[f"die{i+1}"]:
                continue  
            value = random.choice(self.dice[f"die{i+1}"]["sides"])
            self.dice_score[f"die{i+1}"] = value
        
        self.played = list(self.dice_score.values())

        #update the dice
        for i in range(len(self.dice_buttons)):
            self.button_update = self.dice_buttons[i]
            self.button_update.config(text=self.played[i])
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
            current_money = int(self.money_var.get().split(" ")[1])
            new_money = current_money + payout
            self.money_var.set(f"Money: {new_money}")
            self.new_shop_dice()
            self.show_frames("ShopMenu")
        else:
            self.win = False
            self.show_frames("LossScreen")
        return self.win
    #reset all the values for new game
    def game_reset(self):
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)
        self.dice_locked = {"die1": True, "die2": True, "die3": True, "die4": True, "die5": True, "die6": True}
        for i in range(len(self.dice_locked)):
            self.lock_dice(i + 1)
        self.total = 0
        self.round = 0
        self.round += 1
        with open("round.json", "r") as file: 
            round_data = json.load(file)
        self.round_requirement = round_data["Round" + str(self.round)]["Requirement"]
        self.dice_score = {}
        self.played = []
        self.max_hands = 5
        self.roll_dice()
        self.money = 0
        self.money_var.set(f"Money: {self.money}")
        self.update_sidebar()
    #updates the sidebar with new values
    def update_sidebar(self):
        self.requirement_label.config(text=f"Requirement: {self.round_requirement}")
        self.total_label.config(text=f"Total: {self.total}")
        self.scoring_label.config(text=f"Remaining Hands: {self.max_hands}")
        self.money_label.config(text=f"Money: {self.money}")
        
    def next_round(self):
        self.round += 1
        with open("round.json", "r") as file: 
            round_data = json.load(file)
        self.round_requirement = round_data["Round" + str(self.round)]["Requirement"]
        self.dice_locked = {"die1": True, "die2": True, "die3": True, "die4": True, "die5": True, "die6": True}
        for i in range(len(self.dice_locked)):
            self.lock_dice(i + 1)
        self.total = 0
        self.dice_score = {}
        self.played = []
        self.max_hands = 5
        self.roll_dice()
        self.show_frames("GameMenu")
        self.update_sidebar()
#run the game
game = Round()

game.run()
