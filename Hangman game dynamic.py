import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Words and hints for different categories
categories = {
    "movies": {
        "INCEPTION": "A movie about dreams within dreams.",
        "TITANIC": "A tragic love story set on a ship.",
        "AVATAR": "A sci-fi movie set on the planet Pandora.",
        "GLADIATOR": "A story of a Roman general turned gladiator.",
        "COCO": "An animated movie celebrating the Day of the Dead."
    },
    "songs": {
        "IMAGINE": "A famous song by John Lennon.",
        "THRILLER": "A classic Michael Jackson hit.",
        "HELLO": "A hit ballad by Adele.",
        "BOHEMIAN": "A song by Queen with 'Rhapsody' in its title.",
        "HERO": "A song by Enrique Iglesias."
    },
    "actors": {
        "LEONARDO DICAPRIO": "Famous actor known for 'Titanic' and 'Inception'.",
        "MORGAN FREEMAN": "Known for his iconic voice and movies like 'Shawshank Redemption'.",
        "TOM HANKS": "Star of 'Forrest Gump' and 'Saving Private Ryan'.",
        "ROBERT DOWNEY JR.": "Famous for playing Iron Man in the 'Avengers' franchise.",
        "WILL SMITH": "Famous actor known for 'Men in Black' and 'The Pursuit of Happyness'."
    },
    "actresses": {
        "MERYL STREEP": "One of the most celebrated actresses, known for 'The Devil Wears Prada'.",
        "ANGELINA JOLIE": "Known for 'Maleficent' and humanitarian work.",
        "EMMA STONE": "Oscar-winning actress known for 'La La Land'.",
        "JENNIFER LAWRENCE": "Famous for 'The Hunger Games' series.",
        "SCARLETT JOHANSSON": "Famous for playing Black Widow in the Marvel Cinematic Universe."
    },
    "countries": {
        "NEPAL": "Known for the Himalayas and Mount Everest.",
        "FRANCE": "Famous for the Eiffel Tower and French cuisine.",
        "JAPAN": "Known for technology and its unique culture.",
        "BRAZIL": "Famous for its Carnival and the Amazon rainforest.",
        "CANADA": "Known for its vast wilderness and multicultural cities."
    }
}

# Function to select a category
def select_category():
    category = simpledialog.askstring(
        "Category Selection", 
        "Please choose a category: movies, songs, actors, actresses, or countries",
        parent=root
    )
    if not category or category.lower() not in categories:
        messagebox.showerror("Invalid Category", "Please choose a valid category: 'movies', 'songs', 'actors', 'actresses', or 'countries'.")
        return None
    return category.lower()

# Initialize game variables
root = tk.Tk()
root.withdraw()  # Hide the main window for now

category = select_category()
if not category:
    exit()

def start_new_word():
    global selected_word, hint, display_word, guessed_letters, remaining_attempts
    selected_word, hint = random.choice(list(categories[category].items()))
    display_word = ["_"] * len(selected_word)
    guessed_letters.clear()
    remaining_attempts = max_attempts

    word_label.config(text=" ".join(display_word))
    hint_label.config(text=f"Hint: {hint}")
    attempts_label.config(text=f"Attempts Remaining: {remaining_attempts}")
    guessed_letters_label.config(text="Guessed Letters: ")
    draw_hangman(max_attempts)

# Game variables
max_attempts = 6
remaining_attempts = max_attempts
selected_word, hint = random.choice(list(categories[category].items()))
display_word = ["_"] * len(selected_word)
guessed_letters = set()

# GUI setup
root.deiconify()  # Show the main window
root.title("Hangman Game")

canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

word_label = tk.Label(root, text=" ".join(display_word), font=("Arial", 20))
word_label.pack(pady=10)

hint_label = tk.Label(root, text=f"Hint: {hint}", font=("Arial", 14), fg="blue")
hint_label.pack(pady=5)

entry = tk.Entry(root, font=("Arial", 16), justify="center")
entry.pack()

