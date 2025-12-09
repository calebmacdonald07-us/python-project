import sys, pygame

pygame.init()


class Ball:
    def __init__(self, image, speed, height):
        self._speed = speed
        self._image = image
        self._pos = image.get_rect().move(0, height)
        self._sprite_width = image.get_size()[0]
        self._sprite_height = image.get_size()[1]
    
    @property
    def image(self):
        return self._image
    
    @property
    def pos(self):
        return self._pos



    #Our movement function
    # def move(self):
    #     self._pos = self._pos.move(self._speed)
    #     if self._pos.left < 0 or self._pos.right > width:
    #         self._speed[0] = -self._speed[0]
    #     if self._pos.top < 0 or self._pos.bottom > height:
    #         self._speed[1] = -self._speed[1]

    #New move function based on user input
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
            self._pos.left = 0
        if self._pos.top > height-self._sprite_height:
            self._pos.top = 0
        if self._pos.right < self._sprite_width:
            self._pos.right = width
        if self._pos.top < 0:
            self._pos.top = height-self._sprite_height


size = width, height = 1920, 1080
black = 0, 0, 0

screen = pygame.display.set_mode(size)

ball_1 = Ball(pygame.image.load("intro_ball.gif"), 1 , 10)


while True:

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ball_1.move(up=True)
    if keys[pygame.K_DOWN]:
        ball_1.move(down=True)
    if keys[pygame.K_LEFT]:
        ball_1.move(left=True)
    if keys[pygame.K_RIGHT]:
        ball_1.move(right=True)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(black)
    ball_1.move()
    screen.blit(ball_1.image, ball_1.pos)
    pygame.display.flip()