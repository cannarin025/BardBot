from dataclasses import dataclass

@dataclass
class Video:
    title: str
    url: str
    duration: int
    channel: str
    source: str