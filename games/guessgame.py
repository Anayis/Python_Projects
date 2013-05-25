""" Compilation: due to importing simplegui from 
 codeskulptor.org, the code is needed to be executed 
 in codeskulptor.org
 
 input will come from buttons and an input field
 all output for the game will be printed in the console

 Written by Yuttanant Suwansiri 01/05/2013"""
 
import simplegui
import random
import math

# initialize global variables used in your code
num_range = 100
n = 7

#Helper functions
"""first initializing computer guess"""
def init():
    global com_guess
    com_guess = 0
    com_guess = random.randrange(0,num_range)
    """print contents"""
    print "New game. Range is from 0 to", num_range
    print "Number of remaining guesses is", n 
    return com_guess
"""second initializing to your original setting
   initilize 0 to 100, or 0 to 1000"""
def init2():
    if num_range == 100:
       range100()
    else:
       range1000()

# define event handlers for control panel    
def range100():
    # button that changes range to range [0,100) and restarts
    global num_range, n 
    n = 7
    num_range = 100
    print ""
    init()
    return num_range, n

def range1000():
    # button that changes range to range [0,1000) and restarts
    global num_range, n
    num_range = 1000
    n = 10
    print ""
    init()
    return num_range, n

def get_input(guess):
    # main game logic goes here
    global n 
    global com_guess
    """take your guess"""
    guess = int(guess)
    """guesses get subtracted by 1 each time you guess"""
    n = n - 1 
    """print contents"""
    print ""
    print "Guess was", guess
    print "Number of remaining guess is", n
    """computer logic, higher, lower, correct, or ran out of guesses"""
    if n > 0:
        """you still have remaining guesses"""
        if guess == com_guess: 
           print "Correct!"
           print ""
           """initilize 0 to 100, or 0 to 1000"""
           init2()
        elif guess != com_guess:
           if guess > com_guess: 
              print "Lower"
           elif guess < com_guess:
              print "Higher"
    elif n <= 0:
        if guess == com_guess: 
           print "Correct!"
           print ""
           """initilize 0 to 100, or 0 to 1000"""
           init2()
        else:
           """you run out of guesses"""
           print "You ran out of guesses. The number was", com_guess
           print ""
           """initilize 0 to 100, or 0 to 1000"""
           init2()
    
# create frame
frame = simplegui.create_frame("Home", 200, 200)

# register event handlers for control elements
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.add_input("Enter a guess", get_input, 200)

init() 

# start frame
frame.start()

  



