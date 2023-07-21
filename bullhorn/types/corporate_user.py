from typing import Optional


class CorporateUser:
    id: int
    companyName: str
    corporation: Optional[int]
    dateLastComment: Optional[int]
    dateLastModified: int
    email: Optional[str]
    email2: Optional[str]
    email3: Optional[str]
    enabled: bool
    externalEmail: str
    isDeleted: Optional[bool]
    isHidden: Optional[bool]
    isLockedOut: Optional[bool]
    lastName: Optional[str]
    masterUserID: int
    middleName: Optional[str]
    mobile: Optional[str]
    name: Optional[str]
    namePrefix: Optional[str]
    nameSuffix: Optional[str]
    nickName: Optional[str]
    occupation: Optional[str]
    status: Optional[str]
    userDateAdded: int
    userType: int
    username: str
