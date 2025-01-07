import dataclasses


@dataclasses.dataclass
class User:
    tag: str
    link: str
    up: int
    down: int
    time: int
    port : int