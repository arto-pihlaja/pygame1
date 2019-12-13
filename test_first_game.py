import unittest
import firstgame as fg

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

    def rectangle_inside_rectangle(self):
        # We need not test this. In this game, the rectangles will overlap partly 
        # before they overlap completely
        pass 
if __name__ == "__main__":
    unittest.main()