#Generate a random number between 1 and 100
#Ask the user to guess the number
#If the user's guess is correct, print "Congratulations! You guessed the number!"
#If the user's guess is too low, print "Too low! Try again."
#If the user's guess is too high, print "Too high! Try again."
#Continue to ask the user to guess until they guess the correct number

import random

number_to_guess = random.randint(1, 100)

while True:
    guess = int(input("Guess the number between 1 and 100: "))
    try:
        if guess < number_to_guess:
            print("Too low! Try again.")
        elif guess > number_to_guess:
            print("Too high! Try again.")
        else:
            print("Congratulations! You guessed the number!")
            break
    except ValueError:
        print("Invalid input, please enter a number between 1 and 100.")