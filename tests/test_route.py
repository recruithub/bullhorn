from bullhorn.route import Route


def test_route_url():
    method = "GET"
    path = "https://rest123.bullhornstaffing.com/rest-services/1234/" + "ping"
    path_params = {}
    query_params = {}
    route = Route(
        method,
        path,
        path_params,
        query_params,
    )
    assert route.url == "https://rest123.bullhornstaffing.com/rest-services/1234/ping"


def test_route_url_params():
    method = "GET"
    path = (
        "https://rest123.bullhornstaffing.com/rest-services/1234/"
        + "entity/{entityType}/{entityId}"
    )
    path_params = {
        "entityType": "Candidate",
        "entityId": "123456789",
    }
    query_params = {
        "fields": "firstName,lastName,address",
        "count": 5,
    }
    route = Route(
        method,
        path,
        path_params,
        query_params,
    )
    assert (
        route.url
        == "https://rest123.bullhornstaffing.com/rest-services/1234/entity/Candidate/123456789?fields=firstName%2ClastName%2Caddress&count=5"
    )
