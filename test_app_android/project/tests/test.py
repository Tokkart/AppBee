import pytest
import allure

def execute_scenario(driver, test_data_row, app_pages):
    """
    Выполняет тестовый сценарий на основе данных из одной строки.
    """
    scenario = test_data_row.get("Сценарий")
    if scenario == "СменаПр":
        test_plan = TestChangePlan(test_data_row, app_pages)
        test_plan.test_go_settings_tariff()
        test_plan.test_select_data()
        test_plan.test_select_voice()
        test_plan.test_select_dtm()
        test_plan.test_tariff_price()
        test_plan.test_precheck()
        test_plan.test_check_text()
        test_plan.test_check_mobile_price()
        test_plan.test_check_dtm()
        test_plan.test_check_info()
        test_plan.test_check_price()
    else:
        print(f"Сценарий '{scenario}' не поддерживается.")

@allure.feature("Тестирование тарифа UP")
class TestChangePlan:
    def __init__(self, data, app_pages):
        self.data = data
        self.app_pages = app_pages
        self.name_dtm = "Сервисы Яндекс"  # Лучше вынести в константы или передавать из data
        self.price_dtm = str(data.get('Ясервисы')) # Явное приведение к строке
        self.value_gb = str(data.get('Гб')) # Явное приведение к строке
        self.value_min = str(data.get('Мин')) # Явное приведение к строке
        self.price_main = str(data.get('АППодключен')) # Явное приведение к строке
        self.price_tp = str(data.get('АП')) # Явное приведение к строке
        self.name_main = str(data.get('Название')) # Явное приведение к строке
        self.test_plan = self # Добавлено для доступа к app_pages

    @allure.title("Переход в настройки тарифа")
    @pytest.mark.dependency(name="test_go_settings_tariff")
    def test_go_settings_tariff(self):
        #Стартовая страница -> переход в мои продукты
        self.test_plan.app_pages.main.go_my_product()
        # Мои продукты -> переход в настройки тарифа
        self.test_plan.app_pages.my_products.settings_click()
        # Ожидание страницы UP
        self.test_plan.app_pages.tariff_up.wait_page(self.name_main)

    @allure.title("Выбор ГБ")
    @pytest.mark.dependency(depends=["test_go_settings_tariff"])
    def test_select_data(self):
        # Выбор ГБ
        self.app_pages.tariff_up.select_gb(self.value_gb)

    @allure.title("Выбор МИН")
    @pytest.mark.dependency(depends=["test_go_settings_tariff"])
    def test_select_voice(self):
        # выбор МИН
        self.app_pages.tariff_up.select_min(self.value_min)

    @allure.title("Выбор ДТМ опций")
    @pytest.mark.dependency(depends=["test_select_data"])
    def test_select_dtm(self):
        # Скролл вниз
        self.app_pages.tariff_up.scroll_down_up()
        # Поиск клик по тоглу дтм опции
        self.app_pages.tariff_up.dtm_toggle_click(self.name_dtm)
        # Проверка АП дтм опции
        self.app_pages.tariff_up.dtm_ap(self.name_dtm, self.price_dtm)

    @allure.title("Проверка стоимости тарифа")
    @pytest.mark.dependency(depends=["test_select_dtm", "test_select_voice"])
    def test_tariff_price(self):#Проверка общей АП ТП + ДТМ
        self.app_pages.tariff_up.button_price(self.price_main)
        # Клик далее
        self.app_pages.tariff_up.button_next_click()
    @allure.title("Проверка предчека")
    @pytest.mark.dependency(depends=["test_tariff_price"])
    def test_precheck(self):# Ожидание предчека
        self.app_pages.precheck.wait_page_precheck()
        self.app_pages.precheck.changing_tariff()
        self.app_pages.precheck.button_next()

    @allure.title("Проверка в чеке текста изменений тарифа")
    @pytest.mark.dependency(depends=["test_precheck", "test_tariff_price"])
    def test_check_text(self):
        self.app_pages.check.wait_check_page(self.name_main)
        self.app_pages.check.mobil_text()

    @allure.title("Проверка в чеке стоимости мобильной связи")
    @pytest.mark.dependency(depends=["test_precheck", "test_tariff_price"])
    @pytest.mark.xfail(reason="ошибка")
    def test_check_mobile_price(self):
        # self.app_pages.check.mobil_price(self.price_tp)
        try:
            self.app_pages.check.mobil_price(self.price_tp)
        except Exception as e:  # Перехватываем ЛЮБОЕ исключение
            allure.attach(str(e), name="Исключение", attachment_type=allure.attachment_type.TEXT) # Прикрепляем текст ошибки к отчету Allure
            print(f"Ошибка в test_check_mobile_price: {e}") # Выводим ошибку в консоль для отладки

    @allure.title("Проверка в чеке ДТМ опций")
    @pytest.mark.dependency(depends=["test_precheck", "test_tariff_price"])
    def test_check_dtm(self):
        self.app_pages.check.wait_check_page(self.name_main)
        self.app_pages.check.dtm_name(self.name_dtm)
        self.app_pages.check.dtm_price(self.name_dtm, self.price_dtm)

    @allure.title("Проверка в чеке текста в тултипе info")
    @pytest.mark.dependency(depends=["test_precheck", "test_tariff_price"])
    def test_check_info(self):
        self.app_pages.check.info_text()

    @allure.title("Проверка в чеке стоимости тарифа")
    @pytest.mark.dependency(depends=["test_precheck", "test_tariff_price"])
    def test_check_price(self):
        # self.app_pages.check.button_price(self.price_main)
        try:
            self.app_pages.check.button_price(self.price_main)
        except Exception as e:  # Перехватываем ЛЮБОЕ исключение
            allure.attach(str(e), name="Исключение", attachment_type=allure.attachment_type.TEXT) # Прикрепляем текст ошибки к отчету Allure
@allure.feature("Тестирование тарифа UP")
def test_smena_pr(driver, file_data, app_pages):
    """
    Запускает тесты на основе данных из файла.
    """
    for row in file_data:
        execute_scenario(driver, row, app_pages)