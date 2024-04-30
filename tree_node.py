class TreeNode:
    ROOT_NAME = "/"

    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.expanded = False

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

    def get_navigation_options(self):
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
            options = current_node.get_navigation_options()
            print(f"Current node: [{current_node.name}]\n"
                  f"Available options: {", ".join([f"'{opt}'" for opt in options.keys() if opt != TreeNode.ROOT_NAME])} "
                  f"or 'SUBMIT' or 'GIVE UP'")

            user_input = input(f" Enter your choice from the options above: ")

            if user_input == 'SUBMIT':
                return f"Submitted: {current_node.name}"
            elif user_input == 'GIVE UP':
                return "No suitable answer found."
            elif user_input in options:
                next_node = options[user_input]
                if next_node != current_node:
                    # Make sure to collapse other nodes properly when navigating away
                    if not next_node.expanded:
                        next_node.collapse_siblings()
                    next_node.toggle_expand()
                current_node = next_node
            else:
                print("Invalid option, try again.")

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
