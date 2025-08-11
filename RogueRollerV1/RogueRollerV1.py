from tkinter import *
import json
import random

class Round():
    def __init__(self):
        self.played = [0,0,0,0,0,0]

        self.root = Tk()
        self.root.title("Rogue Roller")
        self.root.grid()
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.root.state('zoomed')#open window in fullscreen

        self.container = Frame(self.root)
        self.container.grid(row = 0, column = 0, sticky = "nsew")
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.button_colour = "#B6AADD"
        self.bg_colour = "#746aff"
        self.sidebar_colour = "#46444D"
        self.sidebar_box_colour = "#5A5A6D"
        self.sidebar_text = "#FFFFFF"

        self.font = "Cascadia-code  12"
        self.large_font = "Copperplate_Gothic 30"

        self.frames = {}
        self.frames["MainMenu"] = self.menu()
        self.frames["ShopMenu"] = self.shop()
        self.frames["GameMenu"] = self.game()

        self.font = "Arial 16"
        self.large_font = "Arial 30"

        

        #Declare values
        self.dice_locked = {"die1": False, "die2": False, "die3": False, "die4": False, "die5": False, "die6": False}
        with open("dice.json", "r") as file: 
            self.dice = json.load(file)
        
        
        self.max_rounds = 5
        self.round = 0
        self.show_frames("MainMenu")
        while self.round < self.max_rounds:
            self.round += 1
            self.dice_score = {}
            self.played = []
            self.total = 0
            self.max_hands = 5
            self.roll_dice()
        
    
    def show_frames(self, container):
        frame = self.frames[container]
        frame.tkraise()

    def menu(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.bg_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        self.title_label = Label(frame, font =self.large_font, text = "Rogue Roller", bg=self.bg_colour)
        self.title_label.grid(padx=1, pady=150,sticky = NSEW)

        self.game_button = Button(frame, text="New Game", bg=self.button_colour, font=self.font, command=lambda: self.show_frames("GameMenu"))
        self.game_button.grid(padx=350, pady=10, sticky=NSEW)

        self.quit_button = Button(frame, text="Quit", bg=self.button_colour, font=self.font, command=self.quit)
        self.quit_button.grid(padx=350, pady=10, sticky=NSEW)

        return frame
    
    def shop(self):
        frame = Frame(self.container)
        return frame
    
    def game(self):
        frame = Frame(self.container)
        frame.grid(row=0, column=0, sticky="nsew")

        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(0, weight=1)

        sidebar_frame = self.sidebar(frame)
        sidebar_frame.grid(row=0, column=0, sticky="nsew")

        game_frame = self.game_content(frame)
        game_frame.grid(row=0, column=1, sticky="nsew")

        return frame
    
    def sidebar(self, master):
        frame = Frame(master, width=600)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.configure(bg=self.sidebar_colour)

        frame.rowconfigure(list(range(12)), weight = 1)
        frame.columnconfigure(0, weight = 1)

        ####### PLACEHOLDERS #######
        self.round_requirement = 300 
        self.score = 1000
        self.mult = 1
        self.total = 1000
        self.hands = 4 

        self.requirement_label = Label(frame, font = self.font, text = f"Requirement: {self.round_requirement}", bg=self.sidebar_colour, fg=self.sidebar_text)
        self.requirement_label.grid(padx=100, pady=10, sticky=EW)

        self.total_label = Label(frame, font = self.font, text = f"Total: {self.total}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.total_label.grid(padx=75, pady=5, sticky=EW)

        self.scoring_label = Label(frame, font = self.font, text = f"{self.score} X {self.mult}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.scoring_label.grid(padx=75, pady=5, sticky=EW)

        self.scoring_label = Label(frame, font = self.font, text = f"Remaining Hands: {self.hands}", bg=self.sidebar_box_colour, fg=self.sidebar_text)
        self.scoring_label.grid(padx=75, pady=5, sticky=EW)

        self.menu_button = Button(frame, text="Menu", bg=self.sidebar_box_colour, fg=self.sidebar_text, font=self.font, command=lambda: self.show_frames("MainMenu"))
        self.menu_button.grid(padx=75, pady=15, sticky=EW)

        return frame
    
    def game_content(self, master):
        frame = Frame(master)
        frame.configure(bg=self.bg_colour)

        frame.grid(row=0, column=1, sticky="nsew")
        frame.rowconfigure(list(range(4)), weight=1)
        frame.columnconfigure(list(range(3)), weight=1)
        
        self.dice_image = PhotoImage(file="green_dice1.png")

        self.dice_buttons = []

        for x in range(3):
            for y in range(2):
                print(x*2 + y + 1)
                self.dice_button = Button(frame, image=self.dice_image, text=self.played[x*2 + y], bg="black", font=self.large_font, compound=CENTER, borderwidth=0, command=lambda value=(x*2 + y + 1): self.lock_dice(value))
                self.dice_button.grid(row=x, column=y, padx=100)
                self.dice_buttons.append(self.dice_button)
        
        play_button = Button(frame, text="Play Hand", bg=self.button_colour, font=self.large_font, compound=CENTER, borderwidth=0, command=lambda: self.roll_dice())
        play_button.grid(row=1, column=2)
        
        return frame
    
    def run(self):
        self.root.mainloop()
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
        if self.dice_locked[dice] == False:
            self.dice_locked[dice] = True
        else:
            self.dice_locked[dice] = False
        print(f"Die {die_number} locked: {self.dice_locked[dice]}")

    #rolls the dice
    def roll_dice(self):
        if self.max_hands > 0:
            #rolls the unlocked dice
            for i in range(len(self.dice_locked)):
                if self.dice_locked[f"die{i+1}"]:
                    continue  # Skip locked dice
                value = random.choice(self.dice[f"die{i+1}"]["sides"])
                self.dice_score[f"die{i+1}"] = value
            self.played = list(self.dice_score.values())
            print(self.played)

            for i in range(len(self.dice_buttons)):
                self.button_update = self.dice_buttons[i]
                self.button_update.config(text=self.played[i])
            
            self.max_hands -= 1
            print(self.max_hands)
        if self.max_hands == 0:
            self.requirement()



    
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
        self.round_requirement = round_data["Round" + str(self.round)]["Requirement"]
        if self.total >= self.round_requirement:
            self.win = True
            print("win")
        else:
            self.win = False
            print("lose")
        return self.win

GAME_RUNNING = Round()
GAME_RUNNING.run()