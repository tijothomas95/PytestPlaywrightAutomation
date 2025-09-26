import pytest

from model.pages.bags_page import BagsPage
from model.pages.base_page import BasePage
from utils.enums import PassengerType
from utils.fake_data import FakePassenger


class SeatsPage(BasePage):
    _passenger_name: None

    def __init__(self, page):
        super().__init__(page, root_selector="seats-root")

    @property
    def _passengers_table_rows(self):
        return self.page.locator("tr.passenger-carousel__table-row-pax")

    @property
    def _passengers_selector(self):
        return self.page.locator("tr.passenger-carousel__table-row-pax", has_text=f"{self._passenger_name}")

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

    @property
    def _loading_spinner(self):
        return self.page.locator('[data-ref="basket.basket-total__icon-spinner"]')

    @property
    def _reserve_same_seats_modal(self):
        return self.page.locator("ry-action-sheet.seats-offer__sheet")

    def click_next_flight(self):
        self._next_flight_btn.click()
        self.wait_for_cart_ready()
        self.wait_for_close_return_offer()

    def click_continue(self):
        self._continue_btn.click()
        self.wait_for_cart_ready()
        return SeatsPage(self.page)

    def add_fast_track(self):
        self._add_fast_track_btn.click()
        return BagsPage(self.page)

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
        self.page.wait_for_timeout(2000)


    def wait_for_cart_ready(self):
        spinner = self._loading_spinner
        self.page.wait_for_function(
            """
            el => !el || window.getComputedStyle(el).opacity === "0"
            """,
            arg=spinner,
            timeout=10000
        )
        cart_icon = self.page.locator('[data-ref="basket.basket-total__icon-cart"]')
        cart_icon.wait_for(state="visible", timeout=10000)
        self.page.wait_for_timeout(3000)

    def wait_for_close_return_offer(self):
        popup = self._reserve_same_seats_modal
        if popup.is_visible(timeout=3000):  # wait max 3s for it
            no_thanks_btn = popup.locator("button:has-text('No, thanks')")
            if no_thanks_btn.is_visible():
                no_thanks_btn.click()
            else:
                close_icon = popup.locator(".seats-offer__sheet-close-icon")
                if close_icon.is_visible():
                    close_icon.click()

            self.page.wait_for_timeout(1000)
