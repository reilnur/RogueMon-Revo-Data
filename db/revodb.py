import sqlite3
import re
import os

# Input file and database
input_filename = "PatchRevoData.txt"
db_filename = "evolutions.db"

# Verify input file exists
if not os.path.exists(input_filename):
    print(f"Error: Input file '{input_filename}' not found in {os.getcwd()}")
    exit(1)

# Connect to SQLite database (creates/overwrites evolutions.db)
conn = sqlite3.connect(db_filename)
cursor = conn.cursor()

# Drop existing table (if any) and create new one
cursor.execute("DROP TABLE IF EXISTS evolutions")
cursor.execute("""
    CREATE TABLE evolutions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        pokemon TEXT,
        evolves_to TEXT,
        count INTEGER,
        percentage REAL
    )
""")

# Parse PatchRevoData.txt
def parse_patch_file(file_path):
    records = []
    errors = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            errors.append(f"Line {i}: Skipped (empty)")
            continue
        
        # Match Pokémon -> (EvolvesTo, Count, Percentage), ...
        match = re.match(r'(.+?)\s*->\s*(.*)', line)
        if not match:
            errors.append(f"Line {i}: Skipped (invalid format, no '->' found): {line}")
            continue
        
        pokemon = match.group(1).strip()
        evolution_str = match.group(2).strip()
        
        if not pokemon:
            errors.append(f"Line {i}: Skipped (empty Pokémon name)")
            continue
        
        # Match (EvolvesTo, Count, Percentage) triples
        evolution_triples = re.findall(r'\(([^,]+),\s*(\d+),\s*([\d.]+)\)', evolution_str)
        
        if not evolution_triples:
            errors.append(f"Line {i}: No valid evolution triples found in '{evolution_str}'")
            continue
        
        # Validate and collect records
        for evolves_to, count, percentage in evolution_triples:
            evolves_to = evolves_to.strip()
            try:
                count = int(count)
                percentage = float(percentage)
                if not evolves_to:
                    errors.append(f"Line {i}: Skipped evolution for {pokemon} (empty evolves_to)")
                    continue
                if count <= 0:
                    errors.append(f"Line {i}: Skipped evolution for {pokemon} -> {evolves_to} (invalid count: {count})")
                    continue
                if percentage < 0 or percentage > 100:
                    errors.append(f"Line {i}: Skipped evolution for {pokemon} -> {evolves_to} (invalid percentage: {percentage})")
                    continue
                records.append((pokemon, evolves_to, count, percentage))
            except ValueError as e:
                errors.append(f"Line {i}: Skipped evolution for {pokemon} -> {evolves_to} (invalid count or percentage: {count}, {percentage}, error: {e})")
                continue
    
    return records, errors

# Parse the file and insert records
records, errors = parse_patch_file(input_filename)

# Log any errors
if errors:
    print(f"Found {len(errors)} issues during validation:")
    for error in errors:
        print(error)
else:
    print("No validation issues found")

# Insert records into database
if records:
    cursor.executemany("""
        INSERT INTO evolutions (pokemon, evolves_to, count, percentage)
        VALUES (?, ?, ?, ?)
    """, records)
    conn.commit()
    print(f"Inserted {len(records)} records into {db_filename}")
else:
    print("No valid records to insert into database")

# Close connection
conn.close()