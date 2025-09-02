import unittest

import main
from simpleimage import Image


class TestBasics(unittest.TestCase):
    def test_case01(self):
        ''' Testing copy - creating new object '''
        # Organize 
        self.image = Image("yosemite.jpg")

        # Action 
        new_image = self.image.copy()
        og_id = id(self.image)
        new_id = id(new_image)

        # Verify 
        self.assertTrue(og_id != new_id)

    def test_case02(self):
        # Organize 
        self.image = Image("yosemite.jpg")

        # Action 
        new_image = self.image.sepia()
        differentimagecheck = self.image == self.image
        sepia_worked = new_image != self.image

        # Verify 
        self.assertTrue(differentimagecheck and sepia_worked)

    
    def test_flip_vertical(self):
        flipped_image = self.image.flip(1)
        
        self.assertEqual(flipped_image.get_pixel(0, 0), (0, 0, 0)) 
        self.assertEqual(flipped_image.get_pixel(1, 0), (255, 255, 255)) 
        self.assertEqual(flipped_image.get_pixel(2, 0), (128, 128, 128)) 
        
        self.assertEqual(flipped_image.get_pixel(0, 1), (255, 0, 255))
        self.assertEqual(flipped_image.get_pixel(1, 1), (255, 255, 0))
        self.assertEqual(flipped_image.get_pixel(2, 1), (0, 255, 255))
        
        self.assertEqual(flipped_image.get_pixel(0, 2), (255, 0, 0))
        self.assertEqual(flipped_image.get_pixel(1, 2), (0, 255, 0)) 
        self.assertEqual(flipped_image.get_pixel(2, 2), (0, 0, 255)) 

    def test_flip_horizontal(self):
        flipped_image = self.image.flip(0)
        
        self.assertEqual(flipped_image.get_pixel(0, 0), (0, 0, 255))
        self.assertEqual(flipped_image.get_pixel(1, 0), (0, 255, 0))
        self.assertEqual(flipped_image.get_pixel(2, 0), (255, 0, 0))
        
        self.assertEqual(flipped_image.get_pixel(0, 1), (0, 255, 255))
        self.assertEqual(flipped_image.get_pixel(1, 1), (255, 0, 255))
        self.assertEqual(flipped_image.get_pixel(2, 1), (255, 255, 0))

        self.assertEqual(flipped_image.get_pixel(0, 2), (128, 128, 128))
        self.assertEqual(flipped_image.get_pixel(1, 2), (255, 255, 255))
        self.assertEqual(flipped_image.get_pixel(2, 2), (0, 0, 0))

    def test_shrink(self):

        scale = 2
        shrunken_image = self.image.shrink(scale)
        
        self.assertEqual(shrunken_image.width, 50)
        self.assertEqual(shrunken_image.height, 50)
        

        original_pixel = self.image.get_pixel(20, 20)
        shrunken_pixel = shrunken_image.get_pixel(10, 10)
        
        self.assertEqual(original_pixel, shrunken_pixel)

    

if __name__ == "__main__":
    unittest.main()