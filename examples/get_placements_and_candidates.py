import os

from bullhorn.client import BullhornClient


def get_placements_and_candidates():
    # Set credentials
    session_token = os.environ.get("BULLHORN_SESSION_TOKEN")
    rest_url = os.environ.get("BULLHORN_REST_URL")

    # Initialise client
    bc = BullhornClient(
        token=session_token,
        rest_url=rest_url,
    )

    # Get placements result
    placements = bc.get_placements(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,candidate,comments,dateAdded,dateBegin,dateEnd,dateLastModified,referralFee,salary,status",
    )
    print("Success: %r" % (placements))

    # Get candidates result
    candidates = bc.get_candidates(
        query="dateLastModified:{2023/01/01 TO *}",
        fields="id,firstName,lastName",
    )
    print("Success: %r" % (candidates))
