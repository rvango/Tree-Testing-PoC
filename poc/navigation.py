import datetime
from enum import Enum, auto

from metrics import Metrics


class Command(Enum):
    SUBMIT = auto()
    GIVE_UP = auto()


class Navigation:
    def __init__(self, root_node):
        """Initialises the Navigation class with the starting root node."""
        self.root_node = root_node  # Maintain a reference to the root node
        self.current_node = root_node  # Start navigation at the root node
        self.navigation_records = []  # List to store navigation steps for metrics

    def start(self):
        """Begins the navigation process until user submits or gives up."""
        while True:
            options = self._get_navigation_options()
            print(
                f"Current node: [{self._get_full_path(self.current_node)}]\n"
                f"Available options: {', '.join(f'\'{option}\'' for option in options.keys() if option != self.root_node.name)} "
                f"or '{Command.SUBMIT.name}' or '{Command.GIVE_UP.name}'"
            )

            user_input = input(" Enter your choice from the options above: ")

            if user_input == Command.SUBMIT.name:
                return self._handle_submit()

            elif user_input == Command.GIVE_UP.name:
                return self._handle_give_up()

            elif user_input in options:
                next_node = options[user_input]
                self._handle_navigation(next_node)
            else:
                print("Invalid option, try again.")

    def _get_navigation_options(self):
        """Gathers and returns navigation options from the root node."""
        options = {}
        self._add_options_from_node(options, self.root_node)
        return options

    def _add_options_from_node(self, options, node, prefix=""):
        """Recursively adds nodes and their expanded children to the available options dictionary."""
        for child_name, child_node in node.children.items():
            path = f"{prefix}/{child_name}".strip('/')
            options[path] = child_node
            if child_node.expanded:
                self._add_options_from_node(options, child_node, path)

    def _handle_submit(self):
        """Handles user's decision to submit the current node as the answer."""
        self._record_navigation()
        self.recorded_metrics()
        return f"Submitted: {self._get_full_path(self.current_node)}"

    def _handle_give_up(self):
        """Handles user's decision to give up navigation."""
        self.recorded_metrics()
        return "Giving up as no suitable answer found."

    def _handle_navigation(self, next_node):
        """Navigates to the selected node, updating the current node and its state."""
        if not next_node.expanded:
            next_node.collapse_siblings()
        next_node.toggle_expand()
        self._record_navigation(next_node)
        self.current_node = next_node

    def _record_navigation(self, node=None):
        """Records each navigation step for metrics, avoiding duplicates."""

        # Default to the current node if no specific node is provided
        node = node or self.current_node
        full_path = self._get_full_path(node)

        def _is_last_recorded_node_same_as_current_node():
            """Checks if the last recorded node is the same as the current node."""
            if self.navigation_records:
                last_recorded_path = self.navigation_records[-1].node_name
                if last_recorded_path == full_path:
                    return True
            return False

        if not _is_last_recorded_node_same_as_current_node():
            # Record the navigation
            timestamp = datetime.datetime.now()
            self.navigation_records.append(Metrics(timestamp, full_path))

    def recorded_metrics(self):
        """Prints recorded metrics for all navigation steps."""
        print(f"Recorded metrics: {', '.join([str(record) for record in self.navigation_records])}")

    def _get_full_path(self, node):
        path = []
        if node == self.root_node:
            return self.root_node.name
        else:
            while node:
                path.append(node.name)
                node = node.parent
            return '/'.join(reversed(path)).strip('/')
