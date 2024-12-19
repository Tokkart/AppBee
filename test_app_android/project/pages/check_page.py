from selenium.webdriver.common.by import By
from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure
import pytest
import pytest_check as check


# Страница чека
@allure.parent_suite("Страница Чека")
class CheckPage(BaseApp):
    def wait_check_page(self, name):
        tariff_up = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')
        if tariff_up:
            print()
        else:
            print(f'"{name}" страница с чеком не найдена.')
    def dtm_name(self, name):   #Проверка отключаемых услуг
        with allure.step(f'Проверка отключаемых услуг "{name}"'):
            element = self.get_element_by_text(name)
            assert element.text, f'"{name}" услуга не найдена.'
    def dtm_price(self, name, price):  #Поиск дтм опций в чеке и их стоимость
        # Поиск стоимости ДТМ
        with allure.step(f'Проверка стоимости услуги "{name}"'):
            text_part = "₽"
            dtm = self.check_name_price(name, price, text_part)
            assert dtm == price, f'Ошибка: неверное значение {name},должно:{price}, получено: {dtm}'
    def mobil_text(self):   #Проверка текст мобильной связи
        prefixes = ["Увеличение", "Новые"]
        element = self.find_text_with_prefixes(prefixes)
        mobil_text = element.text
        if element:
            print(f"Проверка чека:\n {mobil_text}")
            return mobil_text
        else:
            print("Текст, про изменения тарифа, не найден.")
            return None
    def mobil_price(self, price):
        with allure.step(f'Проверка стоимости мобильной связи: "{price}"'):
            name = self.mobil_text()
            text_part = "₽"
            mobil = self.check_name_price(name, price, text_part)
            assert mobil == price, f'Ошибка: неверное значение "{name}", должно:{price}, получено: {mobil}'
            # check.equal( mobil,price, f'Ошибка: неверное значение "{name}", должно:{price}, получено: {mobil}')
            # print("Проверка прошла успешно") #Сообщение будет выведено, если assert истинный

    def info_text(self):  #Проверка текста в иконке Инфо
        #Получение текста
        prefixes = ["Остаток", "Сейчас", "Однократная"]
        name = "понятно"
        self.check_info_click()   #Клик по иконке инфо
        self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("понятно")')
        # делаем скриншот
        screenshot = self.driver.get_screenshot_as_png()
        # добавляем скриншот в Allure
        allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
        info = self.find_text_with_prefixes(prefixes)
        info_text = info.text
        if info_text:
            print(f"Текст в тултипе info:\n {info_text}")
            self.button_click(name)    #Клик по кнопке понятно
            return info_text
        else:
            print("Текст в тултипе info не найден.")
            self.button_click(name)
    def button_price(self, price):  #Поиск дтм опций в чеке и их стоимость
        with allure.step('Проверка стоимости на кнопке "Оплатить"'):
            button = "Оплатить"
            text_part = "₽"
            # Проверка стоимости на кнопке оплатить
            self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Оплатить")')
            ap = self.check_name_price(button, price, text_part)
            assert ap == price, f'Ошибка: неверное значение {button},должно:{price}, получено: {ap}'
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def button_pay_click(self):
        name = "Оплатить"
        self.button_click(name)

@allure.feature('Тестирование тарифа UP')
#Класс предчека
class Check:
    def __init__(self, driver):
        self.driver = driver
        self.check = CheckPage(driver)
#Ожидание страницы чека
    def wait_check_page(self, name):
        self.check.wait_check_page(name)
#Стоимость опции дтм
    def dtm_price(self, name, price):
        self.check.dtm_price(name, price)
# Стоимость мобильной связи
    def mobil_price(self, price):
        self.check.mobil_price(price)
#Текст мобильной связи, описание изменений
    def mobil_text(self):
        self.check.mobil_text()
#Проверка наличия опций в чеке
    def dtm_name(self, name_dtm):
        self.check.dtm_name(name_dtm)
# Проверка текста в иконке Инфо
    def info_text(self):
        self.check.info_text()
# Проверка цены на кнопке оплатить
    def button_price(self, price):
        self.check.button_price(price)
#Клик по кнопке оплатить
    def button_pay_click(self):
        self.check.button_pay_click()


