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
    # for key, value in data.items():

    #     # Case 1: If value is a list, check if target matches an item in the list
    #     if isinstance(value, list):
    #         for item in value:
    #             # if isinstance(item, str) and item.strip().lower() ==  target:
    #             if isinstance(item, str) and item.strip().lower() ==  target:
    #                 paths.append(f"{current_path}{key} -> {item}")
    #             elif isinstance(item, dict):
    #                 for sub_key, sub_value in item.items():
    #                     # if sub_key.strip().lower() == target:
    #                     if sub_key.strip().lower() == target:
    #                         paths.append(f"{current_path}{key} -> {sub_key}")
    #                     else:
    #                         # Recurse into the nested dictionary
    #                         sub_paths = find_category_path({sub_key: sub_value}, target, f"{current_path}{key} -> ")
    #                         paths.extend(sub_paths)

    #     # Case 2: If value is a dictionary, check if target matches a key or recurse
    #     elif isinstance(value, dict):
    #         sub_paths = find_category_path(value, target, f"{current_path}{key} -> ")
    #         paths.extend(sub_paths)

    #     # Case 3: Direct key-value match as a string (e.g., {"Belgian": "Flemish"})
    #     elif isinstance(value, str) and value.strip().lower() == target:
    #         paths.append(f"{current_path}{key} -> {value}")
    # return paths


# Main function to get paths for each input category
def get_category_paths(inputs):
    
    try:
        result = [find_category_hierarchy(category) for category in inputs]
        return result
    except Exception as e:
        return 'Error in formating categories: {e}'
    # output_paths = []
    # for category in inputs:
    #     paths = []
    #     for main_category, subcategories in category_data.items():
    #         # For each input, find all matching paths
    #         paths.extend(find_category_path({main_category: subcategories}, category))
    #     # If paths are found, add to output
    #     if paths:
    #         output_paths.extend(paths)
    #     else:
    #         output_paths.append(f"Category '{category}' not found")
    # return output_paths

# Example Inputs
# input_categories1 = ['chicken shop', 'Books, Mags, Music & Video', 'Seafood']
# input_categories2 = ['Salvadoran', 'Coffee & Tea']
# input_categories3 = ['Martial Arts', 'Haunted Houses', 'Mountain Huts', 'Audio/Visual Equipment Rental']

# # Run the function with example inputs
# output1 = get_category_paths(input_categories1)
# output2 = get_category_paths(input_categories2)
# output3 = get_category_paths(input_categories3)

# # Print results
# print("Output for input 1:", output1)
# print("Output for input 2:", output2)
# print("output 3: ", output3)

#Expected output
# Output for input 1: ['Restaurants->Chicken Shop', 'Shopping->Books, Mags, Music & Video', 'Restaurants->Seafood']
# Output for input 2: ['Restaurants->Latin American->Salvadoran', 'Food->Coffee & Tea']
# output 3:  ['Active Life->Fitness & Instruction->Martial Arts', 'Arts & Entertainment->Haunted Houses', 'Event Planning & Services->Hotels->Mountain Huts', 'Event Planning & Services->Party Equipment Rentals->Audio/Visual Equipment Rental']
