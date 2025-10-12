"""
demo script to show imgclean in action
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageFilter
import shutil

sys.path.insert(0, str(Path(__file__).parent))

from imgclean import ImageCleaner


def create_sample_dataset():
    """create a sample messy image dataset for demonstration"""
    demo_dir = Path("demo_images")
    
    if demo_dir.exists():
        shutil.rmtree(demo_dir)
    
    demo_dir.mkdir()
    
    print("creating sample messy dataset...")
    
    # make some normal images
    for i in range(5):
        img = Image.new('RGB', (300, 300), color=(i*50, 100, 255-i*30))
        img.save(demo_dir / f"good_image_{i}.jpg")
    
    # make some duplicates to test duplicate detection
    img = Image.new('RGB', (300, 300), color=(255, 0, 0))
    img.save(demo_dir / "original.jpg")
    img.save(demo_dir / "duplicate1.jpg")
    img.save(demo_dir / "duplicate2.jpg")
    
    # make a blurry image
    img = Image.new('RGB', (300, 300), color=(0, 255, 0))
    blurry = img.filter(ImageFilter.GaussianBlur(radius=50))
    blurry.save(demo_dir / "blurry.jpg")
    
    # make some tiny images
    for i in range(2):
        img = Image.new('RGB', (50, 50), color=(100, 100, 255))
        img.save(demo_dir / f"tiny_{i}.jpg")
    
    # fake a corrupted file with just text
    with open(demo_dir / "corrupted.jpg", 'w') as f:
        f.write("this is not an image")
    
    print(f"created {len(list(demo_dir.glob('*')))} files in {demo_dir}/")
    return demo_dir


def main():
    demo_dir = create_sample_dataset()
    
    print("\n" + "="*60)
    print("imgclean demo")
    print("="*60)
    
    before_count = len(list(demo_dir.glob("*.jpg")))
    print(f"\nbefore cleaning: {before_count} images")
    
    cleaner = ImageCleaner()
    
    print("\nrunning imgclean...\n")
    
    results = cleaner.clean(
        str(demo_dir),
        remove_duplicates=True,
        remove_blurry=True,
        remove_corrupted=True,
        min_width=100,
        min_height=100,
        blur_threshold=100,
        dry_run=False,
        verbose=True,
    )
    
    print("\n" + "="*60)
    print("results")
    print("="*60)
    print(f"kept: {results['kept']} images")
    print(f"removed: {results['removed']} images")
    print(f"   - duplicates: {results['duplicates']}")
    print(f"   - blurry: {results['blurry']}")
    print(f"   - corrupted: {results['corrupted']}")
    print(f"   - too small: {results['size_filtered']}")
    
    print(f"\nyour dataset is now clean! check {demo_dir}/ folder")
    print("\ntip: use --dry-run flag to preview changes without deleting")


if __name__ == "__main__":
    main()
