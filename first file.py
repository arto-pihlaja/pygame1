import pygame as pg

class GameCharacter():
    def __init__(self, startX, startY):
        self.x = startX
        self.y = startY

    def move(self):
        pass

class FgRectangle(GameCharacter):
    def __init__(self, field, startX, startY, width, height):        
        super().__init__()
        self.field = field
        self.step = 5
        self.width = width
        self.height = height
        self.prevKey = []

    def move(self):
        keys = pg.key.get_pressed()
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

class Snake(GameCharacter):
    def move(self, hero):
        if self.x < hero.x:
            self.x += 5
        if self.x > hero.x:
            self.x -= 5
        if self.y < hero.y:
            self.y += 5            
        if self.y > hero.y:
            self.y -= 5            

class FgField():
    def __init__(self):
        self.width = 400
        self.height = 500
        self.screen = pg.display.set_mode((self.width, self.height)) 

    def redraw(self, hero, villain):
        self.screen.fill((0,0,0))
        pg.draw.rect(self.screen, (0,255,0), (hero.x, hero.y, hero.width, hero.height ))
        pg.draw.rect(self.screen, (255,0,0), (villain.x, villain.y, 10, 10 ))

class FirstGame():
    def __init__(self):
        pg.init()
        self.field = FgField()
        self.clock = pg.time.Clock()
        self.hero = FgRectangle(self.field, 50, 50, 10, 10)
        self.villain = Snake(0, 0)

    def moveCharacters(self):
        self.hero.move()
        self.villain.move(self.hero)
        self.field.redraw(self.hero, self.villain)

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
