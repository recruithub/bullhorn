from typing import List, Optional

from bullhorn.types import (
    agreement_line,
    billing_profile,
    branch,
    category,
    client_contact,
    client_corporation,
    corporate_user,
    job_code,
    location,
    opportunity,
    shift,
    workers_compensation_rate,
)


class JobOrder:
    id: int
    address: dict
    appointments: List[int]
    approvedPlacements: List[int]
    assignedUsers: List[int]
    benefits: str
    billRateCategoryID: int
    billingProfile: Optional[billing_profile.BillingProfile]
    bonusPackage: str
    branch: Optional[branch.Branch]
    branchCode: str
    businessSectors: List[int]
    categories: List[int]
    certificationGroups: List[int]
    certificationList: str
    certifications: List[int]
    clientBillRate: float
    clientContact: client_contact.ClientContact
    clientCorporation: client_corporation.ClientCorporation
    clientCorporationLine: Optional[agreement_line.AgreementLine]
    correlatedCustomDate1: Optional[int]
    correlatedCustomDate2: Optional[int]
    correlatedCustomDate3: Optional[int]
    correlatedCustomFloat1: Optional[float]
    correlatedCustomFloat2: Optional[float]
    correlatedCustomFloat3: Optional[float]
    correlatedCustomText1: Optional[str]
    correlatedCustomText2: Optional[str]
    correlatedCustomText3: Optional[str]
    correlatedCustomText4: Optional[str]
    correlatedCustomText5: Optional[str]
    correlatedCustomText6: Optional[str]
    correlatedCustomText7: Optional[str]
    correlatedCustomText8: Optional[str]
    correlatedCustomText9: Optional[str]
    correlatedCustomText10: Optional[str]
    costCenter: str
    customDate1: Optional[int]
    customDate2: Optional[int]
    customDate3: Optional[int]
    customFloat1: Optional[float]
    customFloat2: Optional[float]
    customFloat3: Optional[float]
    customFloat4: Optional[float]
    customFloat5: Optional[float]
    customFloat6: Optional[float]
    customFloat7: Optional[float]
    customFloat8: Optional[float]
    customInt1: Optional[int]
    customInt2: Optional[int]
    customInt3: Optional[int]
    customInt4: Optional[int]
    customInt5: Optional[int]
    customInt6: Optional[int]
    customInt7: Optional[int]
    customInt8: Optional[int]
    customText1: Optional[str]
    customText2: Optional[str]
    customText3: Optional[str]
    customText4: Optional[str]
    customText5: Optional[str]
    customText6: Optional[str]
    customText7: Optional[str]
    customText8: Optional[str]
    customText9: Optional[str]
    customText10: Optional[str]
    customTextBlock1: Optional[str]
    customTextBlock2: Optional[str]
    customTextBlock3: Optional[str]
    customTextBlock4: Optional[str]
    customTextBlock5: Optional[str]
    dateAdded: int
    dateClosed: Optional[int]
    dateEnd: Optional[int]
    dateLastExported: Optional[int]
    dateLastModified: int
    dateLastPublished: Optional[int]
    degreeList: str
    description: str
    durationWeeks: float
    educationDegree: str
    employmentType: str
    externalCategoryID: int
    externalID: str
    feeArrangement: float
    fileAttachments: List[int]
    hoursOfOperation: str
    hoursPerWeek: float
    interviews: List[int]
    isClientEditable: bool
    isDeleted: bool
    isInterviewRequired: bool
    isJobcastPublished: bool
    isOpen: bool
    isPublic: int
    jobBoardList: str
    jobCode: Optional[job_code.JobCode]
    jobOrderIntegrations: List[int]
    location: Optional[location.Location]
    markUpPercentage: float
    notes: List[int]
    numOpenings: int
    onSite: str
    opportunity: Optional[opportunity.Opportunity]
    optionsPackage: str
    owner: corporate_user.CorporateUser
    payRate: float
    placements: List[int]
    publicDescription: str
    publishedCategory: Optional[category.Category]
    publishedZip: str
    reasonClosed: str
    reportTo: str
    reportToClientContact: Optional[client_contact.ClientContact]
    responseUser: Optional[corporate_user.CorporateUser]
    salary: float
    salaryUnit: str
    sendouts: List[int]
    shift: Optional[shift.Shift]
    shifts: List[int]
    skillList: str
    skills: List[int]
    source: str
    specialties: List[int]
    startDate: int
    status: str
    submissions: List[int]
    tasks: List[int]
    taxRate: float
    taxStatus: str
    tearsheets: List[int]
    timeUnits: List[int]
    title: str
    travelRequirements: str
    type: int
    usersAssigned: str
    webResponses: List[int]
    willRelocate: bool
    willRelocateInt: int
    willSponsor: bool
    workersCompRate: Optional[workers_compensation_rate.WorkersCompensationRate]
    yearsRequired: int
