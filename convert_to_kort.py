import json
import sys


def convert_to_kort(data):
    """
    Convert hierarchical tree structure to Kort-compatible format.

    Args:
        data (dict): Hierarchical tree structure.

    Returns:
        list: Kort-compatible tree structure.
    """
    result = []
    for key, value in data.items():
        item = {"text": key}
        if isinstance(value, dict):
            item["children"] = convert_to_kort(value)
        elif isinstance(value, list):
            item["children"] = value
        result.append(item)
    return result


if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python convert_to_kort.py <json_file> [<output_format>]")
        print("output_format (optional): '--pretty' for pretty-printed format, '--compact' for compact format")
        sys.exit(1)

    json_file = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) == 3 else '--pretty'

    try:
        # Load tree structure from JSON file
        with open(json_file, 'r') as tree_file:
            tree_structure = json.load(tree_file)
    except FileNotFoundError:
        print(f"Error: File '{json_file}' not found.")
        sys.exit(1)

    # Convert tree structure to Kort-compatible format
    converted_data = convert_to_kort(tree_structure)

    # Print converted data to copy and paste into Kort's MongoDB database directly
    if output_format == '--compact':
        print(json.dumps(converted_data, separators=(',', ':')))
    elif output_format == '--pretty':
        print(json.dumps(converted_data, indent=2))
    else:
        print("Error: Invalid output format. Use 'pretty' or 'compact'.")
