import pytest
from test_app_android.project.utils.driver_setup import setup_driver
from test_app_android.project.utils.data_parser import parse_test_data
from test_app_android.project.pages.main_page import Main
from test_app_android.project.pages.myproducts_page import MyProducts
from test_app_android.project.pages.tariff_up_page import TariffUp
from test_app_android.project.pages.precheck_page import Precheck
from test_app_android.project.pages.check_page import Check
from test_app_android.project.pages.success_page import SuccessPage


@pytest.fixture(scope="function")
def driver(request):
    """
    Инициализация драйвера для каждого теста.
    """
    driver = setup_driver()
    def fin():
        driver.quit()
    request.addfinalizer(fin)
    return driver


@pytest.fixture(scope="session")
def file_data():
    """
    Загрузка тестовых данных из Excel.
    """
    file_path = r'C:\Users\verli\Downloads\data test.xlsx'
    return parse_test_data(file_path)

@pytest.fixture(scope="function")
def app_pages(driver):
    """
    Фикстура для инициализации всех страниц.
    """
    class Pages:
        def __init__(self, driver):
            self.main = Main(driver)
            self.my_products = MyProducts(driver)
            self.tariff_up = TariffUp(driver)
            self.precheck = Precheck(driver)
            self.check = Check(driver)
            self.success = SuccessPage(driver)

    return Pages(driver)