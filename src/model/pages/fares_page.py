from model.pages.base_page import BasePage
from model.pages.login_page import PassengersPage
from utils.enums import FareType


class FaresPage(BasePage):
    _fare_type = None

    def __init__(self, page):
        super().__init__(page, root_selector="fare-selector-container")

    @property
    def _fare_table(self):
        return self.page.locator("fare-table-new-layout")

    @property
    def _fare_column(self):
        return self._fare_table.get_by_role("columnheader", name=f"{self._fare_type} Fare")

    def select_fare_type(self, fare_type: FareType):
        self._fare_type = str(fare_type)
        self._fare_column.click()
        return PassengersPage(self.page)





