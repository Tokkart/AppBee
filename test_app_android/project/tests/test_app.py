from pages.login_page import TestLoginApp
from utils.driver_setup import setup_driver
import pytest

#Создаем драйвер для управления МП и завершение после
@pytest.fixture(scope="function")
def driver(request):
    driver = setup_driver()

    def fin():
        driver.quit()

    request.addfinalizer(fin)
    return driver

# Авторизация в МП
def test_bee(driver):
    login = TestLoginApp(driver)
    login.test_login("9657531730", "Test2015")








