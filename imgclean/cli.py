import argparse
from .cleaner import ImageCleaner


def main():
    parser = argparse.ArgumentParser(
        description="Clean image datasets by removing duplicates, blurry images, and corrupted files"
    )
    
    parser.add_argument(
        "input_dir",
        help="Directory containing images to clean"
    )
    
    parser.add_argument(
        "--no-duplicates",
        action="store_true",
        help="Skip duplicate detection"
    )
    
    parser.add_argument(
        "--no-blur",
        action="store_true",
        help="Skip blur detection"
    )
    
    parser.add_argument(
        "--no-corrupted",
        action="store_true",
        help="Skip corrupted file detection"
    )
    
    parser.add_argument(
        "--hash-size",
        type=int,
        default=8,
        help="Hash size for duplicate detection (default: 8)"
    )
    
    parser.add_argument(
        "--blur-threshold",
        type=float,
        default=100.0,
        help="Threshold for blur detection (default: 100.0)"
    )
    
    parser.add_argument(
        "--min-width",
        type=int,
        help="Minimum image width"
    )
    
    parser.add_argument(
        "--min-height",
        type=int,
        help="Minimum image height"
    )
    
    parser.add_argument(
        "--max-width",
        type=int,
        help="Maximum image width"
    )
    
    parser.add_argument(
        "--max-height",
        type=int,
        help="Maximum image height"
    )
    
    parser.add_argument(
        "--output-dir",
        help="Copy clean images to this directory instead of deleting"
    )
    
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without actually removing"
    )
    
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress progress output"
    )
    
    args = parser.parse_args()
    
    cleaner = ImageCleaner()
    
    results = cleaner.clean(
        input_dir=args.input_dir,
        remove_duplicates=not args.no_duplicates,
        remove_blurry=not args.no_blur,
        remove_corrupted=not args.no_corrupted,
        hash_size=args.hash_size,
        blur_threshold=args.blur_threshold,
        min_width=args.min_width,
        min_height=args.min_height,
        max_width=args.max_width,
        max_height=args.max_height,
        output_dir=args.output_dir,
        dry_run=args.dry_run,
        verbose=not args.quiet,
    )


if __name__ == "__main__":
    main()
