from model.pages.base_page import BasePage


class SeatsPage(BasePage):

    def __init__(self, page):
        super().__init__(page, root_selector="seats-root")

