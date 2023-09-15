import logging
import sys
import time
from typing import Any, Dict, List, Optional, Union

import requests

from bullhorn import __version__
from bullhorn.exceptions import BullhornServerError, Forbidden, HTTPException, NotFound
from bullhorn.route import Route
from bullhorn.types import (
    appointment,
    business_sector,
    candidate,
    category,
    client_contact,
    client_corporation,
    client_corporation_appointment,
    corporate_user,
    country,
    department,
    employee_pay,
    employer_contribution,
    job_order,
    job_submission,
    job_submission_history,
    lead,
    lead_history,
    location,
    opportunity,
    opportunity_history,
    ping,
    placement,
    placement_commission,
    sendout,
)

logger = logging.getLogger(__name__)


class BullhornClient:
    def __init__(
        self,
        token: Optional[str] = None,
        rest_url: Optional[str] = None,
    ) -> None:
        # Set token and namespace
        self.token: Optional[str] = token
        self.rest_url: Optional[str] = rest_url
        # Set user agent
        self.user_agent: str = self._get_user_agent()

    def _get_user_agent(
        self,
    ) -> str:
        """
        Get the user agent string for the HTTP client.

        Returns:
            str:
                The user agent string combining information about the Python wrapper,
                its version, the Python interpreter version, and the aiohttp version.
        """
        version_info = sys.version_info
        user_agent_strings = [
            "Python wrapper for Bullhorn API",
            f"(https://github.com/recruithub/bullhorn {__version__})",
            f"Python/{version_info.major}.{version_info.minor}.{version_info.micro}",
            f"requests/{requests.__version__}",
        ]
        user_agent = " ".join(user_agent_strings)
        return user_agent

    def request(
        self,
        route: Route,
        json: Optional[Dict] = None,
        files=None,
        form=None,
    ) -> Any:
        # Get attributes from route
        method = route.method
        url = route.url
        # Set headers
        headers: Dict[str, str] = {}
        headers["User-Agent"] = self.user_agent
        if self.token is not None:
            headers["BhRestToken"] = self.token
        if json is not None:
            headers["Content-Type"] = "application/json"

        # Fetch response
        data: Optional[Union[Dict[str, Any], str]] = None
        for tries in range(5):
            # Execute request
            try:
                response = requests.request(
                    method=method, url=url, headers=headers, json=json
                )
                logger.debug(
                    f"{method} {url} with {data} has returned {response.status_code}"
                )
                data = response.json()
                # Successful request
                if 300 > response.status_code >= 200:
                    logger.debug(f"{method} {url} has received {data}")
                    return data
                # Server error, so retry request with exponential back-off
                if response.status_code in {500, 502, 503, 504, 524}:
                    time.sleep(1 + tries * 2)
                    continue
                # Client error, so raise exception
                if response.status_code == 403:
                    raise Forbidden(response, data)
                elif response.status_code == 404:
                    raise NotFound(response, data)
                elif response.status_code >= 500:
                    raise BullhornServerError(response, data)
                else:
                    raise HTTPException(response, data)
            except OSError as e:
                # Connection reset by peer, so retry with exponential back-off
                if tries < 4 and e.errno in (54, 10054):
                    time.sleep(1 + tries * 2)
                    continue
                raise
        if response is not None:
            # Out of retries, so raise an appropriate exception
            if response.status_code >= 500:
                raise BullhornServerError(response, data)
            raise HTTPException(response, data)
        # Capture unhandled logic
        raise RuntimeError(response, "Unreachable code in HTTP handling")

    def ping(
        self,
    ) -> ping.Ping:
        """Ping used to test whether the client’s session is valid."""
        request = self.request(
            Route(
                "GET",
                self.rest_url + "ping",
            )
        )
        return request

    def get_appointments(
        self,
        query: str,
        fields: str,
    ) -> List[appointment.Appointment]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Appointment?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request

    def get_business_sectors(
        self,
        query: str,
        fields: str,
    ) -> List[business_sector.BusinessSector]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/BusinessSector?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request

    def get_candidates(
        self,
        query: str,
        fields: str,
    ) -> List[candidate.Candidate]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Candidate?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_categories(
        self,
        query: str,
        fields: str,
    ) -> List[category.Category]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Category?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request

    def get_client_contacts(
        self,
        query: str,
        fields: str,
    ) -> List[client_contact.ClientContact]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/ClientContact?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_client_corporations(
        self,
        query: str,
        fields: str,
    ) -> List[client_corporation.ClientCorporation]:
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "search/ClientCorporation?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_client_corporation_appointments(
        self,
        query: str,
        fields: str,
    ) -> List[client_corporation_appointment.ClientCorporationAppointment]:
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "search/ClientCorporationAppointment?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_corporate_users(
        self,
        where: str,
        fields: str,
    ) -> List[corporate_user.CorporateUser]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "query/CorporateUser?where={where}&fields={fields}",
                path_params={
                    "where": where,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_countries(
        self,
        where: str,
        fields: str,
    ) -> List[country.Country]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "query/Country?where={where}&fields={fields}",
                path_params={
                    "where": where,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_departments(
        self,
        where: str,
        fields: str,
    ) -> List[department.Department]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "query/Department?where={where}&fields={fields}",
                path_params={
                    "where": where,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_employee_pays(
        self,
        query: str,
        fields: str,
    ) -> List[employee_pay.EmployeePay]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/EmployeePay?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_employer_contributions(
        self,
        query: str,
        fields: str,
    ) -> List[employer_contribution.EmployerContribution]:
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "search/EmployerContribution?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_job_orders(
        self,
        query: str,
        fields: str,
    ) -> List[job_order.JobOrder]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/JobOrder?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_job_submissions(
        self,
        query: str,
        fields: str,
    ) -> List[job_submission.JobSubmission]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/JobSubmission?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_job_submission_histories(
        self,
        query: str,
        fields: str,
    ) -> List[job_submission_history.JobSubmissionHistory]:
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "search/JobSubmissionHistory?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_leads(
        self,
        query: str,
        fields: str,
    ) -> List[lead.Lead]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Lead?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_lead_histories(
        self,
        query: str,
        fields: str,
    ) -> List[lead_history.LeadHistory]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/LeadHistory?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_locations(
        self,
        query: str,
        fields: str,
    ) -> List[location.Location]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Location?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_opportunities(
        self,
        query: str,
        fields: str,
    ) -> List[opportunity.Opportunity]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Opportunity?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_opportunity_histories(
        self,
        query: str,
        fields: str,
    ) -> List[opportunity_history.OpportunityHistory]:
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "search/OpportunityHistory?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_placements(
        self,
        query: str,
        fields: str,
    ) -> List[placement.Placement]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Placement?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_placement_commissions(
        self,
        where: str,
        fields: str,
    ) -> List[placement_commission.PlacementCommission]:
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/PlacementCommission?where={where}&fields={fields}",
                path_params={
                    "where": where,
                    "fields": fields,
                },
            )
        )
        return request["data"]

    def get_sendouts(
        self,
        query: str,
        fields: str,
    ) -> List[sendout.Sendout]:
        request = self.request(
            Route(
                "GET",
                self.rest_url + "search/Sendout?query={query}&fields={fields}",
                path_params={
                    "query": query,
                    "fields": fields,
                },
            )
        )
        return request["data"]
