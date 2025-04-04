#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

def process_file(file_path, dry_run=False):
    """
    Process a single file to replace ", " and " and " with "|".
    
    Args:
        file_path: Path to the file to process
        dry_run: If True, don't actually modify files, just print what would be done
    
    Returns:
        Tuple of (number of comma replacements, number of 'and' replacements)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Count original occurrences
        comma_count = content.count(', ')
        and_count = content.count(' and ')
        
        # Replace ", " and " and " with "|"
        modified_content = re.sub(r', ', '|', content)
        modified_content = re.sub(r' and ', '|', modified_content)
        
        if not dry_run and (comma_count > 0 or and_count > 0):
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(modified_content)
        
        return comma_count, and_count
    
    except Exception as e:
        print(f"Error processing {file_path}: {str(e)}")
        return 0, 0

def process_directory(directory_path, extension='.log', dry_run=False):
    """
    Process all files with the given extension in the directory.
    
    Args:
        directory_path: Path to the directory containing files to process
        extension: File extension to filter by
        dry_run: If True, don't actually modify files, just print what would be done
    """
    total_files = 0
    total_comma_replacements = 0
    total_and_replacements = 0
    
    directory = Path(directory_path)
    
    for file_path in directory.glob(f'*{extension}'):
        comma_count, and_count = process_file(file_path, dry_run)
        
        action = "Would replace" if dry_run else "Replaced"
        if comma_count > 0 or and_count > 0:
            print(f"{action} in {file_path.name}: {comma_count} commas, {and_count} 'and's")
        
        total_files += 1
        total_comma_replacements += comma_count
        total_and_replacements += and_count
    
    print(f"\nProcessed {total_files} files with extension '{extension}'")
    print(f"Total replacements: {total_comma_replacements} commas, {total_and_replacements} 'and's")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Replace ', ' and ' and ' in evolution data files")
    parser.add_argument('--directory', default='.', help='Directory containing the files to process (default: current directory)')
    parser.add_argument('--ext', default='.log', help='File extension to process (default: .log)')
    parser.add_argument('--dry-run', action='store_true', help='Perform a dry run without modifying files')
    
    args = parser.parse_args()
    
    print(f"{'DRY RUN - ' if args.dry_run else ''}Processing files in {args.directory}")
    process_directory(args.directory, args.ext, args.dry_run)
