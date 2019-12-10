import pygame as pg

class GameCharacter():
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY

    def move(self):
        pass

class FgRectangle():
    def __init__(self, field, startX, startY, width, height):        
        self.x = startX
        self.y = startY
        self.field = field
        self.width = width
        self.height = height

    def draw(self, colour):
        pg.draw.rect(self.field.screen, colour, (self.x, self.y, self.width,self.height ))


class FgHero(FgRectangle):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)        
        self.step = 5 
        self.prevKey = []

    def move(self):
        keys = pg.key.get_pressed()
        if len(keys) < 1:
            return
                
        if keys == self.prevKey:
            self.step += 3  
        else:
            self.step = 5          
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
        if self.y < 0:
            self.y = 0
        self.prevKey = keys        

class Snake(FgRectangle):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__(field, startX, startY, width, height)        
        self.length = 1
        self.previousPositions = []

    def move(self, hero):
        self.previousPositions.insert(0, (self.x, self.y))
        if len(self.previousPositions) > self.length:
            self.previousPositions.pop()
        if abs(self.x - hero.x) > 5:
            if self.x < hero.x:
                self.x += 5
            if self.x > hero.x:
                self.x -= 5
        else:
            if self.y < hero.y:
                self.y += 5            
            if self.y > hero.y:
                self.y -= 5            
    def grow():
        self.length += 1

class FgField():
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)

    def __init__(self):
        self.width = 400
        self.height = 500
        self.screen = pg.display.set_mode((self.width, self.height)) 

    def drawCharacter(self, character, colour):
        pg.draw.rect(self.screen, colour, (character.x, character.y, character.width, character.height ))

    def clearCharacters(self, hero, villain):
        self.drawCharacter(villain, self.BLACK)
        self.drawCharacter(hero, self.BLACK)

    def redrawCharacters(self, hero, villain):
        # self.screen.fill((0,0,0))
        self.drawCharacter(hero, self.GREEN)
        self.drawCharacter(villain, self.RED)

class FirstGame():
    def __init__(self):
        pg.init()
        self.field = FgField()
        self.clock = pg.time.Clock()
        self.hero = FgHero(self.field, 50, 50, 6, 8)
        self.villain = Snake(self.field, 0, 0, 10, 10)

    def moveCharacters(self):
        self.field.clearCharacters(self.hero, self.villain)
        self.hero.move()
        self.villain.move(self.hero)
        self.field.redrawCharacters(self.hero, self.villain)

def main():
    fg = FirstGame()
    play = True
    while play:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                play = False                        
        fg.moveCharacters()        
        fg.clock.tick(10)
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main()
