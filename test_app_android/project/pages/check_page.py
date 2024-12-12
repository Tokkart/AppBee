from tabnanny import check

from selenium.webdriver.common.by import By
from pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy

# Стартовая страница main_page.py
class CheckPage(BaseApp):
    def check_dtm_price(self, value_gb):  #Поиск дтм опций в чеке и их стоимость
        # Поиск стоимости ДТМ
        dtm_price = self.check_name_price(value_gb)

        # Если число найдено
        if dtm_price:
            print(f"Найден  элемент {value_gb}, стоимость: {dtm_price}.")
            return dtm_price
    def check_mobil_price(self):  #Поиск стоимости за мобильную связь
        mobil_price = self.check_mobilprice()

        if mobil_price:
            return mobil_price

    def check_dtm_name(self, name_dtm):   #Проверка отключаемых услуг
        element = self.get_element_by_text(name_dtm)
        if element:
            print(f'Опция: "{name_dtm}". найдена.')
            return name_dtm
        else:
            print(f'Опция: "{name_dtm}". не найдена.')


    def check_mobil_text(self):   #Проверка отключаемых услуг
        prefixes = ["Увеличение", "Новые"]
        element = self.find_text_with_prefixes(prefixes)
        mobil_text = element.get_attribute("text")
        if element:
            print(f"Текст про изменение тарифа:\n {mobil_text}")
            return mobil_text

        else:
            print("Текст про изменение тарифа не найден.")

        return mobil_text
    def check_button_pay_click(self):   #Клик по кнопке оплатить
        self.button_pay_click()

    def check_info_text(self):  #Проверка текста в иконке Инфо
        self.check_info()   #Клик по иконке инфо
        #Получение текста
        prefixes = ["Остаток", "Сейчас", "Однократная"]
        info = self.find_text_with_prefixes(prefixes)
        info_text = info.get_attribute("text")
        if info_text:
            print(f"Текст в иконке инфо:\n {info_text}")
            self.button_understand_click()    #Клик по кнопке понятно
            return info_text
        else:
            print("Текст в иконке инфо не найден.")
            self.button_understand_click()
    def check_button_price(self):  #Поиск дтм опций в чеке и их стоимость
        button = "Оплатить"
        # Поиск стоимости ДТМ
        button_price = self.check_name_price(button)

        # Если число найдено
        if button_price:
            print(f"Проверка стоимости на кнопке {button}, цена: {button_price}.")
            return button_price
        else:
            print(f"Проверка стоимости на кнопке {button}, цена не найдена.")

#Класс предчека
class Check:
    def __init__(self, driver):
        self.driver = driver
        self.check = CheckPage(driver)

#Стоимость опции дтм
    def check_dtm_price(self, name_dtm):
        self.check.check_dtm_price(name_dtm)
# Стоимость мобильной связи
    def check_mobil_price(self):
        self.check.check_mobil_price()
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
    def check_button_price(self):
        self.check.check_button_price()
#Клик по кнопке оплатить
    def check_button_pay_click(self):
        self.check.check_button_pay_click()

