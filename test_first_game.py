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
        self.assertTrue(self.rect1.pointIsInside((105, 105)))

    def test_topleft_overlaps(self):
        self.rect2.x = 109
        self.rect2.y = 109
        self.assertTrue(self.rect2.overLapWithRectangle(self.rect1))

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

    @mock.patch.object(fg.FgHero, "move")
    def test_movecharacters(self, mock_move):
        mock_move.return_value = None
        for i in range(0,40):
            self.gd.moveCharacters()
        self.assertEqual(self.gd.score,40,"Counting score")
        self.assertEqual(self.gd.villain.speed, 4, "Speeding up snake")
        self.assertEqual(self.gd.villain.length,7, "Growing snake")

    @mock.patch.object(pg.event, "get")
    def test_playAgain(self, mock_get):
        mock_get.return_value = [MockEvent(pg.KEYDOWN, pg.K_n)]
        self.gd.field.showGameOver.return_value = None        
        self.assertEqual(self.gd.playAgain(), False)

if __name__ == "__main__":
    unittest.main()