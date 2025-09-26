from model.pages.base_page import BasePage
from model.pages.fares_page import FaresPage


class FlightsPage(BasePage):

    def __init__(self, page):
        super().__init__(page, root_selector="flights-root")

    @property
    def _journey_container(self):
        return self.page.locator("journey-container")

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
