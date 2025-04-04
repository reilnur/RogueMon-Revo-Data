#!/usr/bin/env python3
"""
Pokémon Evolution Chain Filter

This script filters a randomized evolution data file to only show evolutions for a specific type
of starter Pokémon and their subsequent evolution chains.

Usage:
    python evolution_filter.py --evo_file <path_to_evo_file> --starter_file <path_to_starter_file> --output <output_file>

Example:
    python evolution_filter.py --evo_file revo3000.txt --starter_file dragon_starters.txt --output dragon_evolution_chains.txt
"""

import re
import argparse
from collections import defaultdict

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Filter Pokémon evolution data based on a starter type file.')
    parser.add_argument('--evo_file', required=True, help='Path to the evolution data file')
    parser.add_argument('--starter_file', required=True, help='Path to the starter Pokémon file')
    parser.add_argument('--output', required=True, help='Path to the output file')
    return parser.parse_args()

def read_starter_pokemon(filepath):
    """Read the starter Pokémon from the given file."""
    with open(filepath, 'r') as f:
        return {line.strip() for line in f if line.strip()}

def parse_evolution_data(filepath):
    """
    Parse the evolution data file and return a dictionary mapping 
    Pokémon to their evolutions and frequencies.
    """
    evolution_data = {}
    current_pokemon = None
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Check if line starts with a Pokémon name followed by "->"
            match = re.match(r'^(\w+(?:\d+)?(?:\w+)?)(?:\s+->)(.+)$', line)
            if match:
                current_pokemon = match.group(1)
                evolutions_data = match.group(2).strip()
                
                # Parse the evolutions data
                evolutions = []
                for evo_match in re.finditer(r'\(([^,]+), (\d+)\)', evolutions_data):
                    evolution_name = evo_match.group(1)
                    frequency = int(evo_match.group(2))
                    evolutions.append((evolution_name, frequency))
                
                evolution_data[current_pokemon] = evolutions
    
    return evolution_data

def build_evolution_chains(starter_pokemon, evolution_data):
    """
    Build complete evolution chains starting from the starter Pokémon.
    Returns a set of all Pokémon in the evolution chains.
    """
    evolution_chain = set(starter_pokemon)
    to_check = list(starter_pokemon)
    checked = set()
    
    while to_check:
        current = to_check.pop(0)
        
        if current in checked or current not in evolution_data:
            continue
            
        checked.add(current)
        
        for evolution, _ in evolution_data[current]:
            evolution_chain.add(evolution)
            if evolution not in checked:
                to_check.append(evolution)
    
    return evolution_chain

def filter_evolution_data(evolution_data, evolution_chain):
    """
    Filter the evolution data to only include Pokémon in the evolution chain.
    """
    filtered_data = {}
    for pokemon, evolutions in evolution_data.items():
        if pokemon in evolution_chain:
            filtered_data[pokemon] = evolutions
    
    return filtered_data

def generate_output(filtered_data, output_file):
    """Generate the output file with the filtered evolution data."""
    with open(output_file, 'w') as f:
        f.write("# Filtered Evolution Chains\n\n")
        
        for pokemon, evolutions in sorted(filtered_data.items()):
            evolution_str = ", ".join([f"({name}, {freq})" for name, freq in evolutions])
            f.write(f"{pokemon} -> {evolution_str}\n")

def main():
    args = parse_arguments()
    
    # Read starter Pokémon
    starter_pokemon = read_starter_pokemon(args.starter_file)
    
    # Parse evolution data
    evolution_data = parse_evolution_data(args.evo_file)
    
    # Build evolution chains
    evolution_chain = build_evolution_chains(starter_pokemon, evolution_data)
    
    # Filter evolution data
    filtered_data = filter_evolution_data(evolution_data, evolution_chain)
    
    # Generate output
    generate_output(filtered_data, args.output)
    
    print(f"Found {len(starter_pokemon)} starter Pokémon")
    print(f"Total Pokémon in evolution chains: {len(evolution_chain)}")
    print(f"Filtered evolution data written to {args.output}")

if __name__ == "__main__":
    main()
