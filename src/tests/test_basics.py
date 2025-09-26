import pytest

from utils.enums import TravelType, Location, PassengerType, FareType
from utils.fake_data import generate_passengers


@pytest.mark.smoke
def test_validate_homepage(home_page):
    assert home_page.page.title() != ""


@pytest.mark.smoke
def test_falsy_title(home_page):
    assert home_page.page.title() == "TBC to remove"


@pytest.mark.parametrize(
"adults, teens, children, infants",
    [
        (2, 1, 1, 1),
    ]
)
@pytest.mark.smoke
def test_search_flights(home_page, adults, teens, children, infants):
    # --- Given ---
    home_page.select_travel_type(TravelType.RETURN_TRIP)
    home_page.fill_departure_fld(Location.DUBLIN)
    home_page.fill_destination_fld(Location.MADRID)

    home_page.select_travel_date("2 October 2025")
    home_page.select_travel_date("03 October 2025")

    home_page.select_passengers(passenger=PassengerType.ADULTS, exp_count=adults)
    home_page.select_passengers(passenger=PassengerType.TEENS, exp_count=teens)
    home_page.select_passengers(passenger=PassengerType.CHILDREN, exp_count=children)
    home_page.select_passengers(passenger=PassengerType.INFANT, exp_count=infants)

    # --- When ---
    flights_page = home_page.click_search()
    fares_page = flights_page.select_suggested_flights()

    passengers_page = fares_page.select_fare_type(FareType.REGULAR)

    # --- Then ---
    assert passengers_page.is_passengers_form_disabled() is True
    passengers_page.click_login_later()
    assert passengers_page.is_passengers_form_disabled() is False

    # --- And when filling passengers ---
    passengers = generate_passengers(adults=adults, teens=teens, children=children, infants=infants)
    passengers_page.fill_all_passengers(passengers)

    # --- Finally ---
    seats_page = passengers_page.click_continue()
    assert home_page.page.title() != ""

