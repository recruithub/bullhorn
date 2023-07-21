from typing import Optional

from bullhorn.types import corporate_user, placement


class PlacementCommission:
    id: int
    comments: Optional[str]
    commissionPercentage: float
    dateAdded: int
    dateLastModified: int
    externalRecipient: Optional[str]
    flatPayout: float
    grossMarginPercentage: float
    hourlyPayout: float
    placement: placement.Placement
    role: str
    status: str
    user: Optional[corporate_user.CorporateUser]
