# Ask : Roll the dice ?
# If user enters y or Y then roll the dice and print the number
# If user enters n or N then exit the game
# If user enters anything else then print "Invalid input, please enter y or n"

import random

while True:
    choice = input("Roll the dice? (y/n): ")
    if choice.lower() == 'y':
        roll = random.randint(1,6)
        print("You rolled a", roll)
    elif choice.lower() == 'n':
        print("Exiting the game. Goodbye!")
    else:
        print("Invalid input, please enter y or n") 
