import pygame as pg
from random import randint
from copy import deepcopy

class FgRectangle():
    def __init__(self, startX, startY, width, height):        
        self.x = startX
        self.y = startY
        self.width = width
        self.height = height

    def getTopLeft(self):
        return (self.x, self.y)

    def getTopRight(self):
        return ((self.x + self.width), self.y)

    def getBottomLeft(self):
        return (self.x, (self.y + self.height))

    def getBottomRight(self):
        return ((self.x + self.width), (self.y + self.height))

    def pointIsInside(self, point):
        x, y = point
        if x > self.x and x < (self.x + self.width)\
            and y > self.y and y < (self.y + self.height):
            return True
        else:
            return False 
    
    def overLapWithRectangle(self, rectangle2):
        # check if top left, top right, bottom left or bottom right of rectangle 2 is inside me
        if self.pointIsInside(rectangle2.getTopLeft())\
            or self.pointIsInside(rectangle2.getTopRight())\
            or self.pointIsInside(rectangle2.getBottomLeft())\
            or self.pointIsInside(rectangle2.getBottomRight()):
            return True
        else:
            return False

class Step():
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    def __init__(self, size, direction):
        self.size = size
        self.direction = direction

class GameCharacter():
    def __init__(self, field, startX, startY, width, height):        
        self.field = field
        # character placed at top left corner of bounding box
        self.x = startX
        self.y = startY
        self.width = width
        self.height = height
        
    def left(self):
        return self.x

    def right(self):
        return self.x + self.width

    def top(self):
        return self.y

    def bottom(self):
        return self.y + self.height

    def draw(self, colour):
        pg.draw.rect(self.field.screen, colour,\
             (self.x, self.y, self.width,self.height ))

    def isLeftOf(self, char2):
        return self.right() < char2.left()

    def isRightOf(self, char2):
        return self.left() > char2.right()
    
    def isAbove(self, char2):
        return self.bottom() < char2.top()

    def isBelow(self, char2):
        return self.top() > char2.bottom()

    def horizontalDistFrom(self, char2):
        # return abs(self.x - char2.x)
        dist = 0
        if self.isLeftOf(char2):
            dist = char2.left() - self.right()
        elif self.isRightOf(char2):
            dist = self.left() - char2.right()
        return dist

    def verticalDistFrom(self, char2):
        return abs(self.y - char2.y)


    def stepRightCollides(self, step, char2):
        if self.right() <= char2.left() < (self.right() + step.size)\
        and char2.top() < self.y < char2.bottom():
            return True
        else:
            return False

    def stepLeftCollides(self, step, char2):        
        if self.left() >= char2.right() > (self.left() - step.size)\
        and char2.top() < self.y < char2.bottom():
            return True
        else:
            return False

    def stepUpCollides(self, step, char2):
            if self.top() >= char2.bottom() > (self.top() - step.size)\
            and char2.left() < self.x < char2.right():
                return True
            else:
                return False

    def stepDownCollides(self, step, char2):
        if self.bottom() <= char2.top()  < (self.bottom() + step.size)\
        and char2.left() < self.x < char2.right():
            return True
        else:
            return False

    def stepCollidesWith(self, step, char2):
        if step.direction == step.RIGHT:
            return self.stepRightCollides(step, char2)
        elif step.direction == step.LEFT:             
            return self.stepLeftCollides(step, char2)
        elif step.direction == step.UP:             
            return self.stepUpCollides(step, char2)
        elif step.direction == step.DOWN:             
            return self.stepDownCollides(step, char2)



class FgHero(GameCharacter):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)        
        self.speed = 0 
        self.prevKey = []

    def move(self):
        keys = pg.key.get_pressed()
        if sum(keys) < 1:
            return
                
        if keys == self.prevKey:
            self.speed += 2  
        else:
            self.speed = 3          
            
        if keys[pg.K_LEFT]:
            self.x -= self.speed
        if keys[pg.K_RIGHT]:
            self.x += self.speed
        if keys[pg.K_UP]:
            self.y -= self.speed
        if keys[pg.K_DOWN]:
            self.y += self.speed
        if self.x > (self.field.width - self.width):
            self.x = (self.field.width - self.width)
        if self.x < 0:
            self.x = 0
        if self.y > (self.field.height - self.height):
            self.y = (self.field.height - self.height)
        if self.y < self.field.topMargin:
            self.y = self.field.topMargin
        self.prevKey = keys        
    
    def draw(self):
        super().draw(self.field.GREEN)

