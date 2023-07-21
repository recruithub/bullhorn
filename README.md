# bullhorn

`bullhorn` is an unofficial REST API wrapper for the Bullhorn CRM, implemented in Python.

## Features

- Seamless interaction with the Bullhorn REST API.
- Simplified access to candidates, jobs, placements and other entity types.
- Error handling, including retries, and proper API response validation.

## Installation

You can install `bullhorn` using `pip`:

```bash
pip install bullhorn
```

## Getting Started

`bullhorn` requires you to have a session token and REST URL from Bullhorn.

> _Authentication from earlier in the pipeline will be added in a later release._

```python
import os

from bullhorn.client import BullhornClient

# Get credentials
session_token = os.environ.get("BULLHORN_SESSION_TOKEN")
rest_url = os.environ.get("BULLHORN_REST_URL")

# Initialise Bullhorn client with credentials
bc = BullhornClient(
    token=session_token,
    rest_url=rest_url,
)

# Get list of candidates
candidates = bc.get_candidates(
    query="dateLastModified:{2023/01/01 TO *}",
    fields="id,firstName,lastName",
)
print("Success: %r" % (candidates))

```

## Contribution

Contributions to `bullhorn` are welcome! If you encounter any issues or have suggestions for improvements, please feel free to create an issue or submit a pull request on the GitHub repository at [https://github.com/recruithub/bullhorn](https://github.com/recruithub/bullhorn).

## License

`bullhorn` is released under the MIT License. See [LICENSE](https://github.com/recruithub/bullhorn/blob/main/LICENSE) for more information.

## Disclaimer

This package is not officially affiliated with or endorsed by Bullhorn. Use it at your own risk, and make sure to comply with the Bullhorn API usage terms and conditions.
