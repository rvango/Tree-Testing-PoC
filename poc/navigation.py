import datetime
from enum import Enum, auto

from metrics import Metrics
from tree_node import TreeNode


class Command(Enum):
    SUBMIT = auto()
    GIVE_UP = auto()


class Navigation:
    def __init__(self, root_node):
        self.current_node = root_node
        self.navigation_records = []

    def start(self):
        while True:
            options = self._get_navigation_options(self.current_node)
            print(f"Current node: [{self._get_full_path(self.current_node)}]\n"
                  f"Available options: {', '.join([f'\'{opt}\''
                                                   for opt in options.keys() if opt != TreeNode.ROOT_NAME])} "
                  f"or '{Command.SUBMIT.name}' or '{Command.GIVE_UP.name}'")

            user_input = input(" Enter your choice from the options above: ")

            if user_input == Command.SUBMIT.name:
                return self._handle_submit()

            elif user_input == Command.GIVE_UP.name:
                return self._handle_give_up()

            elif user_input in options:
                self._handle_navigation(user_input, options)
            else:
                print("Invalid option, try again.")

    def _get_navigation_options(self, node):
        options = {}
        current = node
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

    def _handle_submit(self):
        self._record_navigation()
        self.recorded_metrics()
        return f"Submitted: {self._get_full_path(self.current_node)}"

    def _handle_give_up(self):
        self.recorded_metrics()
        return "Giving up as no suitable answer found."

    def _handle_navigation(self, user_input, options):
        next_node = options[user_input]
        if next_node != self.current_node:
            if not next_node.expanded:
                next_node.collapse_siblings()
            next_node.toggle_expand()
        self._record_navigation(next_node)
        self.current_node = next_node

    def _record_navigation(self, node=None):
        if node is None:
            node = self.current_node
        if self.navigation_records and self.navigation_records[-1].node_name == self._get_full_path(node):
            return

        timestamp = datetime.datetime.now()
        full_path = self._get_full_path(node)
        self.navigation_records.append(Metrics(timestamp, full_path))

    def recorded_metrics(self):
        print(
            f"Recorded metrics: {', '.join([str(record) for record in self.navigation_records])}")

    @staticmethod
    def _get_full_path(node):
        path = []
        if node.name == TreeNode.ROOT_NAME:
            return TreeNode.ROOT_NAME
        else:
            while node:
                path.append(node.name)
                node = node.parent
            return '/'.join(reversed(path)).strip('/')
