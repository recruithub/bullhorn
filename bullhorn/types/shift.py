from typing import Optional

from bullhorn.types import client_corporation, corporate_user


class Shift:
    id: int
    clientCorporation: Optional[client_corporation.ClientCorporation]
    dateLastModified: int
    dayOfWeek: Optional[int]
    endTime: Optional[int]
    htmlColorCode: Optional[str]
    isDefault: Optional[bool]
    isDeleted: bool
    lastModifyingUser: Optional[corporate_user.CorporateUser]
    migrateGUID: Optional[str]
    name: Optional[str]
    shortName: Optional[str]
    startTime: Optional[int]
    type: Optional[str]
