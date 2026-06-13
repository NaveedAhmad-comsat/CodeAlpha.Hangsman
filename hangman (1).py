import random   # Used to pick a random word each round


# ── 1. WORD LIST ─────────────────────────────────────────────
# 5 predefined words the game will randomly choose from.
# All lowercase so we can do case-insensitive comparisons later.
WORDS = ["python", "matrix", "rocket", "bridge", "galaxy"]


# ── 2. HANGMAN STAGES ────────────────────────────────────────
# Each string in this list is one stage of the gallows drawing.
# Index 0  → no body parts (0 wrong guesses)
# Index 6  → fully drawn man (6 wrong guesses → game over)
HANGMAN_STAGES = [
    # Stage 0 — empty gallows
    """
       -----
       |   |
       |
       |
       |
       |
    --------""",
    # Stage 1 — head
    """
       -----
       |   |
       |   O
       |
       |
       |
    --------""",
    # Stage 2 — head + torso
    """
       -----
       |   |
       |   O
       |   |
       |
       |
    --------""",
    # Stage 3 — head + torso + left arm
    """
       -----
       |   |
       |   O
       |  /|
       |
       |
    --------""",
    # Stage 4 — head + torso + both arms
    """
       -----
       |   |
       |   O
       |  /|\\
       |
       |
    --------""",
    # Stage 5 — head + torso + both arms + left leg
    """
       -----
       |   |
       |   O
       |  /|\\
       |  /
       |
    --------""",
    # Stage 6 — full body (game over)
    """
       -----
       |   |
       |   O
       |  /|\\
       |  / \\
       |
    --------""",
]


# ── 3. HELPER FUNCTION — display the word progress ───────────
def display_word(secret_word, guessed_letters):
    """
    Returns the word with correctly guessed letters revealed
    and unguessed letters shown as underscores.

    Example:
        secret_word   = "python"
        guessed_letters = {'p', 'h', 'n'}
        → returns  "p _ _ h _ n"
    """
    # Build a list: show the letter if guessed, else show '_'
    display = [letter if letter in guessed_letters else "_"
               for letter in secret_word]

    # Join with spaces for readability: ['p','_','_'] → "p _ _"
    return " ".join(display)


# ── 4. HELPER FUNCTION — print the current game state ────────
def print_game_state(secret_word, guessed_letters, wrong_guesses, max_wrong):
    """Prints the gallows, the word progress, and wrong letters."""

    # Print the hangman drawing that matches how many wrong guesses
    print(HANGMAN_STAGES[wrong_guesses])

    # Show wrong guess counter
    print(f"\n  Wrong guesses: {wrong_guesses} / {max_wrong}")

    # Show which wrong letters the player already tried
    wrong_letters = [l for l in guessed_letters if l not in secret_word]
    if wrong_letters:
        print(f"  Bad letters  : {', '.join(sorted(wrong_letters))}")
    else:
        print("  Bad letters  : none yet")

    # Show the word with blanks
    print(f"\n  Word  →  {display_word(secret_word, guessed_letters)}\n")


# ── 5. MAIN GAME FUNCTION ────────────────────────────────────
def play_hangman():
    """Runs one full round of Hangman."""

    MAX_WRONG = 6          # Maximum allowed incorrect guesses

    # ── Pick a random word ──────────────────────────────────
    secret_word = random.choice(WORDS)

    # ── Track state ─────────────────────────────────────────
    guessed_letters = set()    # All letters the player has tried (right or wrong)
    wrong_guesses   = 0        # Count of incorrect guesses so far

    # ── Welcome banner ──────────────────────────────────────
    print("\n" + "=" * 45)
    print("      W E L C O M E   T O   H A N G M A N")
    print("=" * 45)
    print(f"  Guess the {len(secret_word)}-letter word before you run out!")
    print(f"  You have {MAX_WRONG} wrong guesses allowed.")
    print("=" * 45)

    # ── Main game loop ───────────────────────────────────────
    # Keep playing as long as the player has guesses left
    # AND hasn't revealed the full word yet.
    while wrong_guesses < MAX_WRONG:

        # Display current gallows + word progress
        print_game_state(secret_word, guessed_letters, wrong_guesses, MAX_WRONG)

        # ── Get a valid single letter from the player ───────
        while True:
            guess = input("  Enter a letter: ").strip().lower()

            # Validate: must be exactly one alphabetic character
            if len(guess) != 1 or not guess.isalpha():
                print("  ⚠  Please enter a single letter (a–z).")
            elif guess in guessed_letters:
                print(f"  ⚠  You already tried '{guess}'. Pick another!")
            else:
                break   # Valid, unused letter — exit the validation loop

        # ── Record the guess ────────────────────────────────
        guessed_letters.add(guess)

        # ── Check: correct or wrong? ─────────────────────────
        if guess in secret_word:
            print(f"\n  ✔  Nice! '{guess}' is in the word!")

            # Check if the player has now revealed ALL letters
            if all(letter in guessed_letters for letter in secret_word):
                # Every letter guessed → player wins!
                print_game_state(secret_word, guessed_letters, wrong_guesses, MAX_WRONG)
                print("=" * 45)
                print("  🎉  YOU WIN!  The word was:", secret_word.upper())
                print("=" * 45 + "\n")
                return   # End the function (and the game)
        else:
            # Wrong guess: increment counter and warn the player
            wrong_guesses += 1
            remaining = MAX_WRONG - wrong_guesses
            print(f"\n  ✘  '{guess}' is NOT in the word. "
                  f"({remaining} guess{'es' if remaining != 1 else ''} left)")

    # ── Loop ended because wrong_guesses reached MAX_WRONG ──
    # Show the final (fully drawn) hangman and reveal the word
    print_game_state(secret_word, guessed_letters, wrong_guesses, MAX_WRONG)
    print("=" * 45)
    print("  💀  GAME OVER!  The word was:", secret_word.upper())
    print("=" * 45 + "\n")


# ── 6. PLAY-AGAIN LOOP ───────────────────────────────────────
def main():
    """Entry point — lets the player keep playing until they quit."""

    while True:
        play_hangman()

        # Ask if they want another round
        again = input("  Play again? (y / n): ").strip().lower()
        if again != "y":
            print("\n  Thanks for playing Hangman! Goodbye 👋\n")
            break   # Exit the play-again loop


# ── 7. ENTRY POINT ───────────────────────────────────────────
# This block runs only when the script is executed directly,
# not when it's imported as a module in another script.
if __name__ == "__main__":
    main()
