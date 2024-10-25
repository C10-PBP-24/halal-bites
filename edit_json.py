import json

# Load the resto.json file
with open('resto/fixtures/resto.json', 'r') as file:
    resto_data = json.load(file)

# Update each entry in the resto data
for entry in resto_data:
    if entry['model'] == 'resto.resto':
        # Check if makanan is a dictionary and contains the expected 'id'
        if isinstance(entry['fields'].get('makanan'), dict) and 'id' in entry['fields']['makanan']:
            # Set makanan to the ID value
            entry['fields']['makanan'] = entry['pk']

# Save the updated data back to resto.json
with open('resto.json', 'w') as file:
    json.dump(resto_data, file, indent=2)

print("The 'resto.json' data has been successfully updated.")
