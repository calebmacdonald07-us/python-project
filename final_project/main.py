import os, sys
import pygame as pg

pg.init()

#Creates an absolute path to our python game file 
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")





size = width, height = 860, 600
black = 0, 0, 0




'''This function loads images with the option a colorkey or scale, and it allows for just the file name to be entered in, instead of the path (easier idk).'''
def load_image(name, colorkey = None, scale = 1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname).convert()

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

'''This function loads sounds and checks for errors, preventing crashing. It also allows for just the name of the file to be entered in.'''
def load_sound(name):
    #Define a small local class to help with error prevention and crashing, it doesn't do anything it just passes safely.
    class NoneSound:
        def play(self):
            pass
    
    #This checks if pg.mixer exists and is initialized, if not, then we return the safe NoneSound local class.
    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()
    
    #If we pass the error checking, we find the filepath and import the sound.
    fullname = os.path.join(data_dir, name)
    sound = pg.mixer.Sound(fullname)
    return sound

class Knight(pg.sprite.Sprite):
    def __init__(self, *groups, height = 100, speed = 5):
        pg.sprite.Sprite.__init__(self, *groups)
        
        #Set out variables for use in the rest of the class
        self._image, self._rect = load_image("idle/idle_1.png")  #we get out image and rect from our load_image function
        self._pos = self._rect.move(0, height)
        self._speed = speed
        self._animation_index = [0, 0]
        self._left_last = False


        self._idle = []
        for x in range(1, 3):
            image, _ = load_image(f"idle/idle_{x}.png")
            self._idle.append(image)

        self._rightf_run, self._leftf_run = [], []   #stands for right facing run
        for x in range(1, 8):   #I named the files run_1 all the way to run_7
            image, _ = load_image(f"run/right_facing/run_{x}.png")
            self._rightf_run.append(image)

            image, _ = load_image(f"run/left_facing/run_{x}.png")
            self._leftf_run.append(image)

    @property
    def image(self):
        return self._image
    
    @property
    def rect(self):
        return self._rect
    
    @property
    def pos(self):
        return self._pos


    def idle(self):
        if not self._left_last:
            self._image = self._idle[1]
        else:
            self._image = self._idle[0]
        

    def move(self, up=False, down=False, left=False, right=False):
        if right:
            self._pos.right += self._speed
        if left:
            self._pos.right -= self._speed
        if down:
            self._pos.top += self._speed
        if up:
            self._pos.top -= self._speed
        

        if self._pos.right > width:
            self._pos.right = width - 1
        if self._pos.left < 0:
            self._pos.left = 0
        if self._pos.bottom > height:
            self._pos.bottom = height
        if self._pos.top < 0:
            self._pos.top = 0

    def is_moving(self, keys):
        return (
            keys[pg.K_UP] or keys[pg.K_w] or
            keys[pg.K_DOWN] or keys[pg.K_s] or
            keys[pg.K_LEFT] or keys[pg.K_a] or
            keys[pg.K_RIGHT] or keys[pg.K_d]
    )

    def animation(self, keys):
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self._animation_index[1] += 0.1
            if self._animation_index[1] > len(self._rightf_run): self._animation_index[1] = 0
            self._image = self._rightf_run[int(self._animation_index[1])]
            self._left_last = False
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self._animation_index[0] += 0.1
            if self._animation_index[0] > len(self._leftf_run): self._animation_index[0] = 0
            self._image = self._leftf_run[int(self._animation_index[0])]
            self._left_last = True
        elif self._left_last == False:
            self._animation_index[1] += 0.1
            if self._animation_index[1] > len(self._rightf_run): self._animation_index[1] = 0
            self._image = self._rightf_run[int(self._animation_index[1])]
        elif self._left_last == True:
            self._animation_index[0] += 0.1
            if self._animation_index[0] > len(self._leftf_run): self._animation_index[0] = 0
            self._image = self._leftf_run[int(self._animation_index[0])]
        
class Skeleton(pg.sprite.Sprite):
    pass
        



def main():
    pg.init()

    screen = pg.display.set_mode(size)


    clock = pg.time.Clock()

    knight = Knight(speed = 2)
    

    while True:
        clock.tick(60)

        keys = pg.key.get_pressed()
        if keys[pg.K_UP] or keys[pg.K_w]:
            knight.move(up=True)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            knight.move(down=True)
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            knight.move(left=True)
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            knight.move(right=True)

        if knight.is_moving(keys):
            knight.animation(keys)
        else:
            knight.idle()



        for event in pg.event.get():
            if event.type == pg.QUIT: sys.exit()
        


        screen.fill([0, 0, 0])
        
        screen.blit(knight.image, knight.pos) 
        pg.display.flip()

main()
         