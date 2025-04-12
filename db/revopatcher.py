import re
import os

# Input and output files
input_filename = "revo12000.txt"
output_filename = "PatchRevoData.txt"

# Verify input file exists
if not os.path.exists(input_filename):
    print(f"Error: Input file '{input_filename}' not found in {os.getcwd()}")
    exit(1)

# Parse and validate the input file
def parse_and_validate_evolutions(file_path):
    records = []
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            errors.append(f"Line {i}: Skipped (empty)")
            continue
        
        # Debug: Print raw line to check for hidden characters
        # print(f"Line {i} (raw): {repr(line)}")
        
        # Match Pokémon name and evolution list with stricter '->' handling
        # Use a more explicit regex to avoid edge cases
        match = re.match(r'(.+?)\s*->\s*(.*)', line)
        if not match:
            errors.append(f"Line {i}: Skipped (invalid format, no '->' found): {line}")
            continue
        
        pokemon = match.group(1).strip()
        evolution_str = match.group(2).strip()
        
        # Debug: Print parsed groups
        # print(f"Line {i}: Pokémon='{pokemon}', EvolutionStr='{evolution_str}'")
        
        if not pokemon:
            errors.append(f"Line {i}: Skipped (empty Pokémon name)")
            continue
        
        # Match (EvolvesTo, Count) pairs, allowing complex names
        evolution_pairs = re.findall(r'\(([^,]+),\s*(\d+)\)', evolution_str)
        
        if not evolution_pairs:
            errors.append(f"Line {i}: No valid evolution pairs found in '{evolution_str}'")
            continue
        
        # Validate and collect counts for this Pokémon
        pokemon_evolutions = []
        for evolves_to, count in evolution_pairs:
            evolves_to = evolves_to.strip()
            try:
                count = int(count)
                if not evolves_to:
                    errors.append(f"Line {i}: Skipped evolution for {pokemon} (empty evolves_to)")
                    continue
                if count <= 0:
                    errors.append(f"Line {i}: Skipped evolution for {pokemon} -> {evolves_to} (invalid count: {count})")
                    continue
                pokemon_evolutions.append((evolves_to, count))
            except ValueError:
                errors.append(f"Line {i}: Skipped evolution for {pokemon} -> {evolves_to} (invalid count: {count})")
                continue
        
        if not pokemon_evolutions:
            errors.append(f"Line {i}: No valid evolutions for {pokemon}")
            continue
        
        # Calculate total count for percentage
        total_count = sum(count for _, count in pokemon_evolutions)
        if total_count == 0:
            errors.append(f"Line {i}: Skipped {pokemon} (total count is zero)")
            continue
        
        # Calculate percentages and create record
        for evolves_to, count in pokemon_evolutions:
            percentage = (count / total_count) * 100
            percentage = round(percentage, 2)
            records.append((pokemon, evolves_to, count, percentage))
    
    return records, errors

# Write to output file
def write_patched_file(records, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        current_pokemon = None
        evolution_list = []
        
        for pokemon, evolves_to, count, percentage in sorted(records):
            if pokemon != current_pokemon:
                if evolution_list:
                    f.write(f"{current_pokemon} -> {', '.join(evolution_list)}\n")
                current_pokemon = pokemon
                evolution_list = []
            evolution_list.append(f"({evolves_to}, {count}, {percentage})")
        
        if evolution_list:
            f.write(f"{current_pokemon} -> {', '.join(evolution_list)}\n")

# Process the file
records, errors = parse_and_validate_evolutions(input_filename)

# Log any errors
if errors:
    print(f"Found {len(errors)} issues during validation:")
    for error in errors:
        print(error)
else:
    print("No validation issues found")

# Write to PatchRevoData.txt
if records:
    write_patched_file(records, output_filename)
    print(f"Created {output_filename} with {len(records)} evolution records")
else:
    print("No valid records to write to output file")