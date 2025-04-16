import csv
import os
import re
import codecs

def csv_to_vdf(csv_file, vdf_file, output_vdf_file=None):
    """
    Convert CSV file to VDF format
    
    Parameters:
    csv_file: Path to the CSV file
    vdf_file: Path to the original VDF file
    output_vdf_file: Path to the output VDF file, if not specified will overwrite the original file
    """
    # Read CSV file, try to handle BOM
    try:
        # First try to read with UTF-8-SIG (handles BOM)
        with codecs.open(csv_file, 'r', encoding='utf-8-sig') as f:
            reader = csv.reader(f)
            headers = next(reader)  # Get header row
            rows = list(reader)  # Read all remaining rows
    except Exception as e:
        print(f"Failed to read with UTF-8-SIG: {e}")
        # If failed, use standard UTF-8
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            headers = next(reader)
            rows = list(reader)
    
    # Display header fields for debugging
    print(f"CSV header fields: {headers}")
    
    # Process header row to ensure correct comparison
    headers = [h.strip() for h in headers]
    
    # Find the ID column index
    id_column_index = -1
    for i, header in enumerate(headers):
        print(f"Checking header {i}: '{header}' if it's 'ID'")
        if header.lower() == 'id':
            id_column_index = i
            print(f"Found ID column at index {i}")
            break
    
    if id_column_index == -1:
        # If 'ID' column not found, use first column as ID
        id_column_index = 0
        print(f"ID column not found, using first column '{headers[0]}' as ID")
    
    # Identify language columns
    language_columns = {}
    for i, header in enumerate(headers):
        if i != id_column_index and header.strip():
            # Convert header names to lowercase for matching in VDF file
            language_columns[header.lower()] = i
    
    print(f"Identified language columns: {language_columns}")
    
    # Initialize translation data structure
    translations = {}
    for lang in language_columns.keys():
        translations[lang] = {}
    
    # Read each row of translation data
    for row in rows:
        if len(row) <= id_column_index:
            continue  # Skip incomplete rows
            
        id_key = row[id_column_index].strip()
        if not id_key:
            continue  # Skip empty IDs
            
        # Read translations for each language
        for lang, col_index in language_columns.items():
            if col_index < len(row):
                translation = row[col_index].strip()
                translations[lang][id_key] = translation
    
    # Read VDF file
    with open(vdf_file, 'r', encoding='utf-8') as f:
        vdf_content = f.read()
    
    # Store updated VDF content
    updated_vdf_content = vdf_content
    
    # Update translations for each language
    for lang, translations_dict in translations.items():
        # Find language block
        lang_pattern = re.compile(fr'"{lang}"\s*\n\s*{{\s*\n\s*"Tokens"\s*\n\s*{{(.*?)}}\s*\n\s*}}', re.DOTALL)
        lang_match = lang_pattern.search(vdf_content)
        
        if not lang_match:
            print(f"Warning: Language '{lang}' not found in VDF")
            continue
        
        lang_tokens = lang_match.group(1)
        updated_tokens = lang_tokens
        
        # Update each translation item
        updated_count = 0
        for id_key, translation in translations_dict.items():
            # Find existing translation item
            token_pattern = re.compile(fr'"{re.escape(id_key)}"\s*"(.*?)"')
            token_match = token_pattern.search(updated_tokens)
            
            if token_match:
                # Update existing translation
                updated_tokens = token_pattern.sub(f'"{id_key}"\t"{translation}"', updated_tokens)
                updated_count += 1
            else:
                # Print not found IDs in Debug mode
                print(f"ID '{id_key}' not found in VDF")
        
        print(f"Updated {updated_count} translations for language '{lang}'")
        
        # Update language block in VDF content
        updated_vdf_content = lang_pattern.sub(f'"{lang}"\n\t{{\n\t\t"Tokens"\n\t\t{{{updated_tokens}}}\n\t}}', updated_vdf_content)
    
    # Output updated VDF file
    output_file = output_vdf_file if output_vdf_file else vdf_file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_vdf_content)
    
    print(f"VDF file updated: {output_file}")
    print(f"Successfully converted CSV file '{csv_file}' to VDF file '{output_file}'")

if __name__ == "__main__":
    # Get current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Default file paths
    default_csv_file = os.path.join(current_dir, "Localization.csv")
    default_vdf_file = os.path.join(current_dir, "loc_all.vdf")
    default_output_file = os.path.join(current_dir, "loc_all_update.vdf")
    
    # Get file paths from command line arguments or use defaults
    import sys
    csv_file = sys.argv[1] if len(sys.argv) > 1 else default_csv_file
    vdf_file = sys.argv[2] if len(sys.argv) > 2 else default_vdf_file
    output_file = sys.argv[3] if len(sys.argv) > 3 else default_output_file
    
    # Execute conversion
    try:
        csv_to_vdf(csv_file, vdf_file, output_file)
    except Exception as e:
        print(f"Error: {e}")