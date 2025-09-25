import unittest
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import numpy as np

from imgclean import ImageCleaner


class TestImageCleaner(unittest.TestCase):
    
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.cleaner = ImageCleaner()
    
    def tearDown(self):
        shutil.rmtree(self.test_dir)
    
    def create_test_image(self, name, size=(100, 100), color=(255, 0, 0)):
        img = Image.new('RGB', size, color)
        path = Path(self.test_dir) / name
        img.save(path)
        return path
    
    def test_get_image_files(self):
        self.create_test_image('test1.jpg')
        self.create_test_image('test2.png')
        
        with open(Path(self.test_dir) / 'not_an_image.txt', 'w') as f:
            f.write('test')
        
        files = self.cleaner._get_image_files(Path(self.test_dir))
        self.assertEqual(len(files), 2)
    
    def test_find_duplicates(self):
        img_path = self.create_test_image('test1.jpg')
        shutil.copy(img_path, Path(self.test_dir) / 'test2.jpg')
        
        files = self.cleaner._get_image_files(Path(self.test_dir))
        duplicates = self.cleaner._find_duplicates(files, hash_size=8, verbose=False)
        
        self.assertEqual(len(duplicates), 1)
    
    def test_filter_by_size(self):
        self.create_test_image('small.jpg', size=(50, 50))
        self.create_test_image('large.jpg', size=(200, 200))
        
        files = self.cleaner._get_image_files(Path(self.test_dir))
        filtered = self.cleaner._filter_by_size(
            files, min_width=100, min_height=100, 
            max_width=None, max_height=None, verbose=False
        )
        
        self.assertEqual(len(filtered), 1)
    
    def test_clean_dry_run(self):
        self.create_test_image('test1.jpg')
        self.create_test_image('test2.jpg')
        
        results = self.cleaner.clean(
            self.test_dir,
            remove_duplicates=False,
            remove_blurry=False,
            remove_corrupted=True,
            dry_run=True,
            verbose=False
        )
        
        files = list(Path(self.test_dir).glob('*.jpg'))
        self.assertEqual(len(files), 2)


if __name__ == '__main__':
    unittest.main()
