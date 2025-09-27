import pytest
import re
from playwright.sync_api import expect

from utils.enums import TravelType, Location, PassengerType, FareType
from utils.fake_data import generate_passengers, get_trip_dates

@pytest.mark.smoke
def test_home_page_title(home_page):
    expect(home_page.page).to_have_title(re.compile("Ryanair"))

@pytest.mark.parametrize(
"adults, teens, children, infants",
    [(2, 0, 0, 0)]
)
@pytest.mark.regression
def test_search_flights(home_page, adults, teens, children, infants):
    # --- Given ---
    home_page.select_travel_type(TravelType.RETURN_TRIP)
    home_page.fill_departure_fld(Location.DUBLIN)
    home_page.fill_destination_fld(Location.MADRID)

    outbound_date, inbound_date = get_trip_dates(days_from_today=14, return_after_days=15)
    home_page.select_travel_date(outbound_date)
    home_page.select_travel_date(inbound_date)

    home_page.select_passenger_list(adults, teens, children, infants)

    # --- When ---
    flights_page = home_page.click_search()

    total_passengers = adults + teens + children + infants
    expected_journey_details = flights_page.expected_journey_details(outbound_date, inbound_date, total_passengers)
    assert expected_journey_details == flights_page.actual_journey_details(), "Mismatched journey details"

    fares_page = flights_page.select_suggested_flights()

    passengers_page = fares_page.select_fare_type(FareType.REGULAR)

    # --- Then ---
    assert passengers_page.is_passengers_form_disabled() is True, "Passengers form not disabled"
    passengers_page.click_login_later()
    assert passengers_page.is_passengers_form_disabled() is False, "Passengers form is disabled"

    # --- And when filling passengers ---
    passengers = generate_passengers(adults=adults, teens=teens, children=children, infants=infants)
    passengers_page.fill_all_passengers(passengers)

    # --- And when selecting seats ---
    seats_page = passengers_page.click_continue()
    seats_page.select_seats(passengers)
    seats_page.click_next_flight()
    seats_page.select_seats(passengers)
    seats_page.click_continue()
    bags_page = seats_page.add_fast_track()

    # --- Then ---
    expect(bags_page._checkin_bags).to_be_visible()
