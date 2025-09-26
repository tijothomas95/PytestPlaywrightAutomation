from model.pages.bags_page import BagsPage
from model.pages.base_page import BasePage
from utils.enums import PassengerType
from utils.fake_data import FakePassenger


class SeatsPage(BasePage):

    def __init__(self, page):
        super().__init__(page, root_selector="seats-root")

    @property
    def _next_flight_btn(self):
        return self.page.get_by_role("button", name="Next Flight")

    @property
    def _inbound_flight_icon(self):
        return self.page.locator("icon.passenger-carousel__plane-icon--inbound")

    @property
    def _continue_btn(self):
        return self.page.get_by_role("button", name="Continue")

    @property
    def _beta_takeover_modal(self):
        return self.page.locator("ry-enhanced-takeover-beta-desktop")

    @property
    def _add_fast_track_btn(self):
        return self._beta_takeover_modal.get_by_role("button", name="Add fast track")

    def click_next_flight(self):
        self._next_flight_btn.click()
        self.page.wait_for_timeout(5000)
        #self._inbound_flight_icon.wait_for(state="visible")

    def click_continue(self):
        self._continue_btn.click()
        return SeatsPage(self.page)

    def add_fast_track(self):
        self._add_fast_track_btn.click()
        return BagsPage(self.page)

    def old_select_seats(self, passengers: list[FakePassenger]):
        used_seats = set()

        for passenger in passengers:
            if passenger.search_passenger_type == PassengerType.INFANT:
                # Infant seat → must be baby seat
                seat = self.page.locator(
                    "button.seatmap__seat--priority:has(icon[iconid='glyphs/baby'])"
                ).first

            elif passenger.search_passenger_type in [PassengerType.CHILDREN, PassengerType.TEENS]:
                # Children → standard or priority seat, but NOT exit rows
                seat = self.page.locator(
                    "button.seatmap__seat:not(.seatmap__seat--unavailable)"
                    ":not(.seatmap__seat--extraleg)"  # exclude XL/exit rows
                ).nth(len(used_seats))

            else:
                # Adults/Teens → any available seat (including extraleg)
                seat = self.page.locator(
                    "button.seatmap__seat:not(.seatmap__seat--unavailable)"
                ).nth(len(used_seats))

            # Ensure uniqueness
            seat_id = seat.get_attribute("id")
            if seat_id in used_seats:
                continue

            seat.click()
            used_seats.add(seat_id)

    def select_seats(self, passengers: list[FakePassenger]):
        used_seats = set()

        for passenger in passengers:
            if passenger.search_passenger_type == PassengerType.INFANT:
                # Infant → only baby seat
                seat = self.page.locator(
                    "button.seatmap__seat--priority:has(icon[iconid='glyphs/baby'])"
                ).first

            elif passenger.search_passenger_type in [PassengerType.CHILDREN, PassengerType.TEENS]:
                # Children/Teens → no exit row (plane-gates) and no XL seats
                seat = self.page.locator(
                    "div.seatmap__seatrow:not(:has(.plane-gates)) "
                    "button.seatmap__seat:not(.seatmap__seat--unavailable)"
                    ":not(.seatmap__seat--extraleg)"
                ).nth(len(used_seats))

            else:
                # Adults → any available seat
                seat = self.page.locator(
                    "button.seatmap__seat:not(.seatmap__seat--unavailable)"
                ).nth(len(used_seats))

            seat_id = seat.get_attribute("id")
            if seat_id in used_seats:
                continue

            seat.click()
            used_seats.add(seat_id)



