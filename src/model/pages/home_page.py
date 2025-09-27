from datetime import datetime

from model.pages.flights_page import FlightsPage
from src.model.pages.base_page import BasePage
from utils.enums import TravelType, Location, PassengerType


class HomePage(BasePage):
    _travel_type = None
    _passenger_type = None

    def __init__(self, page):
        super().__init__(page, root_selector="hp-app-root")

    @property
    def _cookie_popup(self):
        return self.page.locator("div.cookie-popup-with-overlay__box")

    @property
    def _btn_view_settings(self):
        return self._cookie_popup.get_by_role("button", name="View cookie settings")

    @property
    def _btn_no_thanks(self):
        return self._cookie_popup.get_by_role("button", name="No, thanks")

    @property
    def _btn_agree_all(self):
        return self._cookie_popup.get_by_role("button", name="Yes, I agree")

    @property
    def _travel_type_btn(self):
        return self.page.locator("label.ry-radio-circle-button__label", has_text=self._travel_type)

    @property
    def _departure_fld(self):
        return self.page.get_by_placeholder(text="Departure")

    @property
    def _destination_fld(self):
        return self.page.get_by_placeholder(text="Destination")

    @property
    def _airport_list(self):
        return self.page.locator("fsw-airport-item")

    @property
    def _datepicker(self):
        return self.page.locator("fsw-flexible-datepicker-container")

    @property
    def _passenger_fld(self):
        return self.page.get_by_role("button", name="Passengers")

    @property
    def _passenger_picker(self):
        match self._passenger_type:
            case PassengerType.ADULTS:
                return self.page.locator("[data-ref='passengers-picker__adults']")
            case PassengerType.TEENS:
                return self.page.locator("[data-ref='passengers-picker__teens']")
            case PassengerType.CHILDREN:
                return self.page.locator("[data-ref='passengers-picker__children']")
            case PassengerType.INFANT:
                return self.page.locator("[data-ref='passengers-picker__infant']")
            case _:
                raise ValueError(f"Unable to find locator for passenger type: {self._passenger_type}")

    @property
    def _passenger_counter(self):
        return self._passenger_picker.locator("div[data-ref='counter.counter__value']")

    @property
    def _passenger_counter_increment(self):
        return self._passenger_picker.locator("[data-ref='counter.counter__increment']")

    @property
    def _passenger_counter_decrement(self):
        return self._passenger_picker.locator("[data-ref='counter.counter__decrement']")

    @property
    def _search_flight_btn(self):
        return self.page.get_by_role("button", name="Search")

    @property
    def _dependent_info_modal(self):
        return self.page.locator("passengers-dependent-modal-content")

    @property
    def _accept_dependent_info_modal(self):
        return self._dependent_info_modal.get_by_role("button", name="Ok, got it")

    def title(self) -> str:
        return self.get_title()

    def accept_cookies(self):
        if self._cookie_popup.is_visible():
            self._btn_agree_all.click()

    def select_travel_type(self, travel_type: TravelType):
        self._travel_type = str(travel_type)
        if not self._travel_type_btn.is_checked():
            self._travel_type_btn.check()

    def fill_airport_field(self, field, place: Location):
        place = str(place)
        field.clear()
        field.fill(place)

        self._airport_list.filter(has_text=place).click()

    def fill_departure_fld(self, place: Location):
        self.fill_airport_field(self._departure_fld, place)

    def fill_destination_fld(self, place: Location):
        self.fill_airport_field(self._destination_fld, place)

    def select_travel_date(self, date_str):
        date_obj = datetime.strptime(date_str, "%d %B %Y")
        year = date_obj.strftime("%Y")
        month_name = date_obj.strftime("%B")
        day = date_obj.strftime("%-d")

        matching_cal = None
        target_month_year = f"{month_name} {year}"
        is_found = False
        i = 0

        # Keep moving until we see the right month/year
        for _ in range(9):
            calendar_names = self._datepicker.locator("div[data-ref='calendar-month-name']")

            month_loc = self._datepicker.locator(".m-toggle__month")
            if month_loc.count() > i:
                month_loc.nth(i).click()
                i += 2

            # Look for matching month/year
            matching_cal = calendar_names.filter(has_text=target_month_year)
            if matching_cal.count() > 0:
                is_found = True
                break

            self._datepicker.locator("icon[iconid='glyphs/chevron-right']").first.click()

        if not is_found:
            raise ValueError(f"Could not find month {target_month_year} in datepicker")

        calendar_root = matching_cal.first.locator("..")
        day_loc = calendar_root.locator(f"div[data-value='{day}']")
        if "disabled" in day_loc.get_attribute("class"):
            raise ValueError(f"Cannot select disabled date: {day} {month_name} {year}")

        day_loc.click()

    def select_passengers(self, passenger: PassengerType, exp_count: int):
        self._passenger_type = passenger
        value_locator = self._passenger_counter

        current_count = int(value_locator.text_content().strip())
        consent_accepted = False

        # Increment until expected count
        while current_count < exp_count:
            self._passenger_counter_increment.click()
            if passenger != PassengerType.ADULTS and not consent_accepted:
                if self._dependent_info_modal.is_visible():
                    self._accept_dependent_info_modal.click()
                    consent_accepted = True

            current_count = int(value_locator.text_content().strip())

        # Decrement until expected count
        while current_count > exp_count:
            self._passenger_counter_decrement.click()
            current_count = int(value_locator.text_content().strip())


    def select_passenger_list(self, adults: int, teens: int, children: int, infants: int):
        self.select_passengers(passenger=PassengerType.ADULTS, exp_count=adults)
        self.select_passengers(passenger=PassengerType.TEENS, exp_count=teens)
        self.select_passengers(passenger=PassengerType.CHILDREN, exp_count=children)
        self.select_passengers(passenger=PassengerType.INFANT, exp_count=infants)


    def click_search(self):
        self._search_flight_btn.click()
        return FlightsPage(self.page)
