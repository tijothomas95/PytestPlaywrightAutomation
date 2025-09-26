from playwright.sync_api import Page, expect


class BasePage:
    def __init__(self, page: Page, root_selector: str = None, timeout: int = 15000, validate: bool = True):
        self.page = page
        self.root = None

        if root_selector:
            self.root = page.locator(root_selector)

            if validate:
                try:
                    self.root.wait_for(state="visible", timeout=timeout)
                except TimeoutError:
                    raise AssertionError(
                        f"Page did not load: root '{root_selector}' not visible within {timeout}ms")

    def navigate(self, url):
        self.page.goto(url)

    def get_title(self):
        return self.page.title()

    def screenshot(self, name: str = "screenshot.png"):
        self.page.screenshot(path=name)
