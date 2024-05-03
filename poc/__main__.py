import json

from navigation import Navigation
from tree_node import TreeNode

if __name__ == "__main__":

    # Load tree structure from JSON file
    with open('tree.json', 'r') as tree_file:
        tree_structure = json.load(tree_file)

    # Build tree from JSON structure
    tree_nodes = TreeNode.build_tree_from_dict(tree_structure)

    # Start navigation
    print("Task: You wish to read about Winston Churchill. Where should you navigate to?")
    print(Navigation(tree_nodes).start())
