import os

from typing import List

import pytest

from bullhorn import __version__
from bullhorn.client import BullhornClient
from bullhorn.exceptions import Forbidden
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


def test_client_get_appointments(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_appointments(
        where="dateLastModified >= 1693522800000",
        fields="id,candidateReference,clientContactReference,communicationMethod,dateAdded,dateBegin,dateLastModified,isDeleted,jobOrder,lead,opportunity,owner,placement,type",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_business_sectors(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_business_sectors(
        where="dateAdded >= 1693522800000",
        fields="id,dateAdded,name",
    )
    assert (len(result) == 0) or ("id" in result[0])


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
        query="dateLastModified:{2023/09/01 TO *}",
        fields="id,businessSectors,candidateSource,category,companyName,dateAdded,dateLastModified,email,firstName,interviews,isDeleted,lastName,leads,mobile,name,occupation,owner,payrollStatus,salary,source,status,submissions,userDateAdded",
    )
    assert (len(result) == 0) or ("firstName" in result[0])


def test_client_get_categories(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_categories(
        where="dateAdded >= 1693522800000",
        fields="id,dateAdded,name,occupation,type",
    )
    assert (len(result) == 0) or ("id" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,businessSectors,category,clientCorporation,dateAdded,dateLastModified,division,email,firstName,isDeleted,lastName,leads,name,occupation,owner,source,status,type",
    )
    assert (len(result) == 0) or ("lastName" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,businessSectorList,clientContacts,companyURL,dateAdded,dateFounded,dateLastModified,department,exemptionStatus,feeArrangement,industryList,leads,name,owners,revenue,status",
    )
    assert (len(result) == 0) or ("name" in result[0])


def test_client_get_client_corporation_appointments(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_client_corporation_appointments(
        where="id >= 1",
        fields="id,clientCorporation,clientContact,appointment",
    )
    assert (len(result) == 0) or ("id" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,email,firstName,isDeleted,lastName,mobile,name,occupation,status,userType,username",
    )
    assert (len(result) == 0) or ("username" in result[0])


def test_client_get_countries(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_countries(
        where="id >= 1",
        fields="id,code,name",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_departments(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_departments(
        where="id >= 1",
        fields="id,name",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_employee_pays(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    try:
        result = bc.get_employee_pays(
            where="id >= 1",
            fields="id,amount,chargeDate,department,earnCodeName,hoursUnits,hoursWorked,jobCode,location,payCheck,projPhase,projWork,shift,unitRate,workCompID",
        )
    except Forbidden:
        pytest.skip("403 - Forbidden | Skipping...")
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_employer_contributions(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    try:
        result = bc.get_employee_pays(
            where="id >= 1",
            fields="id,amount,chargeDate,department,earnCodeName,hoursUnits,hoursWorked,jobCode,location,payCheck,projPhase,projWork,shift,unitRate,workCompID",
        )
    except Forbidden:
        pytest.skip("403 - Forbidden | Skipping...")
    assert (len(result) == 0) or ("id" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,appointments,approvedPlacements,assignedUsers,billRateCategoryID,billingProfile,bonusPackage,branch,businessSectors,categories,clientBillRate,clientContact,clientCorporation,dateAdded,dateClosed,dateEnd,dateLastModified,description,durationWeeks,employmentType,feeArrangement,interviews,isDeleted,isOpen,isPublic,jobCode,numOpenings,opportunity,owner,payRate,placements,reasonClosed,salary,salaryUnit,source,startDate,status,submissions,title,usersAssigned",
    )
    assert (len(result) == 0) or ("description" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,appointments,billRate,candidate,dateAdded,dateLastModified,endDate,isDeleted,jobOrder,latestAppointment,owners,payRate,salary,sendingUser,source,startDate,status",
    )
    assert (len(result) == 0) or ("endDate" in result[0])


def test_client_get_job_submission_histories(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_job_submission_histories(
        where="dateAdded >= 1693522800000",
        fields="id,dateAdded,jobSubmission,modifyingUser,status",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_leads(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_leads(
        where="dateLastModified >= 1693522800000",
        fields="id,assignedTo,businessSectors,campaignSource,candidates,category,clientContacts,clientCorporation,companyName,dateAdded,dateLastModified,email,firstName,isDeleted,lastName,leadSource,name,occupation,owner,role,salary,status,type",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_lead_histories(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_lead_histories(
        where="dateAdded >= 1693522800000",
        fields="id,clientCorporation,dateAdded,lead,modifyingUser,status",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_locations(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_locations(
        where="dateLastModified >= 1693522800000",
        fields="dateAdded,dateLastModified,owner,status,title",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_opportunities(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_opportunities(
        where="dateLastModified >= 1693522800000",
        fields="id,assignedUsers,category,clientContact,clientCorporation,dateAdded,dateLastModified,dealValue,effectiveDate,estimatedDuration,estimatedEndDate,estimatedHoursPerWeek,estimatedStartDate,expectedCloseDate,expectedFee,expectedPayRate,isDeleted,isOpen,jobOrders,lead,owner,salary,source,title",
    )
    assert (len(result) == 0) or ("id" in result[0])


def test_client_get_opportunity_histories(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_opportunity_histories(
        where="dateAdded >= 1693522800000",
        fields="id,dateAdded,dealValue,effectiveDate,modifyingUser,opportunity,status",
    )
    assert (len(result) == 0) or ("id" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,appointments,billingFrequency,bonusPackage,candidate,clientBillRate,clientOvertimeRate,commissions,dateAdded,dateBegin,dateClientEffective,dateEffective,dateEnd,dateLastModified,durationWeeks,employeeType,employmentStartDate,employmentType,fee,jobOrder,jobSubmission,location,owner,payRate,salary,salaryUnit,status",
    )
    assert (len(result) == 0) or ("fee" in result[0])


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
        where="dateLastModified >= 1693522800000",
        fields="id,commissionPercentage,dateAdded,dateLastModified,flatPayout,grossMarginPercentage,hourlyPayout,placement,role,status,user",
    )
    assert (len(result) == 0) or ("commissionPercentage" in result[0])


def test_client_get_sendouts(mocker):
    # Mock response
    return_value = {
        "total": 1,
        "start": 0,
        "count": 1,
        "data": [
            {
                "id": 1234567891011,
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
    result = bc.get_sendouts(
        where="dateAdded >= 1693522800000",
        fields="id,candidate,clientContact,clientCorporation,dateAdded,email,isRead,jobOrder,user",
    )
    assert (len(result) == 0) or ("id" in result[0])
