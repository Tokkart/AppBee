from selenium.webdriver.common.by import By
from pages.base_app import BaseApp


# Стартовая страница main_page.py
class PreCheckPage(BaseApp):
    def delete_dtm(self):   #Проверка отключаемых услуг
        prefixes = ["При изменении тарифа"]
        element = self.find_text_with_prefixes(prefixes)
        delete_dtm_text = element.get_attribute("text")
        if element:
            print(f"Текст про отключение услуг: {delete_dtm_text}")
            return delete_dtm_text
        else:
            print("Текст про отключение услуг не найден.")


    def changing_tariff(self):   #Проверка отключаемых услуг
        prefixes = ["Остаток", "Сейчас"]
        element = self.find_text_with_prefixes(prefixes)
        changing_tariff_text = element.get_attribute("text")
        if element:
            print(f"Текст про изменение тарифа: {changing_tariff_text}")
            return changing_tariff_text
        else:
            print("Текст про изменение тарифа не найден.")


    def button_next(self):
        next_button = self.wait_for_element(By.XPATH, '//android.widget.ScrollView/android.view.View[2]/android.widget.Button')
        next_button.click()

#Класс предчека
class Precheck:
    def __init__(self, driver):
        self.driver = driver
        self.precheck = PreCheckPage(driver)
#Текст с отключаемыми услугами
    def dtm_delete(self):
        self.precheck.delete_dtm()
#Текст с изменением тарифа
    def changing_tariff(self):
        self.precheck.changing_tariff()
#Клик по кнопке продолжить
    def button_next(self):
        self.precheck.button_next()
