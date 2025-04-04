import os
import glob

def extract_lines(input_file, output_file, start_line=8, end_line=585):
    """
    Extract specific lines from a text file and write them to a new file.
    
    Args:
        input_file (str): Path to the input file
        output_file (str): Path to the output file
        start_line (int): First line to extract (1-based indexing)
        end_line (int): Last line to extract (1-based indexing)
    """
    try:
        with open(input_file, 'r', encoding='utf-8') as f_in:
            # Read all lines and convert to list
            lines = f_in.readlines()
            
            # Python uses 0-based indexing, so adjust line numbers
            start_idx = start_line - 1
            end_idx = min(end_line, len(lines))
            
            # Extract the desired lines
            selected_lines = lines[start_idx:end_idx]
            
            # Write to output file
            with open(output_file, 'w', encoding='utf-8') as f_out:
                f_out.writelines(selected_lines)
                
        print(f"Processed {input_file} -> {output_file}")
        
    except Exception as e:
        print(f"Error processing {input_file}: {e}")

def process_files(input_pattern, output_dir=None):
    """
    Process all files matching the input pattern.
    
    Args:
        input_pattern (str): Glob pattern to match input files
        output_dir (str, optional): Directory for output files. If None, 
                                   files will be created in the same directory as input
    """
    # Create output directory if specified and doesn't exist
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Get all matching files
    input_files = glob.glob(input_pattern)
    
    if not input_files:
        print(f"No files found matching pattern: {input_pattern}")
        return
    
    for input_file in input_files:
        # Generate output filename
        base_name = os.path.basename(input_file)
        if output_dir:
            output_file = os.path.join(output_dir, f"extracted_{base_name}")
        else:
            output_file = os.path.join(os.path.dirname(input_file), f"extracted_{base_name}")
        
        # Process the file
        extract_lines(input_file, output_file)

# Example usage
if __name__ == "__main__":
    # Change these parameters as needed
    input_pattern = "*.log"  # Process all .txt files in current directory
    output_directory = "extracted_files"  # Put results in this directory
    
    process_files(input_pattern, output_directory)