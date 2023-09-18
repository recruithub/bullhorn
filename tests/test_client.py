import os

from typing import List

from bullhorn import __version__
from bullhorn.client import BullhornClient
from bullhorn.types import (
    candidate,
    client_contact,
    client_corporation,
    corporate_user,
    job_order,
    job_submission,
    ping,
    placement,
    placement_commission,
)

# Set test suite defaults
TEST_SESSION_TOKEN = os.environ.get(
    "TEST_SESSION_TOKEN",
    "https://rest123.bullhornstaffing.com/rest-services/1234/",
)
TEST_REST_URL = os.environ.get(
    "TEST_REST_URL",
    "12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
)
TEST_USE_ENV_CREDENTIALS = os.environ.get(
    "TEST_USE_ENV_CREDENTIALS",
    False,
)


def test_client_user_agent():
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get user agent
    user_agent = bc.user_agent
    assert "Python wrapper for Bullhorn API" in user_agent


def test_client_ping(mocker):
    # Mock response
    return_value: ping.Ping = {"sessionExpires": 1234567891011}
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.ping()
    assert "sessionExpires" in result


def test_client_get_candidates(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "firstName": "Example",
                "middleName": "C.",
                "lastName": "Name",
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_candidates(
        query="dateLastModified:{1970/01/01 TO *}",
        fields="id,businessSectors,candidateSource,category,companyName,dateAdded,email,firstName,interviews,isDeleted,lastName,leads,mobile,name,occupation,owner,payrollStatus,salary,source,status,submissions,userDateAdded",
    )
    assert "firstName" in result[0]


def test_client_get_client_contacts(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "firstName": "Example",
                "middleName": "C.",
                "lastName": "Name",
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_client_contacts(
        where="id >= 0",
        fields="id,businessSectors,category,clientCorporation,dateAdded,dateLastModified,division,email,firstName,isDeleted,lastName,leads,name,occupation,owner,source,status,type",
    )
    assert "lastName" in result[0]


def test_client_get_client_corporations(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "name": "Example Inc.",
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_client_corporations(
        where="id >= 0",
        fields="id,businessSectorList,clientContacts,companyURL,dateAdded,dateFounded,dateLastModified,department,exemptionStatus,feeArrangement,industryList,leads,name,owners,revenue,status",
    )
    assert "name" in result[0]


def test_client_get_corporate_users(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "firstName": "Example",
                "middleName": "C.",
                "lastName": "Name",
                "username": "ExampleCName",
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_corporate_users(
        where="id >= 0",
        fields="id,email,firstName,isDeleted,lastName,mobile,name,occupation,status,userType,username",
    )
    assert "username" in result[0]


def test_client_get_job_orders(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "description": "An example open job to be filled.",
                "owner": {
                    "id": 1234567891011,
                    "firstName": "Example",
                    "middleName": "C.",
                    "lastName": "Name",
                    "username": "ExampleCName",
                },
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_job_orders(
        where="id >= 0",
        fields="id,appointments,approvedPlacements,assignedUsers,billRateCategoryID,billingProfile,bonusPackage,branch,businessSectors,categories,clientBillRate,clientContact,clientCorporation,dateAdded,dateClosed,dateEnd,dateLastModified,description,durationWeeks,employmentType,feeArrangement,interviews,isDeleted,isOpen,isPublic,jobCode,numOpenings,opportunity,owner,payRate,placements,reasonClosed,salary,salaryUnit,source,startDate,status,submissions,title,usersAssigned",
    )
    assert "owner" in result[0]


def test_client_get_job_submissions(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "endDate": 1234567891011,
                "owners": [
                    {
                        "id": 1234567891011,
                        "firstName": "Example",
                        "middleName": "C.",
                        "lastName": "Name",
                        "username": "ExampleCName",
                    },
                ],
                "startDate": 1234567891012,
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_job_submissions(
        where="id >= 0",
        fields="id,appointments,billRate,candidate,dateAdded,dateLastModified,endDate,isDeleted,jobOrder,latestAppointment,owners,payRate,salary,sendingUser,source,startDate,status",
    )
    assert "owners" in result[0]


def test_client_get_placements(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "fee": 0.5,
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_placements(
        where="id >= 0",
        fields="id,appointments,billingFrequency,bonusPackage,candidate,clientBillRate,clientOvertimeRate,commissions,dateAdded,dateBegin,dateClientEffective,dateEffective,dateEnd,dateLastModified,durationWeeks,employeeType,employmentStartDate,employmentType,fee,jobOrder,jobSubmission,location,owner,payRate,salary,salaryUnit,status",
    )
    assert "fee" in result[0]


def test_client_get_placement_commissions(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
                "user": {
                    "id": 1234567891011,
                    "firstName": "Example",
                    "middleName": "C.",
                    "lastName": "Name",
                    "username": "ExampleCName",
                },
                "commissionPercentage": 0.05,
            },
        ],
    }
    if not TEST_USE_ENV_CREDENTIALS:
        mocker.patch(
            "bullhorn.client.BullhornClient.request",
            return_value=return_value,
        )
    # Initialise client
    bc = BullhornClient(
        token=TEST_SESSION_TOKEN,
        rest_url=TEST_REST_URL,
    )
    # Get result
    result = bc.get_placement_commissions(
        where="id >= 0",
        fields="id,commissionPercentage,dateAdded,dateLastModified,flatPayout,grossMarginPercentage,hourlyPayout,placement,role,status,user",
    )
    assert "commissionPercentage" in result[0]
