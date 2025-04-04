If you want to use these scripts to generate your own reports:

1. Use extract_lines.py to get the random evos section (lines 8-585)
2. Use standardize_seps.py to turn all "," and " and " into "|" (this made it way easier to parse branched evos)
3. Use evolution_analyzer.py to get the resulting report on evo frequencies

You may also then use evolution_chain_filter.py to filter for starters of a particular type and their possible evo chains.
