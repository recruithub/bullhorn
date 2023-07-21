from typing import Optional, List


class WorkersCompensation:
    id: int
    code: str
    description: Optional[str]
    name: Optional[str]
    rates: List[int]
    state: str
