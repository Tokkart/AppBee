
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

#Создаем драйвер для управления МП и завершение после
@pytest.fixture(scope="function")
def driver(request):
    driver = setup_driver()
    def fin():
        driver.quit()
    request.addfinalizer(fin)
    return driver

# Тесты в МП
def test_bee(driver):
    login = TestLoginApp(driver) #страницы авторизации
    page_main = Main(driver) #стартовая страница
    my_products_page = MyProducts(driver) #мои продукты
    name_dtm = "Сервисы Яндекс"
    value_gb = "70"
    value_min = "2000"
    ap_main = "830"
    gb_main = "70"
    min_main = "800"
    name_main = "Тариф UP"

    tariff_up_page = TariffUp(driver)
    precheck_page = Precheck(driver)
    check_page = Check(driver)
    success_page = SuccessPage(driver)
    #Авторизация - проблема с капчей
    # login.test_login("9657531730", "Test2015")
    #Стартовая страница -> переход в мои продукты
    # page_main.go_my_product()
    # мои продукты -> переход на стартовую страницу
    # my_products_page.go_main()
    # Мои продукты -> переход в настройки тарифа
    my_products_page.go_settings()
    # Проверка АП тарифа после смены
    # my_products_page.ap(ap_main)
    # # Проверка ГБ тарифа после смены
    # my_products_page.gb(gb_main)
    # # Проверка МИН тарифа после смены
    # my_products_page.min(min_main)
    # # Проверка Имени тарифа после смены
    # my_products_page.name(name_main)
    # # Проверка Даты списания тарифа после смены
    # my_products_page.data()
    # Ожидание страницы UP
    tariff_up_page.wait_tariff_up_page(name_main)
    # Выбор ГБ
    tariff_up_page.select_gb(value_gb)
    # выбор МИН
    tariff_up_page.select_min(value_min)
    #Клик далее
    #tarifup_page.select_button_next()
    # Скролл вниз
    #tariff_up_page.scroll_down_up()
    # Поиск клик по тоглу дтм опции
    # tariff_up_page.dtm_select(name_dtm)
    # Проверка АП дтм опции
    # tariff_up_page.dtm_ap(name_dtm)
    # Текст с отключаемыми услугами
    # precheck_page.dtm_delete()
    # # Текст с изменением тарифа
    # precheck_page.changing_tariff()
    # Клик по кнопке продолжить
    # precheck_page.button_next()
    # Стоимость опции дтм
    #check_page.check_dtm_price(name_dtm)
    # Стоимость мобильной связи
    # check_page.check_mobil_text()
    # check_page.check_mobil_price()
    # check_page.check_dtm_name(name_dtm)
    # check_page.check_info_text()
    # check_page.check_button_price()
    # check_page.check_button_pay_click()
    # Текст с отключаемыми услугами
    # success_page.page_text()
    # # Клик по кнопке продолжить
    # success_page.button_understand()







