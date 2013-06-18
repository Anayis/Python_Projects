""" Classic Asteroids game. In this version, you have 3 lives.
When your live = 0, the game restarts. Hit as many asteroids as you can to score. 
(Press up to power the thrust, left and right to move around, and space to shoot)
* Dependency: run this code on codeskulptor.org
By Yuttanant Suwansiri 20 Jun 2013
"""

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
angle_acc = math.pi / 35
thrust_const = 0.2
friction_const = 0.01
missile_const = 5
started = False # starting the game indication
rock_group = set()
missile_group = set()
speed_cnst = 1 # rock traveling speed
explosion_group = set()
DIM = 64 # explosion speed

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def keydown(key):
    if key==simplegui.KEY_MAP["left"]:
        my_ship.angle_vel -= angle_acc
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel += angle_acc
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.thrust = True
    elif key==simplegui.KEY_MAP["space"]:
        my_ship.shoot()

def keyup(key):
    if key==simplegui.KEY_MAP["left"]:
        my_ship.angle_vel += angle_acc
    elif key==simplegui.KEY_MAP["right"]:
        my_ship.angle_vel -= angle_acc
    elif key==simplegui.KEY_MAP["up"]:
        my_ship.thrust = False

# update rock_group in draw handler        
def process_sprite_group():
    for inst in rock_group:
        inst.update()
    for inst in missile_group:
        inst.update()
        inst.age += 1
        if inst.age > 50: # missile age
            missile_group.remove(inst)

# detect collision of ship and rocks
def group_collide(g1):
    global lives, started, score, rock_group, speed_cnst, explosion_group
    for inst in rock_group:
        if inst.collide(g1) == True:
            rock_group.remove(inst)
            # add explosion
            explosion = Sprite(g1.pos, [1, 1], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion.animated = True
            explosion_group.add(explosion)
            # deduct lives
            lives -= 1 
            if lives <= 0: # if live is 0, start new game
                started = False
                frame.set_mouseclick_handler(click)
                score = 0
                lives = 3
                rock_group = set()
                speed_cnst = 1
                 
# detect collision of missiles and rocks
def group_group_collide(g1, g2):
    global score, speed_cnst
    for inst_missile in g1:
        for inst_rock in g2:
            if inst_rock.collide(inst_missile):
                missile_group.remove(inst_missile)
                rock_group.remove(inst_rock)
                score += 10
                speed_cnst += 1
                explosion = Sprite(inst_rock.pos, [1, 1], 0, 0, explosion_image, explosion_info, explosion_sound)
                explosion.animated = True
                explosion_group.add(explosion)
                
# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.age = 0
        
    def draw(self,canvas):
      # canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        if self.thrust == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else: 
            canvas.draw_image(self.image, [135, 45], self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        ship_thrust_sound.pause()   
        # angle velocity update
        self.angle += self.angle_vel
        # position update
        self.pos[1] += self.vel[1]
        self.pos[0] += self.vel[0]
        # collide in y direction
        if self.pos[1] <= 0:
            self.pos[1] = HEIGHT + self.pos[1]
        if self.pos[1] > HEIGHT:
            self.pos[1] = self.pos[1] - HEIGHT
        # collide in x direction
        if self.pos[0] <= 0:
            self.pos[0] = WIDTH + self.pos[0]
        if self.pos[0] > WIDTH:
            self.pos[0] = self.pos[0] - WIDTH
        # velocity update
        self.forward = angle_to_vector(self.angle)
        if self.thrust:
            ship_thrust_sound.play()
            self.vel[0] += self.forward[0] * thrust_const
            self.vel[1] += self.forward[1] * thrust_const
        # friction update
        self.vel[0] *= (1 - friction_const)
        self.vel[1] *= (1 - friction_const)
       
    def shoot(self):
        # create missiles
        a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
        # position
        a_missile.pos[0] = self.pos[0] + self.radius * self.forward[0]
        a_missile.pos[1] = self.pos[1] + self.radius * self.forward[1]
        # velocity
        a_missile.vel[0] =+ self.vel[0] + self.forward[0] * missile_const
        a_missile.vel[1] =+ self.vel[1] + self.forward[1] * missile_const
        missile_sound.rewind()
        missile_sound.play()
        # add a missile to group
        missile_group.add(a_missile)
       
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        self.animated = False
        self.time = 0 
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        # canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        if self.animated == False:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        else: 
            current_index = (self.time % DIM) // 1
            current_center = [self.image_center[0] +  current_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_center, self.image_size, self.pos, self.image_size) 
            self.time += 0.2
        
    def update(self):
        # angle velocity update
        self.angle += self.angle_vel
        # position update
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        # collide in y direction
        if self.pos[1] <= 0:
            self.pos[1] = HEIGHT + self.pos[1]
        if self.pos[1] > HEIGHT:
            self.pos[1] = self.pos[1] - HEIGHT
        # collide in x direction
        if self.pos[0] <= 0:
            self.pos[0] = WIDTH + self.pos[0]
        if self.pos[0] > WIDTH:
            self.pos[0] = self.pos[0] - WIDTH
        
    def collide(self, other_object):
        #detect collision 
        d = []
        d = dist(other_object.pos, self.pos)
        r12 = other_object.radius + self.radius
        if d > r12:
            return False
        else: 
            return True
       
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True   
        
def draw(canvas):
    global time, started
    score_str = str(score)
    lives_str = str(lives)
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])
    
    # draw ship and sprites
    my_ship.draw(canvas)
    for inst in rock_group: # draw rocks
        inst.draw(canvas)
    for inst in missile_group: # draw missiles
        inst.draw(canvas)
    for inst in explosion_group: # draw explosion
        inst.draw(canvas)
        inst.age += 1
        if inst.age > 50: # age
            explosion_group.remove(inst)
        
    # update ship and sprites
    my_ship.update()
    process_sprite_group()
    
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), 
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], 
                          splash_info.get_size())
        
    # collide
    group_collide(my_ship)
    group_group_collide(missile_group, rock_group)
    
    # scores and lives
    canvas.draw_text("Lives", (75, 75), 36, "White")
    canvas.draw_text(lives_str, (75, 110), 36, "White")
    canvas.draw_text("Score", (650, 75), 36, "White")
    canvas.draw_text(score_str, (650, 110), 36, "White")
            
# timer handler that spawns a rock    
def rock_spawner():
    if started == True:
        a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
        # velocity of rocks increase when the game progresses
        a_rock.vel = [random.randrange(-10, 10) / 100 * speed_cnst, random.randrange(-10, 10) / 100 * speed_cnst]
        a_rock.angle_vel = random.randrange(-10, 10) / 100 
        a_rock.pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        # ignore a rock spawn event if the spawned rock is too close to the ship   
        while dist(a_rock.pos, my_ship.pos) < my_ship.radius * 4: 
            a_rock.pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
        # set the number of rocks and add rocks to the group
        if len(rock_group) < 12: 
            rock_group.add(a_rock)    
        
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
#a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
#a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
timer = simplegui.create_timer(1000.0, rock_spawner) # rock spawning time

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(click)

# get things rolling
timer.start()
frame.start()