import os
from collections import defaultdict

def parse_evolution_file(file_content):
    """
    Parse a single evolution log file and extract evolution data.
    
    Args:
        file_content (str): The content of the evolution log file
        
    Returns:
        dict: A dictionary mapping base Pokémon to a list of their evolved forms
    """
    evolution_data = {}
    lines = file_content.strip().split('\n')
    
    # Skip the header line (--Randomized Evolutions--)
    for line in lines[1:]:
        # Check if the line contains evolution data
        if "->" in line:
            # Split the line into base pokemon and evolutions
            parts = line.split("->")
            if len(parts) != 2:
                continue
                
            base_pokemon = parts[0].strip()
            evolutions_part = parts[1].strip()
            
            # Handle branching evolutions (separated by "|")
            evolutions = evolutions_part.split("|")
            
            # Store the evolutions for this base pokemon
            evolution_data[base_pokemon] = [evo.strip() for evo in evolutions]
    
    return evolution_data

def compile_evolution_frequencies(file_contents):
    """
    Compile evolution frequencies from multiple evolution log files.
    
    Args:
        file_contents (list): A list of file contents, each representing an evolution log
        
    Returns:
        dict: A nested dictionary tracking evolution frequencies
    """
    # Dictionary to store evolution frequencies
    # Structure: {base_pokemon: {branch_index: {evolved_pokemon: count}}}
    frequencies = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    
    for file_content in file_contents:
        evolution_data = parse_evolution_file(file_content)
        
        for base_pokemon, evolutions in evolution_data.items():
            for i, evolved_pokemon in enumerate(evolutions):
                # Increment count for this evolution path
                frequencies[base_pokemon][i][evolved_pokemon] += 1
    
    return frequencies

def generate_frequency_report(frequencies):
    """
    Generate a readable report of evolution frequencies.
    
    Args:
        frequencies (dict): The compiled evolution frequencies
        
    Returns:
        str: A formatted report showing evolution frequencies
    """
    report_lines = []
    
    for base_pokemon in sorted(frequencies.keys()):
        branches = frequencies[base_pokemon]
        
        for branch_index in sorted(branches.keys()):
            # For multi-branch evolutions, create numbered base pokemon
            if len(branches) > 1:
                branch_base = f"{base_pokemon}{branch_index+1}"
            else:
                branch_base = base_pokemon
            
            # Sort evolutions by frequency (descending)
            evolutions = branches[branch_index]
            sorted_evolutions = sorted(evolutions.items(), key=lambda x: x[1], reverse=True)
            
            # Format the evolutions list
            evolution_list = ", ".join([f"({evo}, {count})" for evo, count in sorted_evolutions])
            
            # Add the line to the report
            report_lines.append(f"{branch_base} -> {evolution_list}")
    
    return "\n".join(report_lines)

def process_evolution_files(directory_path):
    """
    Process all evolution log files in the specified directory.
    
    Args:
        directory_path (str): Path to the directory containing evolution logs
        
    Returns:
        str: A formatted report of evolution frequencies
    """
    file_contents = []
    
    # Read all .log files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.log') or filename.endswith('.gba.log'):
            with open(os.path.join(directory_path, filename), 'r') as f:
                file_contents.append(f.read())
    
    frequencies = compile_evolution_frequencies(file_contents)
    report = generate_frequency_report(frequencies)
    return report

def write_report_to_file(report, output_path):
    """
    Write the evolution frequency report to a file.
    
    Args:
        report (str): The formatted evolution frequency report
        output_path (str): Path where the report should be saved
    """
    with open(output_path, 'w') as f:
        f.write(report)
    print(f"Report successfully written to {output_path}")

# Example usage:
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python evolution_analyzer.py <input_directory> <output_file>")
        sys.exit(1)
    
    input_directory = sys.argv[1]
    output_file = sys.argv[2]
    
    report = process_evolution_files(input_directory)
    write_report_to_file(report, output_file)