attempts_label = tk.Label(root, text=f"Attempts Remaining: {remaining_attempts}", font=("Arial", 14))
attempts_label.pack()

# Label for displaying guessed letters
guessed_letters_label = tk.Label(root, text="Guessed Letters: ", font=("Arial", 12), fg="gray")
guessed_letters_label.pack(pady=5)

# Cartoonish Hangman drawing functions
def draw_hangman(attempts):
    canvas.delete("all")
    # Base structure (cartoonish, more exaggerated lines)
    canvas.create_line(50, 250, 150, 250, width=5, fill="black")  # Base
    canvas.create_line(100, 250, 100, 50, width=5, fill="purple")  # Pole
    canvas.create_line(100, 50, 200, 50, width=5, fill="blue")  # Top bar
    canvas.create_line(200, 50, 200, 80, width=5, fill="green")  # Noose bar

    # Hangman parts with more colorful and exaggerated shapes
    if attempts <= 5:
        canvas.create_oval(180, 80, 220, 120, width=5, outline="yellow", fill="orange")  # Head (cartoonish)
    if attempts <= 4:
        canvas.create_line(200, 120, 200, 180, width=6, fill="red")  # Body
    if attempts <= 3:
        canvas.create_line(200, 140, 170, 160, width=6, fill="blue")  # Left arm
    if attempts <= 2:
        canvas.create_line(200, 140, 230, 160, width=6, fill="blue")  # Right arm
    if attempts <= 1:
        canvas.create_line(200, 180, 180, 220, width=6, fill="green")  # Left leg
    if attempts <= 0:
        canvas.create_line(200, 180, 220, 220, width=6, fill="green")  # Right leg

# Game logic
def check_guess():
    global remaining_attempts
    guess = entry.get().strip().upper()
    entry.delete(0, tk.END)

    if len(guess) != 1 or not guess.isalpha():
        messagebox.showwarning("Invalid Input", "Please enter a single letter!")
        return

    if guess in guessed_letters:
        messagebox.showinfo("Already Guessed", f"You already guessed '{guess}'!")
        return

    guessed_letters.add(guess)
    guessed_letters_label.config(text=f"Guessed Letters: {', '.join(sorted(guessed_letters))}")

    if guess in selected_word:
        for idx, letter in enumerate(selected_word):
            if letter == guess:
                display_word[idx] = guess
        word_label.config(text=" ".join(display_word))
        if "_" not in display_word:
            game_over("Congratulations!", "You guessed the word!")

    else:
        remaining_attempts -= 1
        attempts_label.config(text=f"Attempts Remaining: {remaining_attempts}")
        draw_hangman(remaining_attempts)
        if remaining_attempts == 0:
            game_over("Game Over", f"You lost! The word was {selected_word}")

def game_over(title, message):
    messagebox.showinfo(title, message)
    play_again()

# Prompt the user to continue or quit after a game ends
def play_again():
    response = messagebox.askyesno("Play Again", "Do you want to play with another word?")
    if response:
        start_new_word()
    else:
        quit_game()

# Skip the word
def skip_word():
    if messagebox.askyesno("Skip Word", "Are you sure you want to skip this word?"):
        start_new_word()

# Quit the game
def quit_game():
    if messagebox.askyesno("Quit Game", "Are you sure you want to quit?"):
        root.quit()

# Guess button
guess_button = tk.Button(root, text="Guess", command=check_guess, font=("Arial", 14))
guess_button.pack(pady=10)

# Buttons for skip and quit
button_frame = tk.Frame(root)
button_frame.pack(fill="x", pady=10)

skip_button = tk.Button(button_frame, text="Skip Word", command=skip_word, font=("Arial", 14))
skip_button.pack(side="left", padx=10)

quit_button = tk.Button(button_frame, text="Quit Game", command=quit_game, font=("Arial", 14))
quit_button.pack(side="right", padx=10)

# Start the game
start_new_word()
root.mainloop()
