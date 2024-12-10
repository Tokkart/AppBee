from selenium.webdriver.common.by import By
from pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy

# Стартовая страница main_page.py
class PreCheckPage(BaseApp):
    def delete_dtm(self):   #Проверка отключаемых услуг
        prefixes = ["При изменении тарифа"]
        element = self.find_text_with_prefixes(prefixes)
        delete_dtm_text = element.get_attribute("text")
        if element:
            print(f"Текст про отключение услуг: {delete_dtm_text}")

        else:
            print("Текст про отключение услуг не найден.")

        return (delete_dtm_text)
    def changing_tariff(self):   #Проверка отключаемых услуг
        prefixes = ["Остаток", "Сейчас"]
        element = self.find_text_with_prefixes(prefixes)
        changing_tariff_text = element.get_attribute("text")
        if element:
            print(f"Текст про изменение тарифа: {changing_tariff_text}")

        else:
            print("Текст про изменение тарифа.")

        return (changing_tariff_text)


#Класс предчека
class Precheck:
    def __init__(self, driver):
        self.driver = driver
        self.precheck = PreCheckPage(driver)
#Отключаемые услуги
    def dtm_delete(self):
        self.precheck.delete_dtm()
#Изменение тарифа
    def changing_tariff(self):
        self.precheck.changing_tariff()