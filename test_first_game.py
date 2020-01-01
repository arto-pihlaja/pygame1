import unittest
import unittest.mock as mock
import firstgame as fg
import pygame as pg

class MockFgField():
    BLACK = (0,0,0)
    RED = (255,0,0)
    GREEN = (0,255,0)

    def __init__(self):
        self.width = 400
        self.height = 500
        self.screen = []

class TestGameCharacter(unittest.TestCase):
    def setUp(self):
        self.obstacle = fg.GameCharacter(mock.Mock(), 100, 100, 10, 80)
        self.movingCharacter = fg.GameCharacter(mock.Mock(), 0, 0, 10, 10)

    def test_stepRightCollides(self): 
        self.movingCharacter.x = 89
        self.movingCharacter.y = 120
        step = fg.Step(20, fg.Step.RIGHT)
        self.assertEqual(self.movingCharacter.stepRightCollides(step, self.obstacle), True,\
             "Failed to notice that step right crosses obstacle")

    def test_stepLeftCollides(self): 
        self.movingCharacter.x = 112
        self.movingCharacter.y = 120
        step = fg.Step(4, fg.Step.LEFT)
        self.assertEqual(self.movingCharacter.stepLeftCollides(step, self.obstacle), True,\
             "Failed to notice that step left crosses obstacle")

        self.movingCharacter.y = 80
        self.assertEqual(self.movingCharacter.stepLeftCollides(step, self.obstacle), False,\
             "Failed to notice that step left goes over obstacle")        

class TestCollisionDetection(unittest.TestCase):
    def setUp(self):
        self.rect1 = fg.FgRectangle(100, 100, 10, 10)
        self.rect2 = fg.FgRectangle(0, 0, 5, 5)     

    def test_topleft(self):
        self.assertEqual(self.rect2.getTopLeft(), (0,0))

    def test_topright(self):
        self.assertEqual(self.rect2.getTopRight(), (5,0))

    def test_bottomleft(self):
        self.assertEqual(self.rect2.getBottomLeft(), (0,5))

    def test_bottomright(self):
        self.assertEqual(self.rect2.getBottomRight(), (5,5))

    def test_topleft_inside(self):        
        self.assertTrue(self.rect1.pointIsInside((105, 105)), "Didn't identify point inside rectangle")

    def test_topleft_overlaps(self):
        self.rect2.x = 109
        self.rect2.y = 109
        self.assertTrue(self.rect2.overLapWithRectangle(self.rect1), "Didn't notice top left overlap")

    def test_topright_overlaps(self):
        self.rect2.x = 96
        self.rect2.y = 109
        self.assertTrue(self.rect2.overLapWithRectangle(self.rect1))

    def test_bottomleft_overlaps(self):
        self.rect2.x = 109
        self.rect2.y = 96
        self.assertTrue(self.rect2.overLapWithRectangle(self.rect1))

    def test_bottomright_overlaps(self):
        self.rect2.x = 96
        self.rect2.y = 96
        self.assertTrue(self.rect2.overLapWithRectangle(self.rect1))

    def test_rectangle_inside_rectangle(self):
        self.rect2.x = 102
        self.rect2.y = 102
        self.assertTrue(self.rect1.overLapWithRectangle(self.rect2))

class MockEvent():
    def __init__(self, event_type, key):
        self.type = event_type
        self.key = key

class TestGameDriver(unittest.TestCase):
    def setUp(self):
        self.gd = fg.GameDriver(mock.Mock())
        self.gd.field.width = 300
        self.gd.field.height = 300
        self.gd.hero.x = 10
        self.gd.hero.y = 10
        

    @mock.patch.object(fg.FgHero, "move")
    @mock.patch.object(fg.GameCharacter, "draw")
    def test_movecharacters(self, mock_move, mock_draw):
        for i in range(0,40):
            self.gd.moveCharacters()
        self.assertEqual(self.gd.score,40,"Failed to count score")
        for s in self.gd.characters["snakes"]:
            self.assertEqual(s.speed, 4, "Failed speeding up snake")
            self.assertEqual(s.length,5, "Failed growing snake")

    @mock.patch.object(pg.event, "get")
    def test_playAgain(self, mock_get):
        mock_get.return_value = [MockEvent(pg.KEYDOWN, pg.K_n)]
        self.assertEqual(self.gd.playAgain(), False, "User wants to end game")

        mock_get.return_value = [MockEvent(pg.KEYDOWN, pg.K_y)]
        self.assertEqual(self.gd.playAgain(), True, "User wants to continue game")

if __name__ == "__main__":
    unittest.main()