from imgclean import ImageCleaner

cleaner = ImageCleaner()

results = cleaner.clean(
    "path/to/images",
    remove_duplicates=True,
    remove_blurry=True,
    remove_corrupted=True,
    hash_size=8,
    blur_threshold=100,
    min_width=100,
    min_height=100,
    max_width=5000,
    max_height=5000,
    output_dir="path/to/clean_images",
    dry_run=False,
    verbose=True,
)

print(results)
