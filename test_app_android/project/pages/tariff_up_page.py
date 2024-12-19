from selenium.webdriver.common.by import By
from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure


@allure.feature('Тестирование тарифа UP')
@allure.title('Конструктор тарифа UP')
# Тариф UP -> Объекты страницы
class TariffUpPage(BaseApp):
    def wait_page(self, name):
        tariff_up = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name.lower()}")')
        if tariff_up is None:
            print(f'"{name}" страница не найдена.')
    def gb(self, value):  #Поиск и выбор ГБ
        with allure.step(f'Выбираем ГБ "{value}"'):
            name = "гб"
            self.find_element_with_swipe(value, name)
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def min(self, value):  #Поиск и выбор Мин
        with allure.step(f'Выбираем МИН "{value}"'):
            name = "мин"
            self.find_element_with_swipe(value, name)
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def dtm_toggle_click(self, name_dtm):  # Выбор ДТМ опции
        with allure.step(f'Клик по тогглу "{name_dtm}"'):
            self.toggle_click(name_dtm)
    def scroll_down_up(self): #Прокрутка экрана вниз
        print(f"Выполняется прокрутка вниз...")
        self.scroll_down()
    def dtm_ap(self, name, price):  # АП ДТМ опции
        with allure.step(f'Проверяем стоимость "{name}" "{price}"'):
            text_part = "₽/мес"
            # Получаем строку, содержащую цену
            ap_dtm = self.child_element_ap(name, text_part)
            # Если не удалось найти цену, вернем None
            if not ap_dtm:
                print(f"Не удалось найти стоимость для опции '{name}'.")
                return None
            # Убираем "₽/мес" и пробелы из строки с ценой
            ap = ap_dtm.replace(text_part, "").replace(" ", "")
            # Сравниваем полученную цену с ожидаемой
            assert ap == price, f'Ошибка: неверное значение "{name}", должно: {price}, получено: {ap}.'
    def button_next_click(self):   #Кнопка далее
        #Клик кнопки продолжить
        name = "Продолжить"
        self.button_click(name)
    def check_button_price(self, price):  # Поиск дтм опций в чеке и их стоимость
        with allure.step('Проверяем стоимости на кнопке "Продолжить"'):
            name = "Продолжить"
            text_part = "₽/мес"
            # Поиск стоимости ДТМ
            ap = self.check_name_price(name, price, text_part)
            assert ap == price, f'Ошибка: неверное значение {name},должно:{price}, получено: {ap}'
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)


#Класс Тариф UP -> Действия с объектами
class TariffUp:
    def __init__(self, driver):
        self.driver = driver
        self.up = TariffUpPage(driver)
#Ожидание страницы тарифа UP
    def wait_page(self, name):
        self.up.wait_page(name)
#Выбор ГБ
    def select_gb(self, value_gb):
        self.up.gb(value_gb)
#Выбор МИН
    def select_min(self, value_gb):
        self.up.min(value_gb)
#Скролл вниз
    def scroll_down_up(self):
        self.up.scroll_down_up()
# Выбор ДТМ опции
    def dtm_toggle_click(self, name_dtm):
        self.up.dtm_toggle_click(name_dtm)
# Получение АП за ДТМ опцию
    def dtm_ap(self, name, price):
        return self.up.dtm_ap(name, price)
#Получение АП за выбранные параметры
    def button_price(self, price):
        self.up.check_button_price(price)
#Клик по кнопке далее
    def button_next_click(self):
        self.up.button_next_click()

