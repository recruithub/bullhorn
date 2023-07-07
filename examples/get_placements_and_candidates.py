import os

from bullhorn.client import BullhornClient


async def get_placements_and_candidates():
    # Set credentials
    token = os.environ.get("BULLHORN_SESSION_TOKEN")
    rest_url = os.environ.get("BULLHORN_REST_URL")

    # Initialise client
    bc = BullhornClient(
        token=token,
        rest_url=rest_url,
    )
    await bc.login()

    # Get placements result
    placements = await bc.get_placements(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,candidate,comments,dateAdded,dateBegin,dateEnd,dateLastModified,referralFee,salary,status",
    )
    print("Success: %r" % (placements))

    # Get candidates result
    candidates = await bc.get_candidates(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,firstName,lastName",
    )
    print("Success: %r" % (candidates))
