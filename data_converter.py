import json
from slugify import slugify  # Correct import for slugify

# Input and output file paths
input_file_path = "output3.json"  # Replace with the actual path to your input file
output_file_path = "output3_updated.json"  # Replace with your desired output file path

# Load the original JSON data
with open(input_file_path, 'r') as file:
    original_data = json.load(file)

# Update each entry's source_url with the new format
for entry in original_data:
    company_slug = slugify(entry.get('company', 'unknown-company'))
    title_slug = slugify(entry.get('title', 'unknown-role'))
    entry['source_url'] = f"https://au.prosple.com/graduate-employers/{company_slug}/jobs-internships/{title_slug}"

# Save the updated JSON data
with open(output_file_path, 'w') as file:
    json.dump(original_data, file, indent=4)

print(f"Updated file saved to: {output_file_path}")
