from selenium.webdriver.common.by import By
from pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime
from datetime import date, timedelta
import locale

from datetime import datetime, timedelta

# Мои продукты
class MyProductsPage(BaseApp):
    def go_main(self):   #Переход на стартовую страницу
        #Переход на стартовую страницу -> клик по иконке свернуть
        self.wait_for_element(By.XPATH, "(//android.widget.FrameLayout[@resource-id='ru.beeline.services.staging:id/bottom_bar_fragment_container'])[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View", 10).click()
    def ap(self, number): #Проверка АП
        text = f"{number} ₽/мес"
        text_part = "₽/мес"
        name = "АП"
        self.find_number_element(text, name, text_part)
    def gb(self, number): #Проверка ГБ
        text = f"{number} гб"
        text_part = "гб"
        name = "ГБ"
        self.find_number_element(text, name, text_part)
    def min(self, number):  #Проверка Мин
        text = f"{number} мин"
        text_part = "мин"
        name = "МИН"
        self.find_number_element(text, name, text_part)
    def name(self, name):  #Проверка Имени ТП
        text = f"{name}"
        text_part = None
        name = "Имя ТП"
        self.find_number_element(text, name, text_part)
    def data(self):  # Дата следующего списания
        data = self.data_through_30d() # Определяем дату
        text = f"оплата спишется {data}"
        text_part = "оплата спишется"
        name = "Дата"
        self.find_number_element(text, name, text_part)
    def go_setting(self):  # Переход в карточку тарифа
        # Переход в картоку тарифа -> клик по настройки тарифа
        self.wait_for_element(By.XPATH,'//android.widget.TextView[@text="настройки тарифа"]',10).click()
    def go_change_tariff(self):  # Смена тарифа
        # Смена тарифа -> клик по сменить тариф
        self.wait_for_element(By.XPATH,'//android.widget.TextView[@text="сменить тариф"]',10).click()

#Класс моих продуктов
class MyProducts:
    def __init__(self, driver):
        self.driver = driver
        self.my_products = MyProductsPage(driver)
#Переход на стартовую страницу
    def go_main(self):
        self.my_products.myprodact_main()
#Переход в смену тарифа
    def go_change_tariff(self):
        self.my_products.myprodact_changetarif()
#Переходом в настройки тарифа
    def go_settings(self):
        self.my_products.myprodact_setting()
#Проверяем АП
    def ap(self, number):
        self.my_products.ap(number)
#Проверяем ГБ
    def gb(self, number):
        self.my_products.gb(number)
#Проверяем МИН
    def min(self, number):
        self.my_products.min(number)
#Проверяем имя тарифв
    def name(self, number):
        self.my_products.name(number)
#Проверяем дату следующего списания
    def data(self):
        self.my_products.data()