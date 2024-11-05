import json
import pandas as pd
with open('categories_listing.json', 'r') as file:
    category_data = json.load(file)

category_dict = {category["alias"].lower(): category for category in category_data}

def find_category_hierarchy(target):
    target = target.lower()
    hierarchy_list = []
    current_category = next((category for category in category_dict.values() if category["title"].lower() == target), None)
    while current_category:
        hierarchy_list.insert(0,current_category["title"])
        parent_alias = current_category["parent_aliases"].lower() if current_category["parent_aliases"] else None
        current_category = category_dict.get(parent_alias) if parent_alias else None
    return '->'.join(hierarchy_list), hierarchy_list[0]

formated_data = {}

for data in category_data:
    result, title = find_category_hierarchy(data["title"])

    if title in formated_data:
        formated_data[title].append(result)
    else:
        formated_data[title] = [result]

df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in formated_data.items()]))
df.to_csv('yelp_category_hierarchy.csv', index=False)  # Export to CSV
