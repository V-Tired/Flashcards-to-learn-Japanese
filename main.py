from tkinter import *
import pandas
import random

"""A GUI flashcard app to teach japanese. It removes the card from the list if you indicate you know it already."""

# Colors
MID = "#50B498"
LIGHT = "#DEF9C4"
DARK = "#468585"

card = {}
japanese_dictionary = {}

try:
    info = pandas.read_csv("Data/words_to_learn.csv")
except FileNotFoundError:
    original_info = pandas.read_csv("Data/common_words.csv")
    japanese_dictionary = original_info.to_dict(orient="records")
else:
    japanese_dictionary = info.to_dict(orient="records")


def do_know():
    """Updates the score when you know the card. Removes the card from the pool. Flips to next card."""
    japanese_dictionary.remove(card)
    next_card()
    data = pandas.DataFrame(japanese_dictionary)
    data.to_csv("data/words_to_learn.csv", index=False)
    print(len(japanese_dictionary))


def flip_card():
    canvas.itemconfig(words, text=card['translation'])


def next_card():
    """Picks a random english word and finds the corresponding japanese info to show. Flips after 7 seconds."""
    global card, timer
    num_words.config(text=f"Words to Learn\n{len(japanese_dictionary)}")
    window.after_cancel(timer)
    card = random.choice(japanese_dictionary)
    japanese = card['japanese']
    romaji = card['pronunciation']
    canvas.itemconfig(words, text=f"{japanese}\n{romaji}")
    timer = window.after(7000, flip_card)


#Window and Canvas
window = Tk()
window.config(height=200, width=100, bg=DARK, pady=25, padx=25)
window.minsize(200, 100)
canvas = Canvas(width=400, height=300, bg=DARK, highlightthickness=0)
img = PhotoImage(file="Images/card_front.png")
img = img.subsample(2)
canvas.create_image(200, 150, image=img)
canvas.grid(column=1, row=1, columnspan=2)

# Buttons
circle = PhotoImage(file="Images/Check.png")
check = Button(command=do_know, image=circle, highlightthickness=0, bg="white")
check.grid(column=2, row=2)
big_x = PhotoImage(file="Images/X.png")
x = Button(command=next_card, image=big_x, highlightthickness=0, bg="white")
x.grid(column=1, row=2)

# Labels
num_words = Label(text=f"Words to Learn\n{len(japanese_dictionary)}", bg=DARK, fg=LIGHT, font=("futura", 18, "bold"))
num_words.grid(column=1, row=0, columnspan=3)

words = canvas.create_text(200, 150, text="", font=("futura", 18, "bold"))

timer = window.after(7000, flip_card)
next_card()


window.mainloop()


