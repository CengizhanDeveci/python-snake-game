import pygame
import random
pygame.init()

global row
global width
global length
row = 20
width = 500
length = width // row

win = pygame.display.set_mode((width,width))
clock = pygame.time.Clock()

class Snake:
    def __init__(self,x=275,y=200,height=length,width=length):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.positions = [(200,200),(225,200),(250,200)]
        self.dirx = 1
        self.diry = 0
        self.eatItself = False

    def move(self):
        if self.dirx == 1 and self.diry == 0:
            self.x += length
        elif self.dirx == -1 and self.diry == 0:
            self.x -= length
        elif self.dirx == 0 and self.diry == 1:
            self.y -= length
        elif self.dirx == 0 and self.diry == -1:
            self.y += length
        for i in self.positions[:-2]:
            if i == (self.x,self.y):                
                self.eatItself = True
        self.positions.append((self.x,self.y))
        self.positions.pop(0)
    

    def control(self):
        if self.positions[-1][0] >= 500 or self.positions[-1][0] < 0 or self.positions[-1][1] >= 500 or self.positions[-1][1] < 0:
            return True

    def draw(self,win):
        drawGrid(win)
        for i in self.positions:
            pygame.draw.rect(win, (255,0,0), (i[0],i[1],length,length))


class Food:
    def __init__(self):
        self.x = random.randint(0,row-1) * length
        self.y = random.randint(0,row-1) * length

    def spawn(self,win):
        pygame.draw.rect(win, (0,0,255), (self.x ,self.y, length, length))


def drawGrid(win):
    for i in range(1,row):
        pygame.draw.line(win, (255,255,255), (width//row * i,0), (width//row*i,width))
        pygame.draw.line(win, (255,255,255), (0, width//row * i), (width,width//row*i))
        

def reDrawGameWindow(win):
    win.fill((0,0,0))
    snake.draw(win)
    food.spawn(win)
    drawGrid(win)
    pygame.display.update()
    

snake = Snake()
food = Food()

run = True
while run:
    pygame.display.set_caption(f"Python Snake Game Score: {len(snake.positions) - 3}")
    clock.tick(10)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and snake.dirx != 1:
        snake.dirx = -1
        snake.diry = 0
    elif keys[pygame.K_RIGHT] and snake.dirx != -1:
        snake.dirx = 1
        snake.diry = 0
    elif keys[pygame.K_UP] and snake.diry != -1:
        snake.dirx = 0
        snake.diry = 1
    elif keys[pygame.K_DOWN] and snake.diry != 1:
        snake.dirx = 0
        snake.diry = -1

    if snake.control() == True or snake.eatItself:       
        font1 = pygame.font.SysFont('comicsans',50)
        text = font1.render('You Lose Your Score: ' + str(len(snake.positions) -3), 1, (255,0,0))
        win.blit(text, (round(250- (text.get_width() / 2)),200))
        pygame.display.update()
        i = 0
        while i < 300:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    run = False
        snake = Snake()
        food = Food()
    
    if snake.x == food.x and snake.y == food.y:
        pygame.time.delay(10)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and snake.dirx != 1:
            snake.dirx = -1
            snake.diry = 0
        elif keys[pygame.K_RIGHT] and snake.dirx != -1:
            snake.dirx = 1
            snake.diry = 0
        elif keys[pygame.K_UP] and snake.diry != -1:
            snake.dirx = 0
            snake.diry = 1
        elif keys[pygame.K_DOWN] and snake.diry != 1:
            snake.dirx = 0
            snake.diry = -1
        snake.positions.append((snake.x + snake.dirx * length, snake.y - snake.diry * length))
        snake.move()
        del food
        food = Food()
    else:
        snake.move()

    reDrawGameWindow(win)
    