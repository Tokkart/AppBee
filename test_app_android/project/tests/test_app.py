from pages.login_page import TestLoginApp
from utils.driver_setup import setup_driver
from pages.main_page import Main
from pages.myprodact_page import MyProdact
from pages.tarif_up_page import TarifUp
from pages.precheck_page import Precheck

import pytest

from beeline.AppBee.AppBee.test_app_android.project.pages.precheck_page import Precheck


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
    main_page = Main(driver) #стартовая страница
    myprodact_page = MyProdact(driver) #мои продукты
    name_dtm = "Видео"
    value_gb = "300"
    value_min = "2000"
    tarifup_page = TarifUp(driver)
    precheck_page = Precheck(driver)
    #Авторизация - проблема с капчей
    # login.test_login("9657531730", "Test2015")
    #Стартовая страница -> переход в мои продукты
    # main_page.go_myprodact()
    # мои продукты -> переход на стартовую страницу
    # myprodact_page.go_main()
    # мои продукты -> переход в настройки тарифа
    # myprodact_page.go_settings()
    # выбог ГБ
    #tarifup_page.select_gb(value_gb)
    # выбор МИН
    #tarifup_page.select_min(value_min)
    #клик далее
    #tarifup_page.select_button_next()
    # print(f"Начало теста для опции '{name_dtm}'")
    # tarifup_page.dtm_scroll()
    # tarifup_page.dtm_select(name_dtm)
    # tarifup_page.dtm_ap(name_dtm)
    precheck_page.dtm_delete()
    precheck_page.changing_tariff()












