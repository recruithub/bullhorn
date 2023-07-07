import pytest

from bullhorn import __version__
from bullhorn.client import BullhornClient
from bullhorn.types import ping


@pytest.mark.asyncio
async def test_bullhorn_client_ping(mocker):
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
    result = await bc.ping()
    assert "sessionExpires" in result


def test_client_user_agent():
    # Initialise client
    bc = BullhornClient(
        token="12345_1234567_a12345bc-123a-45bc-67de-12345678910a",
        rest_url="https://rest123.bullhornstaffing.com/rest-services/1234/",
    )
    # Get user agent
    user_agent = bc.user_agent
    assert "Python wrapper for Bullhorn API" in user_agent
