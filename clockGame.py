import simplegui

# define global variables
'''time t = 1 is 0.1 second'''
t = 0
'''status boolean false when pressing stop'''
status = True
sec = 0
m = 0
n = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D

def format(t):
    global status, sec
    
    # convert time into the format in integer
    ''' multiplier to convert 60 seconds to 1 minute
    and so on...'''    
    secMultiplier = int(t / 600)
    
    ''' convert every 60 secs, 120 secs to 1 min, 2 min 
    repectively and so on...'''
    if secMultiplier > 0:
       sec = (t - 600 * secMultiplier) / 10
       sec = int(sec)
    else:
       sec = t / 10 
       sec = int(sec)
        
    '''converting time to centi second or 0.1 second'''
    csec = t % 10
    
    ''' converting time to minute'''
    min = int(t / 600)          

    # convert the format to string
    '''coverting min, sec, csec to strings'''
    min = str(min)
    csec = str(csec)
    
    ''' check to see if second is less than 10,
    if so put 0 infront'''
    if sec < 10:
        secs = str(sec)
        secs = "0" + secs
    else:
        secs = str(sec)
    return min + ":" + secs + ":" + csec

# check to see how many times you win or lose
def check():
    global m, n 
    global status
    secc = sec
    if status == False:
          if secc % 5 == 0:
             m += 1
             n += 1
          else:
             n += 1
    status = True
    q = str(m)
    r = str(n)
    return q + "/" + r
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global status
    timer.start()

def stop():
    global status
    global n 
    timer.stop()
    status = False
    
def reset():
    global t
    timer.stop()
    t = 0    

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global t
    t += 1

# define draw handler
def draw(canvas):
    '''draw timer'''
    canvas.draw_text(format(t), (145, 125), 48, "White")
    '''draw times you win or lose'''
    canvas.draw_text(check(), (285, 50), 24, "Green")
    
# create frame
frame = simplegui.create_frame("Converter", 400, 200)

# register event handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, timer_handler)
"""Buttons Start, Stop, and Reset"""
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

# start frame
frame.start()
