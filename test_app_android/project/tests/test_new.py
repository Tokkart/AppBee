from time import sleep

from beeline.AppBee.AppBee.test_app_android.project.pages.login_page import TestLoginApp
from beeline.AppBee.AppBee.test_app_android.project.utils.driver_setup import setup_driver
from beeline.AppBee.AppBee.test_app_android.project.pages.main_page import Main
from beeline.AppBee.AppBee.test_app_android.project.pages.myproducts_page import MyProducts
from beeline.AppBee.AppBee.test_app_android.project.pages.tariff_up_page import TariffUp
from beeline.AppBee.AppBee.test_app_android.project.pages.precheck_page import Precheck
from beeline.AppBee.AppBee.test_app_android.project.pages.check_page import Check
from beeline.AppBee.AppBee.test_app_android.project.pages.success_page import SuccessPage
import pytest
import openpyxl
import pandas as pd


# Фикстура для драйвера
@pytest.fixture(scope="function")
def driver(request):
    driver = setup_driver()
    def fin():
        driver.quit()
    request.addfinalizer(fin)
    return driver


# Новая фикстура для получения данных из Excel
@pytest.fixture(scope="session")
def test_data():
    file_path = r'C:\Users\verli\Downloads\data test.xlsx'
    return parse_test_data(file_path)

def parse_test_data(file_path):
    """
    Функция для чтения и фильтрации данных из Excel-файла.
    Возвращает список словарей, где каждая строка представляет тестовый набор данных.
    """
    # Читаем данные
    data = pd.ExcelFile(file_path)
    sheet_data = data.parse('Global')

    # Удаляем строки с пустыми сценариями
    filtered_data = sheet_data.dropna(subset=['Сценарий'])

    # Преобразуем строки в список словарей
    test_data = filtered_data.to_dict(orient='records')

    return test_data

def execute_scenario(driver, test_data_row):
    """
    Выполняет тестовый сценарий на основе данных из одной строки.
    """
    scenario = test_data_row.get('Сценарий')

    # Маппинг сценариев на методы тестов
    scenario_mapping = {
        'СменаТп': change_tariff,
        'СменаПр': change_plan,
    }

    # Выполнение соответствующего метода
    test_method = scenario_mapping.get(scenario)
    if test_method:
        test_method(driver, test_data_row)
    else:
        print(f"Сценарий '{scenario}' не поддерживается.")


def change_tariff(data):
    """Пример реализации теста для смены тарифа."""
    print(f"Выполняется смена тарифа для номера {data.get('Номер')}.")

def change_plan(driver, data):
    """Пример реализации теста для смены плана."""
    print(f"Выполняется смена пресета для номера {data.get('Номер')}.")
    page_main = Main(driver)  # стартовая страница
    my_products_page = MyProducts(driver)  # мои продукты
    tariff_up_page = TariffUp(driver)
    precheck_page = Precheck(driver)
    check_page = Check(driver)
    success_page = SuccessPage(driver)
    name_dtm = "Сервисы Яндекс"
    price_dtm = f"{data.get('Ясервисы')}"
    value_gb = f"{data.get('Гб')}"
    value_min = f"{data.get('Мин')}"
    price_main = f"{data.get('АППодключен')}"
    price_tp = f"{data.get('АП')}"
    gb_main = f"{data.get('ГбПодключен')}"
    min_main = f"{data.get('МинПодключен')}"
    name_main = f"{data.get('Название')}"
    # Стартовая страница -> переход в мои продукты
    page_main.go_my_product()
    # Мои продукты -> переход в настройки тарифа
    my_products_page.go_settings()
    # Ожидание страницы UP
    tariff_up_page.wait_tariff_up_page(name_main)
    # Выбор ГБ
    tariff_up_page.select_gb(value_gb)
    # выбор МИН
    tariff_up_page.select_min(value_min)
    # Скролл вниз
    tariff_up_page.scroll_down_up()
    # Поиск клик по тоглу дтм опции
    tariff_up_page.dtm_select(name_dtm)
    # Проверка АП дтм опции
    tariff_up_page.dtm_ap(name_dtm, price_dtm)
    #Проверка общей АП ТП + ДТМ
    tariff_up_page.button_price(price_main)
    # Клик далее
    tariff_up_page.select_button_next()
    # Ожидание предчека
    precheck_page.wait_page_precheck()
    # Текст с отключаемыми услугами
    # precheck_page.dtm_delete()
    # # Текст с изменением тарифа
    precheck_page.changing_tariff()
    # Клик по кнопке продолжить
    precheck_page.button_next()
    # Ожидание страницы чека
    check_page.wait_check_page(name_main)
    # Стоимость опции дтм
    check_page.check_dtm_price(name_dtm, price_dtm)
    # Проверка описания мобильной связи
    check_page.check_mobil_text()
    # Стоимость мобильной связи
    check_page.check_mobil_price(price_tp)
    # Проверка в чеке дтм опции
    # check_page.check_dtm_name(name_dtm)
    # Проверка описания в тултипе ИНФО
    check_page.check_info_text()
    #Проверка АП на кнопке оплатить
    check_page.check_button_price(price_main)
    #Клик по кнопке оплатить
    check_page.check_button_pay_click()
    # Текст с отключаемыми услугами
    success_page.page_text()
    # Клик по кнопке продолжить
    success_page.button_understand_click()
    # Проверка АП тарифа после смены
    my_products_page.ap(price_main)
    # # Проверка ГБ тарифа после смены
    my_products_page.gb(gb_main)
    # Проверка МИН тарифа после смены
    my_products_page.min(min_main)
    # # Проверка Имени тарифа после смены
    my_products_page.name(name_main)
    # # Проверка Даты списания тарифа после смены
    my_products_page.data()


# Тестовая функция, использующая обе фикстуры
def test_smena_pr(driver, test_data):
    for row in test_data:
        execute_scenario(driver, row)
# def test_smena_pr(driver, test_data):
#     for index, row in enumerate(test_data):
#         if index == 0:
#             execute_scenario(driver, row)
#             break
#         else:
#             continue