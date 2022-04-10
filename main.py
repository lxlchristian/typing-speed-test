from tkinter import *
from random import choices
from words import words

WORDS_N = 4
ROWS_N = 5
TIME_LIMIT = 60
start = 0
nth_word = 0
nth_row = 0
shown_words = [choices(words, k=WORDS_N) for i in range(ROWS_N)]
row_words = []
canvas_words = []
correct_count = 0
wrong_count = 0
finish = 0
cpm = 0


def click_temp(*args):
    global start
    entry.delete(0, "end")
    entry.config(fg="black", font=CANVAS_FONT)
    if start == 0:
        display_words()
        start = 1
        count_down(TIME_LIMIT)

    if finish == 1:
        entry.delete(0, "end")
        restart()


def display_words():
    for j in range(ROWS_N):
        for i in range(WORDS_N):
            canvas.itemconfig(canvas_words[j][i], text=shown_words[j][i])
            if j == nth_row and i == nth_word:
                canvas.itemconfig(canvas_words[nth_row][nth_word], fill=BG_COLOR)

            elif j >= nth_row and i > nth_word:
                canvas.itemconfig(canvas_words[j][i], fill=TEXT_COLOR)


def update_words():
    global shown_words
    shown_words = [choices(words, k=WORDS_N) for i in range(ROWS_N)]
    display_words()


def check(*args):
    global correct_count, wrong_count, nth_word, nth_row

    if start == 1:
        if entry.get() == shown_words[nth_row][nth_word]:
            entry.config(fg=CORRECT_COLOR)

        elif entry.get() == shown_words[nth_row][nth_word][:len(entry.get())]:
            entry.config(fg="#000")

        else:
            entry.config(fg=WRONG_COLOR)

        if finish == 0 and " " in entry.get():
            if entry.get() == shown_words[nth_row][nth_word] + " ":
                canvas.itemconfig(canvas_words[nth_row][nth_word], fill=CORRECT_COLOR)
                correct_count += len(entry.get()) + 1

            else:
                canvas.itemconfig(canvas_words[nth_row][nth_word], fill=WRONG_COLOR)
                wrong_count += len(shown_words[nth_row][nth_word])

            entry.delete(0, "end")

            nth_word += 1
            if nth_word == WORDS_N:
                nth_word = 0
                nth_row += 1

                if nth_row == ROWS_N:
                    nth_row = 0
                    update_words()
                    for j in range(ROWS_N):
                        for i in range(WORDS_N):
                            canvas.itemconfig(canvas_words[j][i], fill=TEXT_COLOR)

            display_words()


def count_down(count):
    global cpm, finish
    countdown.config(text=f"Time: {count}")

    if count < TIME_LIMIT:
        cpm = int(round(correct_count / (TIME_LIMIT - count) * 60))
        full_cpm = int(round((correct_count + wrong_count) / (TIME_LIMIT - count) * 60))
        cpm_label.config(text=f"Characters per minute: {cpm}")

    if count > 0:
        screen.after(1000, count_down, count - 1)

    else:
        finish = 1
        entry.delete(0, "end")
        entry.config(font=TEMP_FONT, fg=HEADER_COLOR)
        entry.insert(0, "click here to try again")
        popup_text_1 = f"Final typing speed: {cpm} characters per minute"
        if wrong_count != 0:
            popup_text_2 = f"You got {wrong_count} characters wrong. If you had typed them correctly, your typing speed would be {full_cpm} characters per minute."

        else:
            popup_text_2 = f"You typed every word correctly. Great job!"

        screen.focus()
        popup = Toplevel(screen)
        popup.config(width=550, height=80, padx=50, pady=30, bg=HEADER_COLOR)
        popup.title("Time's Up!")
        Label(popup, text=popup_text_1, fg=TEXT_COLOR, bg=HEADER_COLOR, font=POPUP_FONT).pack()
        Label(popup, text=popup_text_2, fg=TEXT_COLOR, bg=HEADER_COLOR, font=POPUP_FONT, wraplength=350).pack()
        Button(popup, text="OK", width=10, font=POPUP_FONT, highlightbackground=HEADER_COLOR, command=popup.destroy).pack(pady=20)


def restart():
    global start, nth_word, nth_row, shown_words, cpm, correct_count, wrong_count, finish
    start = 0
    nth_word = 0
    nth_row = 0
    shown_words = [choices(words, k=WORDS_N) for i in range(ROWS_N)]
    correct_count = 0
    wrong_count = 0
    finish = 0
    cpm = 0

    update_words()

    for j in range(ROWS_N):
        for i in range(WORDS_N):
            canvas.itemconfig(canvas_words[j][i], fill=TEXT_COLOR)

    click_temp()


# -------- UI --------
BG_COLOR = "#233142"
HEADER_COLOR = "#F95959"
HEADER_FONT = ("Didot", "60", "bold italic")
CANVAS_HEIGHT = 350
CANVAS_WIDTH = 800
CANVAS_COLOR = "#455D7A"
CANVAS_FONT = ("Futura", "32", "normal")
TEXT_COLOR = "#E3E3E3"
CORRECT_COLOR = "#50CB86"
WRONG_COLOR = "#F95959"
TEMP_FONT = ("Futura", "32", "italic")
COUNTER_FONT = ("Didot", "26", "bold")
POPUP_FONT = ("Futura", "14", "normal")

screen = Tk()
screen.title("Typing Speed Test")
screen.config(bg=BG_COLOR, padx=20, pady=20)

# Logo
logo = Label(text="Typing Speed Test", font=HEADER_FONT, bg=BG_COLOR, fg=HEADER_COLOR)
logo.grid(row=0, column=0, columnspan=2, pady=20)

# Canvas
canvas = Canvas(height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg=CANVAS_COLOR, highlightbackground=HEADER_COLOR, bd=-2)

for m in range(ROWS_N):
    for n in range(WORDS_N):
        row_words.append(canvas.create_text(26 + CANVAS_WIDTH * n / WORDS_N,
                                            17 + CANVAS_HEIGHT * m / (ROWS_N + 1),
                                            anchor="nw",
                                            text=shown_words[m][n],
                                            font=CANVAS_FONT,
                                            fill=TEXT_COLOR,
                                            justify="center"))

    canvas_words.append(row_words)
    row_words = []

# Entry
sv = StringVar()
sv.trace("w", check)
entry = Entry(font=TEMP_FONT, fg=HEADER_COLOR, bg=TEXT_COLOR, justify="center", highlightbackground=HEADER_COLOR, textvariable=sv)
entry.insert(0, "type here to begin")
entry.bind("<FocusIn>", click_temp)
canvas_entry = canvas.create_window(0, CANVAS_HEIGHT*0.9, anchor="nw", width=CANVAS_WIDTH+1.5, window=entry)
canvas.grid(row=2, column=0, columnspan=2, pady=40, padx=50)

# Timer
countdown = Label(text=f"Time: {TIME_LIMIT}", bg=BG_COLOR, fg=TEXT_COLOR, font=COUNTER_FONT)
countdown.grid(row=1, column=0)

# CPM Label
cpm_label = Label(text=f"Characters per minute: 0  ", bg=BG_COLOR, fg=TEXT_COLOR, font=COUNTER_FONT)
cpm_label.grid(row=1, column=1)

screen.mainloop()
