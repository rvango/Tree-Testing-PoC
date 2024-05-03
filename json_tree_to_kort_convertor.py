import json


def convert_to_list(data):
    result = []
    for key, value in data.items():
        item = {"text": key}
        if isinstance(value, dict):
            item["children"] = convert_to_list(value)
        elif isinstance(value, list):
            item["children"] = value
        result.append(item)
    return result


if __name__ == "__main__":
    with open('tree.json', 'r') as tree_file:
        tree_structure = json.load(tree_file)

    converted_data = convert_to_list(tree_structure)
    print(json.dumps(converted_data, indent=4))
