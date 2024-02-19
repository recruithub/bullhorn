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
    setting,
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
        Generates a user agent string for the HTTP client. The user agent string is composed of information regarding
        the wrapper library, Python version, and requests library version being used.

        Returns:
        - str: The generated user agent string.

        Example usage:
        >>> user_agent_str = api_instance._get_user_agent()
        >>> print(user_agent_str)
        Python wrapper for Bullhorn API (https://github.com/recruithub/bullhorn 1.0.0) Python/3.8.10 requests/2.25.1
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
    ) -> Any:
        """
        Sends an HTTP request to a specified route and handles the response. Retries the request in case of certain
        server errors or rate-limiting issues, with exponential back-off. Raises exceptions for client or unexpected
        server errors.

        Parameters:
        - route (Route): An object containing the method and URL for the HTTP request.
        - json (Optional[Dict], optional): A dictionary containing the JSON payload to be sent with the request.
          Defaults to None.

        Returns:
        - Any: The JSON response data if the request is successful.

        Raises:
        - Forbidden: If the request is forbidden (HTTP status 403).
        - NotFound: If the requested resource is not found (HTTP status 404).
        - BullhornServerError: If there's a server error (HTTP status 500 or above, except for specific retriable
          errors).
        - HTTPException: For other HTTP errors.
        - OSError: For connection-related errors.
        - RuntimeError: If an unexpected state occurs, indicating a bug in the code.
        """
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
                # Server error or too many requests, so retry request with exponential back-off
                if response.status_code in {429, 500, 502, 503, 504, 524}:
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
        """
        Sends a GET request to the API's ping endpoint to retrieve the expiration date of the calling client's session.
        This method can be used to test whether the client's session is valid.

        Returns:
        - ping.Ping: An object containing the date of the session expiration if the session is valid.

        Raises:
        - Unauthorized: If the client's session is not valid (assuming `Unauthorized` exception is defined to handle
          such cases).
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url + "ping",
            )
        )
        return request

    def get_appointments(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[appointment.Appointment]:
        """
        Sends a GET request to the REST API to retrieve a list of appointments based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the appointments.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the appointments.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of appointments to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning appointments.
          Defaults to 0.

        Returns:
        - List[Appointment]: A list of appointments matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Appointment?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_business_sectors(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[business_sector.BusinessSector]:
        """
        Sends a GET request to the REST API to retrieve a list of business sectors based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the business sectors.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the business sectors.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of business sectors to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning business sectors.
          Defaults to 0.

        Returns:
        - List[BusinessSector]: A list of business sectors matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/BusinessSector?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_candidates(
        self,
        query: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[candidate.Candidate]:
        """
        Sends a GET request to the REST API to retrieve a list of candidates based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the candidates.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the candidates.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of candidates to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning candidates.
          Defaults to 0.

        Returns:
        - List[Candidate]: A list of candidates matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "search/Candidate?query={query}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "query": query,
                    "fields": fields,
                    "order_by": order_by,
                    "start": start,
                    "count": count,
                },
            )
        )
        return request["data"]

    def get_categories(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[category.Category]:
        """
        Sends a GET request to the REST API to retrieve a list of categories based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the categories.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the categories.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of categories to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning categories.
          Defaults to 0.

        Returns:
        - List[Category]: A list of categories matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Category?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_client_contacts(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[client_contact.ClientContact]:
        """
        Sends a GET request to the REST API to retrieve a list of client contacts based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the client contacts.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the client contacts.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of client contacts to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning client contacts.
          Defaults to 0.

        Returns:
        - List[ClientContact]: A list of client contacts matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/ClientContact?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_client_corporations(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[client_corporation.ClientCorporation]:
        """
        Sends a GET request to the REST API to retrieve a list of client corporations based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the client corporations.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the client corporations.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of client corporations to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning client corporations.
          Defaults to 0.

        Returns:
        - List[ClientCorporation]: A list of client corporations matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/ClientCorporation?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_client_corporation_appointments(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[client_corporation_appointment.ClientCorporationAppointment]:
        """
        Sends a GET request to the REST API to retrieve a list of client_corporation_appointments based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the client_corporation_appointments.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the client_corporation_appointments.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of client_corporation_appointments to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning client_corporation_appointments.
          Defaults to 0.

        Returns:
        - List[ClientCorporationAppointment]: A list of client_corporation_appointments matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/ClientCorporationAppointment?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_corporate_users(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[corporate_user.CorporateUser]:
        """
        Sends a GET request to the REST API to retrieve a list of corporate users based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the corporate users.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the corporate users.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of corporate users to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning corporate users.
          Defaults to 0.

        Returns:
        - List[CorporateUser]: A list of corporate users matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/CorporateUser?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_countries(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[country.Country]:
        """
        Sends a GET request to the REST API to retrieve a list of countries based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the countries.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the countries.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of countries to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning countries.
          Defaults to 0.

        Returns:
        - List[Country]: A list of countries matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Country?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_departments(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[department.Department]:
        """
        Sends a GET request to the REST API to retrieve a list of departments based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the departments.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the departments.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of departments to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning departments.
          Defaults to 0.

        Returns:
        - List[Department]: A list of departments matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Department?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_employee_pays(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[employee_pay.EmployeePay]:
        """
        Sends a GET request to the REST API to retrieve a list of employee pays based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the employee pays.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the employee pays.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of employee pays to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning employee pays.
          Defaults to 0.

        Returns:
        - List[EmployeePay]: A list of employee pays matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/EmployeePay?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_employer_contributions(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[employer_contribution.EmployerContribution]:
        """
        Sends a GET request to the REST API to retrieve a list of employer contributions based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the employer contributions.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the employer contributions.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of employer contributions to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning employer contributions.
          Defaults to 0.

        Returns:
        - List[EmployerContribution]: A list of employer contributions matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/EmployerContribution?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_job_orders(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[job_order.JobOrder]:
        """
        Sends a GET request to the REST API to retrieve a list of job orders based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the job orders.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the job orders.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of job orders to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning job orders.
          Defaults to 0.

        Returns:
        - List[JobOrder]: A list of job orders matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/JobOrder?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_job_submissions(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[job_submission.JobSubmission]:
        """
        Sends a GET request to the REST API to retrieve a list of job submissions based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the job submissions.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the job submissions.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of job submissions to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning job submissions.
          Defaults to 0.

        Returns:
        - List[JobSubmission]: A list of job submissions matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/JobSubmission?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_job_submission_histories(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[job_submission_history.JobSubmissionHistory]:
        """
        Sends a GET request to the REST API to retrieve a list of job submission histories based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the job submission histories.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the job submission histories.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of job submission histories to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning job submission histories.
          Defaults to 0.

        Returns:
        - List[JobSubmissionHistory]: A list of job submission histories matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/JobSubmissionHistory?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_leads(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[lead.Lead]:
        """
        Sends a GET request to the REST API to retrieve a list of leads based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the leads.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the leads.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of leads to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning leads.
          Defaults to 0.

        Returns:
        - List[Leads]: A list of leads matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Lead?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_lead_histories(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[lead_history.LeadHistory]:
        """
        Sends a GET request to the REST API to retrieve a list of lead histories based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the lead histories.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the lead histories.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of lead histories to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning lead histories.
          Defaults to 0.

        Returns:
        - List[LeadHistory]: A list of lead histories matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/LeadHistory?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_locations(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[location.Location]:
        """
        Sends a GET request to the REST API to retrieve a list of locations based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the locations.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the locations.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of locations to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning locations.
          Defaults to 0.

        Returns:
        - List[Location]: A list of locations matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Location?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_opportunities(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[opportunity.Opportunity]:
        """
        Sends a GET request to the REST API to retrieve a list of opportunities based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the opportunities.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the opportunities.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of opportunities to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning opportunities.
          Defaults to 0.

        Returns:
        - List[Opportunity]: A list of opportunities matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Opportunity?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_opportunity_histories(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[opportunity_history.OpportunityHistory]:
        """
        Sends a GET request to the REST API to retrieve a list of opportunity histories based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the opportunity histories.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the opportunity histories.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of opportunity histories to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning opportunity histories.
          Defaults to 0.

        Returns:
        - List[OpportunityHistory]: A list of opportunity histories matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/OpportunityHistory?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_placements(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[placement.Placement]:
        """
        Sends a GET request to the REST API to retrieve a list of placements based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the placements.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the placements.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of placements to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning placements.
          Defaults to 0.

        Returns:
        - List[Placement]: A list of placements matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Placement?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_placement_commissions(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[placement_commission.PlacementCommission]:
        """
        Sends a GET request to the REST API to retrieve a list of placement commissions based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the placement commissions.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the placement commissions.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of placement commissions to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning placement commissions.
          Defaults to 0.

        Returns:
        - List[PlacementCommission]: A list of placement commissions matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/PlacementCommission?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_sendouts(
        self,
        where: str,
        fields: str,
        order_by: str = "",
        count: int = 10,
        start: int = 0,
    ) -> List[sendout.Sendout]:
        """
        Sends a GET request to the REST API to retrieve a list of sendouts based on specified parameters.

        Parameters:
        - where (str): A string specifying the filter conditions for querying the sendouts.
        - fields (str): A string specifying which fields to include in the returned records.
        - order_by (str, optional): A string specifying the order in which to return the sendouts.
          Defaults to an empty string, which means the order is unspecified.
        - count (int, optional): The maximum number of sendouts to return. Defaults to 10.
        - start (int, optional): The position in the query result to start returning sendouts.
          Defaults to 0.

        Returns:
        - List[Sendout]: A list of sendouts matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url
                + "query/Sendout?where={where}&fields={fields}&orderBy={order_by}&count={count}&start={start}",
                path_params={
                    "where": where,
                    "fields": fields,
                    "order_by": order_by,
                    "count": count,
                    "start": start,
                },
            )
        )
        return request["data"]

    def get_settings(
        self,
        settings: str,
    ) -> List[setting.Setting]:
        """
        Sends a GET request to the REST API to retrieve a list of settings values based on specified parameters.

        Parameters:
        - settings (str): A string specifying which settings values to include in the returned records.

        Returns:
        - List[Setting]: A list of settings matching the query parameters.
        """
        request = self.request(
            Route(
                "GET",
                self.rest_url + "settings/{settings}",
                path_params={
                    "settings": settings,
                },
            )
        )
        return request
