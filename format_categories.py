import json

# Load JSON structure
with open('categories_listing.json', 'r') as file:
    category_data = json.load(file)

category_dict = {category["alias"].lower(): category for category in category_data}
# Function to recursively search and build path
def find_category_hierarchy(target):
    target = target.lower()

    current_category = next((category for category in category_dict.values() if category["title"].lower() == target), None)
    hierarchy_list = []

    while current_category:
        hierarchy_list.insert(0,current_category["title"])
        parent_alias = current_category["parent_aliases"].lower() if current_category["parent_aliases"] else None
        current_category = category_dict.get(parent_alias) if parent_alias else None
    return '->'.join(hierarchy_list)


# Main function to get paths for each input category
def get_category_paths(inputs):
    
    try:
        result = [find_category_hierarchy(category) for category in inputs]
        return result
    except Exception as e:
        return 'Error in formating categories: {e}'