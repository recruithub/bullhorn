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
)


def test_client_user_agent():
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get user agent
    user_agent = bc.user_agent
    assert "Python wrapper for Bullhorn API" in user_agent


def test_client_ping(mocker):
    # Mock response
    return_value: ping.Ping = {"sessionExpires": 1234567891011}
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.ping()
    assert "sessionExpires" in result


def test_client_get_candidates(mocker):
    # Mock response
    return_value: List[candidate.Candidate] = [
        {
            "id": 1234567891011,
            "firstName": "Example",
            "middleName": "C.",
            "lastName": "Name",
        },
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_candidates(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,firstName,middleName,lastName",
    )
    assert "firstName" in result[0]


def test_client_get_client_contacts(mocker):
    # Mock response
    return_value: List[client_contact.ClientContact] = [
        {
            "id": 1234567891011,
            "firstName": "Example",
            "middleName": "C.",
            "lastName": "Name",
        },
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_client_contacts(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,firstName,middleName,lastName",
    )
    assert "lastName" in result[0]


def test_client_get_client_corporations(mocker):
    # Mock response
    return_value: List[client_corporation.ClientCorporation] = [
        {
            "id": 1234567891011,
            "name": "Example Inc.",
        },
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_client_corporations(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,name",
    )
    assert "name" in result[0]


def test_client_get_corporate_users(mocker):
    # Mock response
    return_value: List[corporate_user.CorporateUser] = [
        {
            "id": 1234567891011,
            "firstName": "Example",
            "middleName": "C.",
            "lastName": "Name",
            "username": "ExampleCName",
        },
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_corporate_users(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,firstName,middleName,lastName,username",
    )
    assert "username" in result[0]


def test_client_get_job_orders(mocker):
    # Mock response
    return_value: List[job_order.JobOrder] = [
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
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_job_orders(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,description,owner",
    )
    assert "owner" in result[0]


def test_client_get_job_submissions(mocker):
    # Mock response
    return_value: List[job_submission.JobSubmission] = [
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
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_job_submissions(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,endDate,owners,startDate",
    )
    assert "owners" in result[0]


def test_client_get_placements(mocker):
    # Mock response
    return_value: List[placement.Placement] = [
        {
            "id": 1234567891011,
            "fee": 0.5,
        },
    ]
    mocker.patch(
        "bullhorn.client.BullhornClient.request",
        return_value=return_value,
    )
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get result
    result = bc.get_placements(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,fee",
    )
    assert "fee" in result[0]
