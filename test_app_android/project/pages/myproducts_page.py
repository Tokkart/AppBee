from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure
import pytest

# Мои продукты
class MyProductsPage(BaseApp):
    def wait_changes_tariff(self, number):
        for i in range(12): #Проверка на изменение тарифа
            element = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{number} гб")')
            if element:
                break
            else:
                self.scroll_up()
                # делаем скриншот
        screenshot = self.driver.get_screenshot_as_png()
        # добавляем скриншот в Allure
        allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def go_main(self):   #Переход на стартовую страницу
        #Переход на стартовую страницу -> клик по иконке свернуть
        main = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(14)')
        if main.click():
            main.click()
            print('Переход на стартовую страницу')
        else:
            print('Кнопка выхода из "Мои продукты" не найдена')
    def ap(self, number): #Проверка АП
        with allure.step('Проверка стоимости тарифа'):
            text = f"{number} ₽/мес"
            text_part = "₽/мес"
            name = "АП"
            result = self.find_number_element(text, name, text_part)
            assert result.replace(text_part, '').replace(" ", "") == number, f'Ошибка: неверное значение {name},должно:{text}, получено: {result}'
    def gb(self, number): #Проверка ГБ
        with allure.step('Проверка начисленных гигабайт'):
            text = f"{number} гб"
            text_part = "гб"
            name = "ГБ"
            result = self.find_number_element(text, name, text_part)
            assert result.replace(text_part, '').replace(" ", "") == number, f'Ошибка: неверное значение {name},должно:{text}, получено: {result}'
    def min(self, number):  #Проверка Мин
        with allure.step('Проверка начисленных минут'):
            text = f"{number} мин"
            text_part = "мин"
            name = "МИН"
            result = self.find_number_element(text, name, text_part)
            assert result.replace(text_part, '').replace(" ", "") == number, f'Ошибка: неверное значение {name},должно:{text}, получено: {result}'
    def name(self, name):  #Проверка Имени ТП
        with allure.step('Проверка названия тарифа'):
            text = f"{name}"
            text_part = None
            name = "Имя ТП"
            result = self.find_number_element(text, name, text_part)
            assert result == text, f'Ошибка: неверное значение {name},должно:{text}, получено: {result}'

    def data(self):  # Дата следующего списания
        with allure.step('Проверка даты следующего списания'):
            data = self.data_through_30d() # Определяем дату
            text = f"оплата спишется {data}"
            text_part = "оплата спишется"
            name = "Дата"
            result = self.find_number_element(text, name, text_part)
            assert result == text, f'Ошибка: неверное значение {name},должно:{text}, получено: {result}'
    def setting_click(self):  # Переход в карточку тарифа
        # Переход в карточку тарифа -> клик по настройки тарифа
        name = "настройки тарифа"
        self.button_click(name)
    def change_tariff_click(self):  # Смена тарифа
        # Смена тарифа -> клик по сменить тариф
        name = "сменить тариф"
        self.button_click(name)


@allure.feature('Тестирование тарифа UP')
@allure.title('Страница Мои продукты')
#Класс моих продуктов
class MyProducts:
    def __init__(self, driver):
        self.driver = driver
        self.my_products = MyProductsPage(driver)
#Ожидание изменения тарифа
    def wait_changes_tariff(self, number):
        self.my_products.wait_changes_tariff(number)
#Переход на стартовую страницу
    def go_main(self):
        self.my_products.go_main()
#Переход в смену тарифа
    def change_tariff_click(self):
        self.my_products.change_tariff_click()
#Переходом в настройки тарифа
    def settings_click(self):
        self.my_products.setting_click()
#Проверяем АП
    def ap(self, number):
        self.my_products.ap(number)
#Проверяем ГБ
    def gb(self, number):
        self.my_products.gb(number)
#Проверяем МИН
    def min(self, number):
        self.my_products.min(number)
#Проверяем имя тарифов
    def name(self, number):
        self.my_products.name(number)
#Проверяем дату следующего списания
    def data(self):
        self.my_products.data()