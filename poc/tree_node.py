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

