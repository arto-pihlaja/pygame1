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
        if sum(keys) < 1:
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
        self.length = 3
        self.body = []

    def move(self, hero):
        self.body.insert(0, (self.x, self.y))
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
        self.body.insert(0, (self.x, self.y)) 
        while len(self.body) >= self.length:
            self.body.pop()

    def grow():
        self.length += 3

    def draw(self, colour):
        for p in reversed(self.body):
            self.x, self.y = p
            super().draw(colour)

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
        hero.draw(self.BLACK)
        villain.draw(self.BLACK)
        # self.drawCharacter(villain, self.BLACK)
        # self.drawCharacter(hero, self.BLACK)

    def redrawCharacters(self, hero, villain):
        hero.draw(self.GREEN)
        villain.draw(self.RED)

        # self.screen.fill((0,0,0))
        # self.drawCharacter(hero, self.GREEN)
        # self.drawCharacter(villain, self.RED)


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

    def noCollision(self):
        noCol = True
        for p in self.villain.body:
            sx, sy = p
            if self.hero.x > sx and self.hero.x < (sx + self.villain.width)\
                and self.hero.y > sy and self.hero.y < (sy + self.villain.height):                
                noCol = False
                break
        return noCol

    def playAgain(self):        
        font = pg.font.SysFont("arial", 20, True)
        text = font.render("Game over! Play again (y/n)?", True, (0,0,255))
        self.field.screen.blit(text, (100,10))
        pg.display.update()
        keys = []
        validResponse = False
        while not(validResponse):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pygame.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_n:
                        return False
                    else:
                        return True

def main():
    playMore = True
    while playMore:
        fg = FirstGame()
        gameOn = True
        while gameOn:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameOn = False
                    playMore = False                        
            fg.moveCharacters()
            gameOn = fg.noCollision()
            fg.clock.tick(10)
            pg.display.update()
        playMore = fg.playAgain()    
    pg.quit()


if __name__ == '__main__':
    main()
