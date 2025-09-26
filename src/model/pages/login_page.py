from datetime import datetime

from model.pages.base_page import BasePage
from model.pages.seats_page import SeatsPage
from utils.enums import PassengerType
from utils.fake_data import FakePassenger


class PassengersPage(BasePage):
    _title = None
    _passenger_form_container = None

    def __init__(self, page):
        super().__init__(page, root_selector="flights-passengers")

    @property
    def _login_container(self):
        return self.page.locator("ry-login-touchpoint-container")

    @property
    def _login_later_btn(self):
        return self._login_container.get_by_text("Log in later")

    @property
    def _passengers_form(self):
        return self.page.locator("div.form-wrapper")

    @property
    def _passenger_containers(self):
        return self.page.locator("div.passenger")

    @property
    def _title_field(self):
         return self._passenger_form_container.locator("button.dropdown__toggle")

    @property
    def _title_option(self):
        return self._passenger_form_container.locator("button.dropdown-item__link").filter(has_text=self._title)

    @property
    def _first_name_field(self):
        return self._passenger_form_container.locator("input[autocomplete='given-name']")

    @property
    def _last_name_field(self):
        return self._passenger_form_container.locator("input[autocomplete='family-name']")

    @property
    def _dob_field(self):
        return self._passenger_form_container.locator("input[name*='dateOfBirth']")

    @property
    def _continue_btn(self):
        return self.page.get_by_role("button", name="Continue")

    def is_passengers_form_disabled(self):
        return "disabled" in self._passengers_form.get_attribute("class")

    def click_login_later(self):
        self._login_later_btn.click()

    def click_continue(self):
        self._continue_btn.click()
        return SeatsPage(self.page)

    def fill_all_passengers(self, passengers: list[FakePassenger]):
        for passenger in passengers:
            self.enter_passenger_details(passenger)

    def enter_passenger_details(self, passenger: FakePassenger):
        passenger_blocks = self._passenger_containers
        self._passenger_form_container = (passenger_blocks
                                          .filter(has_text=passenger.form_passenger_type).nth(passenger.index))

        if passenger.search_passenger_type in [PassengerType.ADULTS, PassengerType.TEENS]:
            self._title = passenger.title
            self._title_field.click()
            self._title_option.click()

        self._first_name_field.fill(passenger.first_name)
        self._last_name_field.fill(passenger.last_name)

        if self._dob_field.is_visible():
            dob = datetime.strptime(passenger.dob, "%d/%m/%Y")
            iso_dob = dob.strftime("%Y-%m-%d")  # required by type="date"
            self._dob_field.fill(iso_dob)
