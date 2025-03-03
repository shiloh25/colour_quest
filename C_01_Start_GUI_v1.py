from tkinter import *
from functools import partial # To prevent unwanted windows

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

        # strings for labels
        intro_string = ("In each round you will be invited to choose a colour. your goal is "
                        "to beat the target score and win the round (and keep your points)")

        # choose string = "Oops - Please choose a whole number more then zero."
        choose_string = "How many rounds do you want to play"

        # List of labels to be made (text | font | fg)
        start_labels_list = [
            ["Colour Quest", ("Arial", "16", "bold"), None],
            [intro_string, ("Arial", "12", "bold"), None],
            [choose_string, ("Arial", "12", "bold"), "#009900"]
        ]

        # create labels and add them to the reference list...

        start_label_ref = []
        for count, item in enumerate(start_labels_list):
            make_label = Label(self.start_frame, text=item[0], font=item[1], fg=item[2],
                               wraplength=350, justify="left", pady=10, padx=20)
            make_label.grid(row=count)

            start_label_ref.append(make_label)

        # extract choice label so that it can ne changed to an error message if necessary
        self.choose_label = start_label_ref[2]

        # frame so that entry box and button can be in the same row
        self.entry_area_frame = Frame(self.start_frame)
        self.entry_area_frame.grid(row=3)

        self.num_rounds_entry = Entry(self.entry_area_frame, font=("Arial", "20", "bold"),
                                      width=10)
        self.num_rounds_entry.grid(row=0, column=0, padx=10, pady=10)

        # create play button
        self.play_button = Button(self.entry_area_frame, font=("Arial", "16", "bold"),
                                  fg="#FFFFFF", bg="#0057D8", text="Play", width=10,
                                  command=self.check_rounds)
        self.play_button.grid(row=0, column=1)


    def check_rounds(self):
        """
        Checks users have entered 1 or more rounds
        """

        rounds_wanted = self.num_rounds_entry.get()

        # Reset label and entry box (for when users come back to the home screen)
        self.choose_label.config(fg="#009900", font=("Arial", "12", "bold"))
        self.num_rounds_entry.config(bg="#FFFFFF")

        error = "Oops - Please choose a whole number more than zero"
        has_errors = "no"

        # checks that amount to be converted is a number above absolute zero
        try:
            rounds_wanted = int(rounds_wanted)
            if rounds_wanted > 0:
                # temporary success message, replace with call to PlayGame class
                self.choose_label.config(text=f"You have chosen to play {rounds_wanted} rounds")
            else:
                has_errors = "yes"

        except ValueError:
            has_errors = "yes"

        # display the error if necessary
            if has_errors == "yes":
                self.choose_label.config(text=error, fg="#990099", font=("Arial", "10", "bold"))
                self.num_rounds_entry.config(bg="#F4CCCC")
                self.num_rounds_entry.delete(0, END)


# main routine
if __name__ == "__main__":
    root = Tk()
    root.title("Colour Quest")
    StartGame()
    root.mainloop()
