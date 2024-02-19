import os

from bullhorn.client import BullhornClient



# Set credentials
session_token = os.environ.get("BULLHORN_SESSION_TOKEN")
rest_url = os.environ.get("BULLHORN_REST_URL")
# Initialise client
bc = BullhornClient(
    token=session_token,
    rest_url=rest_url,
)
# Get settings result
settings = bc.get_settings(
    fields="",
)
print(settings)


1 2 2 3 5

1 2 3 4 5