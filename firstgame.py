import pygame as pg

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

class GameCharacter():
    def __init__(self, field, startX, startY, width, height):        
        self.field = field
        # character placed at top left corner of bounding box
        self.x = startX
        self.y = startY
        self.width = width
        self.height = height

    def draw(self, colour):
        pg.draw.rect(self.field.screen, colour,\
             (self.x, self.y, self.width,self.height ))


class FgHero(GameCharacter):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)        
        self.step = 5 
        self.prevKey = []

    def move(self):
        keys = pg.key.get_pressed()
        if sum(keys) < 1:
            return
                
        if keys == self.prevKey:
            self.step += 2  
        else:
            self.step = 3          
            
        if keys[pg.K_LEFT]:
            self.x -= self.step
        if keys[pg.K_RIGHT]:
            self.x += self.step
        if keys[pg.K_UP]:
            self.y -= self.step
        if keys[pg.K_DOWN]:
            self.y += self.step
        if self.x > (self.field.width - self.width):
            self.x = (self.field.width - self.width)
        if self.x < 0:
            self.x = 0
        if self.y > (self.field.height - self.height):
            self.y = (self.field.height - self.height)
        if self.y < self.field.topMargin:
            self.y = self.field.topMargin
        self.prevKey = keys        

class Snake(GameCharacter):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)        
        self.length = 3
        self.speed = 3
        self.body = []

    def move(self, hero):
        self.body.insert(0, (self.x, self.y))
        if abs(self.x - hero.x) > self.speed:
            if self.x < hero.x:
                self.x += self.speed
            if self.x > hero.x:
                self.x -= self.speed
        else:
            self.x = hero.x
            if abs(self.y - hero.y) < self.speed:
                self.y = hero.y
            else:
                if self.y < hero.y:
                    self.y += self.speed            
                if self.y > hero.y:
                    self.y -= self.speed           
        self.body.insert(0, (self.x, self.y)) 
        while len(self.body) >= self.length:
            self.body.pop()

    def grow(self):
        self.length += 2

    def speedUp(self):
        self.speed += 1

    def draw(self, colour):
        for p in reversed(self.body):
            self.x, self.y = p
            super().draw(colour)

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

    def clearCharacters(self, hero, villain):
        self.screen.fill(self.BLACK)

    def redrawCharacters(self, hero, villain):
        hero.draw(self.GREEN)
        villain.draw(self.RED)

    def showScore(self, score):
        text = self.scoreFont.render(str(score), True, self.WHITE)
        self.screen.blit(text, ((self.width - 30),10))

    def showGameOver(self):
        font = pg.font.SysFont("arial", 20, True)
        text = font.render("Game over! Play again (y/n)?", True, self.BLUE)
        self.screen.blit(text, (40,10))
        pg.display.update()

class GameDriver():
    def __init__(self, sp):
        self.field = sp       
        self.hero = FgHero(self.field, 50, 50, 6, 8)
        self.villain = Snake(self.field, 0, 50, 10, 10)
        self.frame = 0
        self.score = 0

    def moveCharacters(self):
        self.field.clearCharacters(self.hero, self.villain)
        self.hero.move()
        self.villain.move(self.hero)
        self.field.redrawCharacters(self.hero, self.villain)
        self.frame +=1
        if self.frame % 10 == 0:
            self.score += 10
        if self.frame % 20 == 0:
            self.villain.grow()
        if self.frame % 40 == 0:    
            self.villain.speedUp()

    def updateScore(self):
        self.field.showScore(self.score)

    def noCollision(self):
        noCol = True
        for p in self.villain.body:
            sx, sy = p
            rectVillain = FgRectangle(sx, sy, self.villain.width, self.villain.height)
            rectHero = FgRectangle(self.hero.x, self.hero.y, self.hero.width, self.hero.height)
            if rectVillain.overLapWithRectangle(rectHero):
                noCol = False
                break
            del rectHero
            del rectVillain
        return noCol

    def playAgain(self):        
        self.field.showGameOver()
        keys = []
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
        while gameOn:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameOn = False
                    playMore = False                        
            gd.moveCharacters()
            gameOn = gd.noCollision()
            gd.updateScore()
            clock.tick(10)
            pg.display.update()
        playMore = gd.playAgain()    
    pg.quit()


if __name__ == '__main__':
    main()
