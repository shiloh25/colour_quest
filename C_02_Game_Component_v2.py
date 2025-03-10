import csv
import random
from tkinter import *
from functools import partial # To prevent unwanted windows


# helper functions go here
def get_colours():
    # retrieve colours from csv file and put them in a list
    file = open("00_colour_list_hex_v3.csv", "r")
    all_colours = list(csv.reader(file, delimiter=","))
    file.close()

    # remove the first row
    all_colours.pop(0)

    return all_colours


def get_round_colours():
    """
    Choose four colours from larger list ensuring that the scores are all different
    :return: list of colours and score to beat (median of scores)
    """

    all_colour_list = get_colours()

    round_colours = []
    colour_scores = []

    # loop until we have four colours with different scores
    while len(round_colours) < 4:
        potential_colour = random.choice(all_colour_list)

        # Get the score and check it's not a duplicate
        if potential_colour[1] not in colour_scores:
            round_colours.append(potential_colour)
            colour_scores.append(potential_colour[1])

    # change scores to integers
    int_scores = [int(x) for x in colour_scores]
    int_scores.sort()

    median = (int_scores[1] + int_scores[2]) / 2
    median = round_ans(median)

    return round_colours, median


def round_ans(val):
    """
    rounds numbers to the nearest integer
    :param val: number to be rounded
    :return: rounded number (an integer)
    """
    var_rounded = (val * 2 + 1) // 2
    raw_rounded = "{:.0f}".format(var_rounded)
    return int(raw_rounded)


# classes start here
class StartGame:
    """
    Initial Game interface (asks users how many rounds they would like to play)
    """

    def __init__(self):
        """
        Gets number of rounds from user
        """

        self.start_frame = Frame(padx=10, pady=10)
        self.start_frame.grid()

        # create play button
        self.play_button = Button(self.start_frame, font=("Arial", "16", "bold"), fg="#FFFFFF",
                                  bg="#0057D8", text="Play", width=10, command=self.check_rounds)
        self.play_button.grid(row=0, column=1)

    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        Play(5)
        # ride root window (ie: hide rounds choice window)
        root.withdraw()


class Play:
    """
    Interface for playing the Colour Quest Game
    """

    def __init__(self, how_many):

        # integers / string variables
        self.target_score = IntVar()

        self.rounds_played = IntVar()
        self.rounds_played.set(0)

        self.rounds_wanted = IntVar()
        self.rounds_wanted.set(how_many)

        # colour lists and score list
        self.round_colour_list = []
        self.all_scores_list = []
        self.all_medians_list = []

        self.play_box = Toplevel()

        self.game_frame = Frame(self.play_box)
        self.game_frame.grid(pady=10, padx=10)

        # body font for most labels
        body_font = ("Arial", "12")

        # list for label details (text | font | background | row)
        play_labels_list = [
            ["Round # of #", ("Arial", "16", "bold"), None, 0],
            ["Score to beat: #", body_font, "#FFF2CC", 1],
            ["Choose a colour below. Good Luck.", body_font, "#D5E8D4", 2],
            ["You chose, result", body_font, "#D5E8D4", 4]
        ]

        play_labels_ref = []
        for item in play_labels_list:
            self.make_label = Label(self.game_frame, text=item[0], font=item[1], bg=item[2],
                                    wraplength=300, justify="left")
            self.make_label.grid(row=item[3], padx=10, pady=10)

            play_labels_ref.append(self.make_label)

        # retrieve labels so they can be configured later
        self.heading_label = play_labels_ref[0]
        self.target_label = play_labels_ref[1]
        self.results_label = play_labels_ref[3]

        # set up colour buttons...
        self.colour_frame = Frame(self.game_frame)
        self.colour_frame.grid(row=3)

        self.colour_button_ref = []
        self.colour_button_list = []

        # create four buttons in a 2 x 2 grid
        for item in range(0, 4):
            self.colour_button = Button(self.colour_frame, font=("Arial", "12"), text="Colour Name",
                                        width=15, command=partial(self.round_results, item))
            self.colour_button.grid(row=item // 2, column=item % 2, pady=5, padx=5)

            self.colour_button_ref.append(self.colour_button)

        # frame to hold hints and stats button
        self.hints_stats_frame = Frame(self.game_frame)
        self.hints_stats_frame.grid(row=6)

        # list for buttons (frame | text | bg | command | width | row | column
        control_button_list = [
            [self.game_frame, "Next Round", "#0057D8", "", 21, 5, None],
            [self.hints_stats_frame, "Hints", "#FF8000", "", 10, 0, 0],
            [self.hints_stats_frame, "Stats", "#333333", "", 10, 0, 1],
            [self.game_frame, "End", "#990000", self.close_play, 21, 7, None],
        ]

        # create buttons and add to list
        control_ref_list = []
        for item in control_button_list:
            make_control_button = Button(item[0], text=item[1], bg=item[2], command=item[3],
                                         font=("Arial", "16", "bold"), fg="#FFFFFF", width=item[4])
            make_control_button.grid(row=item[5], column=item[6], padx=5, pady=5)

            control_ref_list.append(make_control_button)

        # retrieve next, stats and end button so that they can be configured
        self.next_button = control_ref_list[0]
        self.stats_button = control_ref_list[2]
        self.end_game_button = control_ref_list[3]

        # once interface has been created, invoke new round function for first round
        self.new_round()


    def new_round(self):
        """
        Chooses four colours, works out median for score to beat. Configures buttons
        with chosen colours
        """

        # retrieve number of rounds played, add one to it and configure heading
        rounds_played = self.rounds_played.get()
        rounds_played += 1
        self.rounds_played.set(rounds_played)

        rounds_wanted = self.rounds_wanted.get()

        # get round colours and median score
        self.round_colour_list, median = get_round_colours()

        # set target score as median (for later comparison)
        self.target_score.set(median)

        # update heading and score to beat labels. 'Hide' results label
        self.heading_label.config(text=f"Round {rounds_played} of {rounds_wanted}")
        self.target_label.config(text=f"Target Score: {median}", font=("Arial", "14", "bold"))
        self.results_label.config(text=f"{'=' * 7}", bg="#F0F0F0")

        # configure buttons using foreground and background colours from list
        # enable colour buttons (disabled at end of last round)
        for count, item in enumerate(self.colour_button_ref):
            item.config(fg=self.round_colour_list[count][2], bg=self.round_colour_list[count][0],
                        text=self.round_colour_list[count][0], state=NORMAL)

        self.next_button.config(state=DISABLED)


    def round_results(self, user_choice):
        """
        Retrieves which button was pushed (index 0-3), retrieves score and then compare it
        with median, updates results and adds result to stats list
        """
        # get user score and colour based on button press...
        score = int(self.round_colour_list[user_choice][1])

        # alternate way to get button name, good for if buttons have been scrambled
        colour_name = self.colour_button_ref[user_choice].cget('text')

        # retrieve target score and compare with user score to find round result
        target = self.target_score.get()

        if score >= target:
            result_text = f"Success! {colour_name} earned you {score} points"
            result_bg = "#82B366"
        else:
            result_text = f"Oops {colour_name} ({score}) is less than the target"
            result_bg = "#F8CECC"

        self.results_label.config(text=result_text, bg=result_bg)

    def close_play(self):
        # reshow root (ie: close rounds) and end current
        # game / allow new game to start
        root.deiconify()
        self.play_box.destroy()


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