class Snake(GameCharacter):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)        
        self.length = 3
        self.speed = 3
        self.body = []

    def makeStep(self, step):
        if step.direction == step.LEFT:
            self.x -= step.size
        elif step.direction == step.RIGHT:
            self.x += step.size
        elif step.direction == step.UP:
            self.y -= step.size
        elif step.direction == step.DOWN:
            self.y += step.size

    def move(self, characters):
        hero = characters["hero"]
        makeMove = True
        heroCaught = False
        hDist = self.horizontalDistFrom(hero)
        vDist = self.verticalDistFrom(hero)  
        step = Step(1, 0)
        if self.isLeftOf(hero):
            step.direction = step.RIGHT
            distance = hDist
        elif self.isRightOf(hero):
            step.direction = step.LEFT
            distance = hDist
        elif self.isAbove(hero):
            step.direction = step.DOWN
            distance = vDist
        elif self.isBelow(hero):
            step.direction = step.UP 
            distance = vDist
        else:
            distance = 0
            heroCaught = True

        if distance > self.speed:
            step.size = self.speed
        else:
            step.size = distance                            
        
        for o in characters["obstacles"]:
                if self.stepCollidesWith(step, o):
                    # Can't move towards, so move in other direction
                    if step.direction == step.LEFT:
                        step.direction = step.DOWN
                    elif step.direction == step.RIGHT:
                        step.direction = step.UP
                    elif step.direction == step.UP:
                        step.direction = step.LEFT
                    elif step.direction == step.DOWN:
                        step.direction = step.RIGHT                        
                    break

        self.makeStep(step)
        self.body.insert(0, (self.x, self.y)) 

        while len(self.body) >= self.length:
            self.body.pop()
        
        return heroCaught

    def grow(self):
        self.length += 1

    def speedUp(self):
        self.speed += 1

    def draw(self):
        for p in reversed(self.body):
            self.x, self.y = p
            super().draw(self.field.RED)

class Obstacle(GameCharacter):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)
        self.colour = (100,100,100)        
    
    def hideOld(self):
        super().draw(self.field.BLACK)

    def move(self, characters):
        r = randint(0, 2)
        # if r <1: #swap orientation
        #     tmpWidth = self.width
        #     self.width = self.height        
        #     self.height = tmpWidth        
        self.x = randint(0, (self.field.width - self.width))
        self.y = randint(40, (self.field.height - self.height))        

    def draw(self):
        super().draw(self.colour)

class ScreenProcessor():
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    WHITE = (255,255,255)

    def __init__(self):
        pg.init()
        self.width = 300
        self.height = 300
        self.topMargin = 30
        self.screen = pg.display.set_mode((self.width, self.height)) 
        self.scoreFont = pg.font.SysFont("arial", 20, True)

    def drawCharacter(self, character, colour):
        pg.draw.rect(self.screen, colour, (character.x, character.y, character.width, character.height ))

    def clearCharacters(self):
        self.screen.fill(self.BLACK)

    def showScore(self, score):
        text = self.scoreFont.render(str(score), True, self.WHITE)
        self.screen.blit(text, ((self.width - 40),10))

    def showGameOver(self):
        font = pg.font.SysFont("arial", 20, True)
        text = font.render("Game over! Play again (y/n)?", True, self.BLUE)
        self.screen.blit(text, (40,10))
        pg.display.update()

class GameDriver():
    def __init__(self, sp):
        self.field = sp       
        self.hero = FgHero(self.field, 10, 50, 6, 8)
        self.snakes = [Snake(self.field, 10, 10, 10, 10)] 
        self.obstacles = [Obstacle(self.field, 100, 100, 80,10)]
        self.frame = 0
        self.score = 0
        self.characters = {"hero": self.hero, "snakes": self.snakes, "obstacles": self.obstacles}
   
    def updateGame(self):   
        heroCaught = self.moveCharacters()     
        self.frame +=1
        if self.frame % 50 == 0:    
            for s in self.characters["snakes"]:  
                s.grow()
                s.speedUp()        

        if self.frame % 200 == 0:
            self.characters["snakes"].append(Snake(self.field, 0, 0, 10, 10))
    
        if self.frame % 50 == 0:
            for o in self.characters["obstacles"]:
                o.move(self.characters)        

        if self.frame % 200 == 0:
            self.characters["obstacles"].append(Obstacle(self.field, 0, 30, 80,10))        
            
        self.updateScore()
        
        return heroCaught

    def moveCharacters(self):
        self.field.clearCharacters()
        self.frame +=1

        self.characters["hero"].move()
        self.characters["hero"].draw()
        heroCaught = False
        for s in self.characters["snakes"]:
            heroCaught = s.move(self.characters)
            s.draw()
            if heroCaught:
                break            

        for o in self.characters["obstacles"]:
            o.draw()

        return heroCaught

    def updateScore(self):
        if self.frame % 10 == 0:
            self.score += 10
        self.field.showScore(self.score)

    def noCollision(self):
        noCol = True
        hero = self.characters["hero"]
        for s in self.characters["snakes"]:
            for p in s.body:
                sx, sy = p
                rectSnake = FgRectangle(sx, sy, s.width, s.height)
                rectHero = FgRectangle(hero.x, hero.y, hero.width, hero.height)
                if rectSnake.overLapWithRectangle(rectHero):
                    noCol = False
                    break
                del rectHero
                del rectSnake
            if noCol == False:
                break
        return noCol

    def playAgain(self):        
        self.field.showGameOver()
        validResponse = False
        while not(validResponse):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_n:
                        return False
                    elif event.key == pg.K_y:
                        return True
                    else:
                        continue

def main():
    playMore = True
    sp = ScreenProcessor()
    clock = pg.time.Clock()
    while playMore:
        gd = GameDriver(sp)
        gameOn = True
        heroCaught = False
        while gameOn:
            heroCaught = gd.updateGame()
            # gameOn = gd.noCollision()
            clock.tick(10)
            pg.display.update()
            if heroCaught:
                gameOn = False
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameOn = False
                    playMore = False                        
        playMore = gd.playAgain()    
    pg.quit()


if __name__ == '__main__':
    main()
