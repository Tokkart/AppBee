from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseApp:
    """Базовый класс для работы с мобильным приложением."""
    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator_type, locator):
        return self.driver.find_element(locator_type, locator)

    def find_elements(self, locator_type, locator):
        return self.driver.find_elements(locator_type, locator)

    def wait_for_element(self, locator_type, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((locator_type, locator))
        )
