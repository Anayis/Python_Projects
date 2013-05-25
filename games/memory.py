# implementation of card game - Memory
""" There are 16 cards in total, 2 sets of 8 cards
with value 0 to 7. You have to draw the same valued cards
to keep the 2 cards openned. This game keeps track of 
how many times it take in total to open all the 16 cards.

* Dependency: run this code on codeskulptor.org
By Yuttanant Suwansiri 5 May 2013
"""

import simplegui
import random

# helper function to initialize globals
def init():
    global full_list, exposed, state, compare, i, j, k, moves
    # assign numbers to all 16 cards
    half_list = range(8)
    full_list = half_list + half_list
    random.shuffle(full_list)
    # initialize exposed to all True to
    # keep track which card is selected
    exposed = range(16)
    for n in range(16):
         exposed[n] = True
    # initialize state 1st or 2nd card is selected        
    state = 0 
    compare = [0,0]
    i = 0
    j = 0
    k = 0
    # moves keeps track of how many moves you have clicked
    moves = 0
     
# define event handlers
def mouseclick(pos):
    global exposed, state, compare, i, j, k, moves
    # picking the cards
    # determining card number. Ex. 1 or 2
    if state == 0:
        i = pos[0] // 50
        if exposed[i] == True:
            exposed[i] = False
            compare[0] = full_list[i]
            compare[1] = full_list[i]
            state = 1
            moves += 1       
    elif state == 1:
        j = pos[0] // 50
        if exposed[j] == True:
            compare[1] = full_list[j]
            state = 2
            moves += 1    
            exposed[j] = False
        else:
            # prevent card from re-selected again
            print "card2 is already openned"
            compare[0] = 8
            compare[1] = 8
    
    else:
        compare_f()
        k = pos[0] // 50
        if exposed[k] == True:
            compare[0] = full_list[k]
            state = 1    
            moves += 1
            exposed[k] = False
        else:
            # prevent card from re-selected again
            print "card1 is already openned"
            compare[0] = 8
            compare[1] = 8
            
    print compare    
    moves_str = str(moves)   
    label.set_text("Move = " + moves_str)
    
# compare 2 cards if they have the same values        
def compare_f():
    if compare[0] != compare[1]:
        exposed[i] = True
        exposed[j] = True
        exposed[k] = True
        compare[0] = full_list[k]
    else:
        print "keep", compare
                     
# cards are logically 50x100 pixels in size    
def draw(canvas):
    
    # selecting the cards
    # draw numbers of 16 cards
    global full_list
    i = 0
    for n in full_list:
        n = str(n)
        canvas.draw_text(n, [19 + 50 * i, 50], 25, "White")
        canvas.draw_line([50 * (i + 1), 0], [50 * (i + 1), 100], 1, "Red")
        i += 1
        # draw the back of the cards in green color
        for m in range(16):
                if exposed[m] == True:
                    canvas.draw_polygon([[0 + 50*m,0], [0 + 50*m, 100], [50 + 50*m,100], [50 + 50*m,0]], 1, "Red", "Green") 
                    m += 1   
       
# create frame and add a button and labels

frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Move = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
