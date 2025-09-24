from src.model.pages.base_page import BasePage


class HomePage(BasePage):

    def __init__(self, page):
        super().__init__(page, root_selector="hp-app-root")

    @property
    def _popup(self):
        return self.page.locator("div.cookie-popup-with-overlay__box")

    @property
    def _btn_view_settings(self):
        return self._popup.get_by_role("button", name="View cookie settings")

    @property
    def _btn_no_thanks(self):
        return self._popup.get_by_role("button", name="No, thanks")

    @property
    def _btn_agree_all(self):
        return self._popup.get_by_role("button", name="Yes, I agree")

    def accept_cookies(self):
        if self._popup.is_visible():
            self._btn_agree_all.click()
