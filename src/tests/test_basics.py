import pytest

from src.model.pages.home_page import HomePage


@pytest.mark.smoke
def test_homepage(web_page):
    home_pg = HomePage(web_page)
    home_pg.accept_cookies()

    assert web_page.title() != ""
    print("Page title:", web_page.title())
