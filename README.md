<div align="center">

#  imgclean

**clean your image datasets effortlessly!**

[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Installation](#-quick-start) • [Features](#-features) • [Usage](#-usage) • [CLI](#-command-line) • [Contributing](#-contributing)

</div>

---

imgclean is a python library that helps you quickly clean image datasets by detecting and removing:
-  **duplicate images** (including near-duplicates using perceptual hashing)
-  **blurry images** (using laplacian variance)
-  **corrupted or unreadable files**
-  **images that don't meet size requirements**

## why imgclean?

when building machine learning models or managing large image collections, you often encounter:
- duplicate images wasting storage and skewing training data
- blurry or low-quality images reducing model performance  
- corrupted files causing pipeline failures
- images with wrong dimensions

**imgclean solves all of this in one line of code!**

##  quick start

### installation

```bash
pip install imgclean
```

or install from source:
```bash
git clone https://github.com/yourusername/imgclean.git
cd imgclean
pip install -e .
```

### basic usage

**python api:**

```python
from imgclean import ImageCleaner

# create a cleaner
cleaner = ImageCleaner()

# clean a directory
results = cleaner.clean("path/to/images", 
                       remove_duplicates=True,
                       remove_blurry=True,
                       blur_threshold=100)

print(f"Removed {results['removed']} images")
print(f"Kept {results['kept']} images")
```

**command line:**

```bash
# basic usage
imgclean path/to/images

# with options
imgclean path/to/images --remove-duplicates --remove-blurry --blur-threshold 100

# dry run (see what would be removed without actually removing)
imgclean path/to/images --dry-run
```

##  features

### duplicate detection
uses perceptual hashing to find duplicates and near-duplicates:
```python
cleaner.clean("images/", remove_duplicates=True, hash_size=8)
```

### blur detection
detects blurry images using laplacian variance:
```python
cleaner.clean("images/", remove_blurry=True, blur_threshold=100)
```

### corruption check
automatically removes corrupted or unreadable images:
```python
cleaner.clean("images/", remove_corrupted=True)
```

### size filtering
remove images that are too small or too large:
```python
cleaner.clean("images/", 
             min_width=100, 
             min_height=100,
             max_width=5000,
             max_height=5000)
```

##  get detailed reports

```python
results = cleaner.clean("images/", remove_duplicates=True, remove_blurry=True)

print(results)
# {
#     'kept': 850,
#     'removed': 150,
#     'duplicates': 100,
#     'blurry': 30,
#     'corrupted': 20,
#     'report': [...list of removed files with reasons...]
# }
```

##  advanced options

```python
from imgclean import ImageCleaner

cleaner = ImageCleaner()

results = cleaner.clean(
    "path/to/images",
    
    # duplicate detection
    remove_duplicates=True,
    hash_size=8,  # smaller = more sensitive
    
    # blur detection
    remove_blurry=True,
    blur_threshold=100,  # higher = more strict
    
    # corruption check
    remove_corrupted=True,
    
    # size constraints
    min_width=100,
    min_height=100,
    max_width=5000,
    max_height=5000,
    
    # output
    output_dir=None,  # copy good images to new directory
    dry_run=False,  # preview without deleting
    verbose=True,  # show progress bar
)
```

##  Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

##  license

mit license - feel free to use this in your projects!

##  star history

if you find this useful, please star the repo! it helps others discover the project.

##  performance

imgclean is fast! here's what you can expect:
- **1,000 images**: ~10 seconds
- **10,000 images**: ~2 minutes  
- **100,000 images**: ~20 minutes

*performance varies based on image size and enabled features*

##  use cases

- **ml dataset preparation**: clean training data before model training
- **photography**: organize and deduplicate photo collections
- **web scraping**: clean downloaded image datasets
- **research**: prepare datasets for computer vision research
- **storage optimization**: remove duplicates to save disk space

##  contributing

contributions are welcome! here's how you can help:

1. fork the repository
2. create a feature branch (`git checkout -b feature/amazing-feature`)
3. commit your changes (`git commit -m 'add amazing feature'`)
4. push to the branch (`git push origin feature/amazing-feature`)
5. open a pull request

please make sure to:
- add tests for new features
- update documentation
- follow the existing code style
- keep commits atomic and messages clear

##  found a bug?

please [open an issue](https://github.com/yourusername/imgclean/issues) with:
- a clear description of the bug
- steps to reproduce
- expected vs actual behavior
- your environment (os, python version, imgclean version)

##  get help

- 📖 [documentation](https://github.com/yourusername/imgclean)
-  [discussions](https://github.com/yourusername/imgclean/discussions)
-  [issues](https://github.com/yourusername/imgclean/issues)

##  show your support

if imgclean helped you, please:
-  star this repo
-  [tweet about it](https://twitter.com/intent/tweet?text=Check%20out%20imgclean%20-%20easily%20clean%20image%20datasets!&url=https://github.com/yourusername/imgclean)
-  write a blog post
-  tell your friends

##  acknowledgments

built with:
- [pillow](https://python-pillow.org/) - image processing
- [opencv](https://opencv.org/) - blur detection  
- [imagehash](https://github.com/JohannesBuchner/imagehash) - perceptual hashing
- [tqdm](https://github.com/tqdm/tqdm) - progress bars

##  stats

![GitHub stars](https://img.shields.io/github/stars/yourusername/imgclean?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/imgclean?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/yourusername/imgclean?style=social)

---

<div align="center">
made with  for the computer vision community
</div>
