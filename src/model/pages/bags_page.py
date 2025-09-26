from model.pages.base_page import BasePage


class BagsPage(BasePage):

    def __init__(self, page):
        super().__init__(page, root_selector="bags-root")

    @property
    def _checkin_bags(self):
        return self.page.locator("div[data-ref='checkin-bag-expanded']")

    def checkin_bags_card(self):
        return self._checkin_bags