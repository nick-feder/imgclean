from imgclean import ImageCleaner

cleaner = ImageCleaner()

results = cleaner.clean(
    "path/to/images",
    remove_duplicates=True,
    remove_blurry=True,
    blur_threshold=100
)

print(f"Removed {results['removed']} images")
print(f"Kept {results['kept']} images")
print(f"  - Duplicates: {results['duplicates']}")
print(f"  - Blurry: {results['blurry']}")
print(f"  - Corrupted: {results['corrupted']}")
