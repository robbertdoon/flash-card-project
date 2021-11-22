from tkinter import *
from tkinter import messagebox
import random
import pandas
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# ---------------------- Read data ---------------------- #

try:
    with open('data/words_to_learn.csv') as data_file:
        data = pandas.read_csv(data_file)
except FileNotFoundError:
    with open('data/french_words.csv') as data_file:
        data = pandas.read_csv(data_file)
finally:
    to_learn = data.to_dict(orient='records')


def is_known():
    try:
        to_learn.remove(current_card)
    except ValueError:
        print('to_learn dictionary is empty')
    else:
        with open('data/words_to_learn.csv', 'w') as data_file2:
            df = pandas.DataFrame(to_learn)
            df.to_csv(data_file2, index=False)

    try:
        next_card()
    except IndexError:
        no_more_cards()


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)

    try:
        current_card = random.choice(to_learn)
    except IndexError:
        no_more_cards()

    canvas.itemconfig(card_background, image=card_front_img)
    canvas.itemconfig(card_title, text='French', fill="black")
    canvas.itemconfig(card_word, text=current_card['French'],  fill="black")
    flip_timer = window.after(3000, flip_card)


def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text='English', fill="white")
    canvas.itemconfig(card_word, text=current_card['English'], fill="white", )


def no_more_cards():
    messagebox.showinfo(title='Mission accomplished! ', message='There are no more words to learn!')

# ---------------------- User Interface ---------------------- #


window = Tk()
window.title('Flashy')
window.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, flip_card)

card_front_img = PhotoImage(file='images/card_front.png')
card_back_img = PhotoImage(file='images/card_back.png')

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_background = canvas.create_image(400, 263)
card_title = canvas.create_text(400, 150, font=('Ariel', 40, 'italic'))
card_word = canvas.create_text(400, 263, font=('Ariel', 60, 'bold'))
canvas.grid(column=0, row=0, columnspan=2)

wrong_button_img = PhotoImage(file='images/wrong.png')
wrong_button = Button(image=wrong_button_img, highlightthickness=0, command=next_card)
wrong_button.grid(column=0, row=1)

right_button_img = PhotoImage(file='images/right.png')
right_button = Button(image=right_button_img, highlightthickness=0, command=is_known)
right_button.grid(column=1, row=1)

next_card()

window.mainloop()