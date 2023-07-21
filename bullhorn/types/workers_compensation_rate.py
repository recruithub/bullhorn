from bullhorn.types import workers_compensation


class WorkersCompensationRate:
    id: int
    compensation: workers_compensation.WorkersCompensation
    endDate: int
    rate: float
    startDate: int
