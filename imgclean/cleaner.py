import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from collections import defaultdict

import cv2
import numpy as np
from PIL import Image
import imagehash
from tqdm import tqdm


class ImageCleaner:
    SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'}
    
    def __init__(self):
        # keep track of hashes we've seen before
        self.hash_cache = {}
        
    def clean(
        self,
        input_dir: str,
        remove_duplicates: bool = True,
        remove_blurry: bool = True,
        remove_corrupted: bool = True,
        hash_size: int = 8,
        blur_threshold: float = 100.0,
        min_width: Optional[int] = None,
        min_height: Optional[int] = None,
        max_width: Optional[int] = None,
        max_height: Optional[int] = None,
        output_dir: Optional[str] = None,
        dry_run: bool = False,
        verbose: bool = True,
    ) -> Dict:
        input_path = Path(input_dir)
        if not input_path.exists():
            raise ValueError(f"Input directory does not exist: {input_dir}")
        
        image_files = self._get_image_files(input_path)
        
        if verbose:
            print(f"Found {len(image_files)} images")
        
        results = {
            'kept': 0,
            'removed': 0,
            'duplicates': 0,
            'blurry': 0,
            'corrupted': 0,
            'size_filtered': 0,
            'report': []
        }
        
        to_remove = set()
        
        if remove_corrupted:
            corrupted = self._find_corrupted(image_files, verbose)
            to_remove.update(corrupted)
            results['corrupted'] = len(corrupted)
        
        valid_files = [f for f in image_files if f not in to_remove]
        
        if remove_duplicates:
            duplicates = self._find_duplicates(valid_files, hash_size, verbose)
            to_remove.update(duplicates)
            results['duplicates'] = len(duplicates)
        
        valid_files = [f for f in valid_files if f not in to_remove]
        
        if remove_blurry:
            blurry = self._find_blurry(valid_files, blur_threshold, verbose)
            to_remove.update(blurry)
            results['blurry'] = len(blurry)
        
        valid_files = [f for f in valid_files if f not in to_remove]
        
        if any([min_width, min_height, max_width, max_height]):
            size_filtered = self._filter_by_size(
                valid_files, min_width, min_height, max_width, max_height, verbose
            )
            to_remove.update(size_filtered)
            results['size_filtered'] = len(size_filtered)
        
        results['removed'] = len(to_remove)
        results['kept'] = len(image_files) - results['removed']
        
        if output_dir:
            self._copy_to_output(
                [f for f in image_files if f not in to_remove],
                output_dir,
                verbose
            )
        elif not dry_run:
            self._remove_files(to_remove, verbose)
        
        if dry_run and verbose:
            print(f"\nDry run complete - no files were deleted")
            print(f"Would remove {results['removed']} files:")
            print(f"  - Duplicates: {results['duplicates']}")
            print(f"  - Blurry: {results['blurry']}")
            print(f"  - Corrupted: {results['corrupted']}")
            print(f"  - Size filtered: {results['size_filtered']}")
        elif verbose:
            print(f"\nCleaning complete!")
            print(f"Kept: {results['kept']}")
            print(f"Removed: {results['removed']}")
        
        return results
    
    def _get_image_files(self, directory: Path) -> List[Path]:
        image_files = []
        for file_path in directory.rglob('*'):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_FORMATS:
                image_files.append(file_path)
        return image_files
    
    def _find_corrupted(self, files: List[Path], verbose: bool) -> List[Path]:
        corrupted = []
        iterator = tqdm(files, desc="Checking for corruption") if verbose else files
        
        for file_path in iterator:
            try:
                # need to open twice because verify() invalidates the image
                with Image.open(file_path) as img:
                    img.verify()
                with Image.open(file_path) as img:
                    img.load()
            except Exception:
                corrupted.append(file_path)
        
        return corrupted
    
    def _find_duplicates(self, files: List[Path], hash_size: int, verbose: bool) -> List[Path]:
        hash_dict = defaultdict(list)
        duplicates = []
        
        iterator = tqdm(files, desc="Finding duplicates") if verbose else files
        
        for file_path in iterator:
            try:
                with Image.open(file_path) as img:
                    img_hash = imagehash.phash(img, hash_size=hash_size)
                    hash_dict[img_hash].append(file_path)
            except Exception:
                continue
        
        # keep first image, mark rest as duplicates
        for img_hash, paths in hash_dict.items():
            if len(paths) > 1:
                duplicates.extend(paths[1:])
        
        return duplicates
    
    def _find_blurry(self, files: List[Path], threshold: float, verbose: bool) -> List[Path]:
        blurry = []
        iterator = tqdm(files, desc="Detecting blur") if verbose else files
        
        for file_path in iterator:
            try:
                image = cv2.imread(str(file_path))
                if image is None:
                    continue
                
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                # higher variance = sharper image
                laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                
                if laplacian_var < threshold:
                    blurry.append(file_path)
            except Exception:
                continue
        
        return blurry
    
    def _filter_by_size(
        self,
        files: List[Path],
        min_width: Optional[int],
        min_height: Optional[int],
        max_width: Optional[int],
        max_height: Optional[int],
        verbose: bool
    ) -> List[Path]:
        filtered = []
        iterator = tqdm(files, desc="Filtering by size") if verbose else files
        
        for file_path in iterator:
            try:
                with Image.open(file_path) as img:
                    width, height = img.size
                    
                    if min_width and width < min_width:
                        filtered.append(file_path)
                        continue
                    if min_height and height < min_height:
                        filtered.append(file_path)
                        continue
                    if max_width and width > max_width:
                        filtered.append(file_path)
                        continue
                    if max_height and height > max_height:
                        filtered.append(file_path)
                        continue
            except Exception:
                continue
        
        return filtered
    
    def _copy_to_output(self, files: List[Path], output_dir: str, verbose: bool):
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        iterator = tqdm(files, desc="Copying files") if verbose else files
        
        for file_path in iterator:
            dest = output_path / file_path.name
            counter = 1
            # add numbers if file already exists
            while dest.exists():
                stem = file_path.stem
                suffix = file_path.suffix
                dest = output_path / f"{stem}_{counter}{suffix}"
                counter += 1
            
            shutil.copy2(file_path, dest)
    
    def _remove_files(self, files: List[Path], verbose: bool):
        iterator = tqdm(files, desc="Removing files") if verbose else files
        
        for file_path in iterator:
            try:
                file_path.unlink()
            except Exception:
                pass
