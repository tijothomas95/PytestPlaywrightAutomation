from datetime import datetime

from model.pages.base_page import BasePage
from model.pages.fares_page import FaresPage
from utils.fake_data import normalize_spaces


class FlightsPage(BasePage):

    def __init__(self, page):
        super().__init__(page, root_selector="flights-root")

    @property
    def _journey_container(self):
        return self.page.locator("journey-container")

    @property
    def _trip_details(self):
        return self.page.locator("flights-trip-details div.details__bottom-bar")

    def actual_journey_details(self):
        act_journey_details = self._trip_details.inner_text().split("\n")[1:]
        act_journey_details = normalize_spaces(" ".join(act_journey_details))
        return act_journey_details

    def expected_journey_details(self, outbound_date, inbound_date, total_passengers):
        outbound_date = datetime.strptime(outbound_date, "%d %B %Y")
        inbound_date = datetime.strptime(inbound_date, "%d %B %Y")
        return f"{outbound_date.strftime('%d %b')} - {inbound_date.strftime('%d %b')} {total_passengers}"

    def select_suggested_flights(self):
        journey_containers = self._journey_container

        outbound_flights = journey_containers.nth(0).locator(
            "flight-card-new:not(.flight-card--disabled)"
        )
        outbound_flights.first.get_by_role("button", name="Select").click()

        inbound_flights = journey_containers.nth(1).locator(
            "flight-card-new:not(.flight-card--disabled)"
        )
        inbound_flights.first.get_by_role("button", name="Select").click()

        return FaresPage(self.page)
