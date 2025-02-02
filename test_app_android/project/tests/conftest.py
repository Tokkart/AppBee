import pytest
from test_app_android.project.utils.driver_setup import setup_driver
from test_app_android.project.utils.data_parser import parse_test_data
from test_app_android.project.pages.main_page import Main
from test_app_android.project.pages.myproducts_page import MyProducts
from test_app_android.project.pages.tariff_up_page import TariffUp
from test_app_android.project.pages.precheck_page import Precheck
from test_app_android.project.pages.check_page import Check
from test_app_android.project.pages.status_page import StatusPage
from test_app_android.project.pages.tariff_list_page import List
import shutil
import os

def pytest_configure(config):
    """Очищает папку с результатами тестов allure-results."""
    allure_results_dir = "allure-results"
    allure_report_dir = "allure-report.html"

    if os.path.exists(allure_results_dir):
        shutil.rmtree(allure_results_dir)
    if os.path.exists(allure_report_dir):
        shutil.rmtree(allure_report_dir)

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
    file_path = r'C:\Users\verli\Downloads\data test2.xlsx'
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
            self.status = StatusPage(driver)
            self.list = List(driver)

    return Pages(driver)

