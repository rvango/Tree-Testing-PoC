from dataclasses import dataclass

import datetime


@dataclass
class NavigationRecord:
    timestamp: datetime.datetime
    node_name: str

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.node_name}]"


class TreeNode:
    ROOT_NAME = "/"

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.expanded = False
        self.navigation = []

    def add_child(self, child):
        self.children[child.name] = child

    def toggle_expand(self):
        if not self.expanded:
            # Collapse all siblings before expanding this node
            self.collapse_siblings()
        self.expanded = not self.expanded

    def collapse_siblings(self):
        if self.parent:
            for sibling in self.parent.children.values():
                if sibling != self:
                    sibling.collapse()

    def collapse(self):
        if self.expanded:
            self.expanded = False
            for child in self.children.values():
                child.collapse()

    def _get_navigation_options(self):
        options = {}
        current = self
        while current.parent:
            current = current.parent

        for sibling_name, sibling_node in current.children.items():
            options[sibling_name] = sibling_node
            if sibling_node.expanded:
                self._add_expanded_children(options, sibling_name, sibling_node)

        return options

    def _add_expanded_children(self, options, path, node):
        if node.expanded:
            for child_name, child_node in node.children.items():
                combined_name = f"{path}/{child_name}"
                options[combined_name] = child_node
                self._add_expanded_children(options, combined_name, child_node)

    def navigate_tree(self):
        current_node = self
        while True:
            options = current_node._get_navigation_options()
            print(f"Current node: [{current_node.name}]\n"
                  f"Available options: {", ".join([f"'{opt}'" for opt in options.keys() if opt != TreeNode.ROOT_NAME])} "
                  f"or 'SUBMIT' or 'GIVE UP'")

            user_input = input(f" Enter your choice from the options above: ")

            if user_input == 'SUBMIT':
                # Record the current node's path before submitting
                self._record_navigation(current_node)
                # Display all recorded paths for review then return the user submission
                self.recorded_metrics()
                return f"Submitted: {self._get_full_path(current_node)}"

            elif user_input == 'GIVE UP':
                # Display all recorded paths before giving up
                self.recorded_metrics()
                return "Giving up as no suitable answer found."

            # Check if the user input matches one of the available navigation options
            elif user_input in options:
                # Record the current navigation step
                self._record_navigation(current_node)
                # Retrieve the node associated with the user's choice
                next_node = options[user_input]
                # Check if the next node is different from the current node
                if next_node != current_node:
                    # If navigating to a new node that isn't expanded, collapse all sibling nodes
                    if not next_node.expanded:
                        next_node.collapse_siblings()
                    # Expand the next node to show its children
                    next_node.toggle_expand()
                # Update the current node to the next node
                current_node = next_node

            # Handle the case where the user input does not match any valid option
            else:
                print("Invalid option, try again.")

    def _record_navigation(self, current_node):
        # Check if the last recorded node is the same as the current node to prevent duplicates
        if self.navigation and self.navigation[-1].node_name == self._get_full_path(current_node):
            return  # Skip recording if the last recorded node is the same as the current

        timestamp = datetime.datetime.now()
        full_path = self._get_full_path(current_node)
        self.navigation.append(NavigationRecord(timestamp, full_path))

    @staticmethod
    def _get_full_path(node):
        path = []
        while node:
            path.append(node.name)
            node = node.parent
        return '/'.join(reversed(path)).strip('/')

    def recorded_metrics(self):
        print(
            f"Recorded metrics: {', '.join([str(record) for record in self.navigation])}")

    @staticmethod
    def build_tree_from_dict(node_dict, parent=None, parent_name=None):
        if parent_name is None:
            parent_name = TreeNode.ROOT_NAME
        root = TreeNode(parent_name, parent)
        for key, value in node_dict.items():
            if isinstance(value, dict):
                child_node = TreeNode.build_tree_from_dict(value, root, key)
                root.add_child(child_node)
            else:
                child_node = TreeNode(key, root)
                root.add_child(child_node)
                for leaf in value:
                    leaf_node = TreeNode(leaf, child_node)
                    child_node.add_child(leaf_node)
        return root


if __name__ == "__main__":
    tree_structure = {
        "Electronics": {
            "Mobile Phones": {
                "Smartphones": ["iPhone", "Android"],
                "Accessories": ["Cases", "Chargers"]
            },
            "Computers": {
                "Laptops": ["MacBook", "Windows Laptop"],
                "Desktops": ["Gaming PC", "Office PC"]
            }
        },
        "Clothing": {
            "Men": {
                "Shirts": ["T-Shirts", "Formal Shirts"],
                "Trousers": ["Jeans", "Chinos"]
            },
            "Women": {
                "Dresses": ["Casual Dresses", "Evening Dresses"],
                "Skirts": ["Mini Skirts", "Long Skirts"]
            }
        },
        "Books": {
            "Fiction": {
                "Novels": ["Sci-Fi", "Fantasy"],
                "Short Stories": ["Anthologies", "Collections"]
            },
            "Non-Fiction": {
                "Biographies": ["Historical", "Celebrity"],
                "Science": ["Physics", "Biology"]
            }
        }
    }

    print(TreeNode.build_tree_from_dict(tree_structure).navigate_tree())
