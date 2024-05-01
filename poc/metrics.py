from dataclasses import dataclass
import datetime


@dataclass
class Metrics:
    timestamp: datetime.datetime
    node_name: str

    def __str__(self):
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {self.node_name}]"
