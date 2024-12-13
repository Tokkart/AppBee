from tabnanny import check

from selenium.webdriver.common.by import By
from beeline.AppBee.AppBee.test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy

# Стартовая страница main_page.py
class CheckPage(BaseApp):
    def wait_check_page(self, name):
        tariff_up = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')
        if tariff_up:
            print()
        else:
            print(f'"{name}" страница с чеком не найдена.')
    def check_dtm_name(self, name):   #Проверка отключаемых услуг
        element = self.get_element_by_text(name)
        if element:
            print(f'Опция: "{name}". найдена.')
            return element.text
        else:
            print(f'Опция: "{name}". не найдена.')
            return None
    def check_dtm_price(self, name, price):  #Поиск дтм опций в чеке и их стоимость
        # Поиск стоимости ДТМ
        text_part = "₽"
        self.check_name_price(name, price, text_part)

    def check_mobil_text(self):   #Проверка текст мобильной связи
        prefixes = ["Увеличение", "Новые"]
        element = self.find_text_with_prefixes(prefixes)
        mobil_text = element.text
        if element:
            print(f"Текст про изменение тарифа:\n {mobil_text}")
            return mobil_text
        else:
            print("Текст про изменение тарифа не найден.")
            return None
    def check_mobil_price(self, price):  #Поиск стоимости за мобильную связь
        name = self.check_mobil_text()
        text_part = "₽"
        self.check_name_price(name, price, text_part)

    def check_button_pay_click(self):   #Клик по кнопке оплатить
        self.button_pay_click()

    def check_info_text(self):  #Проверка текста в иконке Инфо
        self.check_info()   #Клик по иконке инфо
        #Получение текста
        prefixes = ["Остаток", "Сейчас", "Однократная"]
        info = self.find_text_with_prefixes(prefixes)
        info_text = info.text
        if info_text:
            print(f"Текст в иконке инфо:\n {info_text}")
            self.button_understand_click()    #Клик по кнопке понятно
            return info_text
        else:
            print("Текст в иконке инфо не найден.")
            self.button_understand_click()
    def check_button_price(self, price):  #Поиск дтм опций в чеке и их стоимость
        button = "Оплатить"
        text_part = "₽"
        # Поиск стоимости ДТМ
        self.check_name_price(button, price, text_part)

#Класс предчека
class Check:
    def __init__(self, driver):
        self.driver = driver
        self.check = CheckPage(driver)
#Ожидание страницы чека
    def wait_check_page(self, name):
        self.check.wait_check_page(name)
#Стоимость опции дтм
    def check_dtm_price(self, name, price):
        self.check.check_dtm_price(name, price)
# Стоимость мобильной связи
    def check_mobil_price(self, price):
        self.check.check_mobil_price(price)
#Текст мобильной связи, описание изменений
    def check_mobil_text(self):
        self.check.check_mobil_text()
#Проверка наличия опций в чеке
    def check_dtm_name(self, name_dtm):
        self.check.check_dtm_name(name_dtm)
# Проверка текста в иконке Инфо
    def check_info_text(self):
        self.check.check_info_text()
# Проверка цены на кнопке оплатить
    def check_button_price(self, price):
        self.check.check_button_price(price)
#Клик по кнопке оплатить
    def check_button_pay_click(self):
        self.check.check_button_pay_click()

