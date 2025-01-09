from time import sleep

from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure



# Мои продукты
class MyProductsPage(BaseApp):
    def wait_changes_tariff(self, number, text):
        with allure.step(f'Ожидание изменения тарифа'):
            for i in range(5): #Проверка на изменение тарифа
                element = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{number} {text}")')
                if element:
                    break
                else:
                    self.scroll_up()
                    # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def go_main(self):   #Переход на стартовую страницу
        with allure.step('Переход на стартовую страницу'):
            self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("мои продукты")')
            #Переход на стартовую страницу -> клик по иконке свернуть
            main = self.find_nearby_element(name = "мои продукты", class_name = "android.view.View", y_coordinate = 150, direction = "above")
            try:
                assert main, f'Ошибка: кнопка для перехода на стартовую страницу не найдена'
                main.click()
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def ap(self, number): #Проверка АП
        with allure.step('Проверка стоимости тарифа'):
            text_part = "₽/мес"
            name = "АП"
            result = int(self.find_text_part_element(text_part))
            try:
                allure.attach(f"Ожидаемая: {number}, Полученная: {result}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert result == number, f'Ошибка: неверное значение {name},должно:{number}'
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def gb(self, number): #Проверка ГБ
        with allure.step('Проверка начисленных гигабайт'):
            text_part = "гб"
            name = "ГБ"
            result = int(self.find_text_part_element(text_part))
            try:
                allure.attach(f"Ожидаемая: {number}, Полученная: {result}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert result == number, f'Ошибка: неверное значение {name},должно:{number}, получено: {result}'
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def min(self, number):  #Проверка Мин
        with allure.step('Проверка начисленных минут'):
            text_part = "мин"
            name = "МИН"
            result = int(self.find_text_part_element(text_part))
            try:
                allure.attach(f"Ожидаемая: {number}, Полученная: {result}", name="Значения минут", attachment_type=allure.attachment_type.TEXT)
                assert result == number, f'Ошибка: неверное значение {name},должно:{number}, получено: {result}'
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def name(self, name):  #Проверка Имени ТП
        with allure.step(f'Проверка названия тарифа "{name}"'):
            text = "Имя ТП"
            result = self.get_element_by_text(name).text
            try:
                assert result, f'Ошибка:  {text}:{name}, не найдено'
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def data(self):  # Дата следующего списания
        with allure.step('Проверка даты следующего списания'):
            data = self.data_through_30d() # Определяем дату
            text_part = "оплата спишется"
            name = "Даты"
            result = self.find_text_part_element(text_part)
            try:
                allure.attach(f"Ожидаемая: {data.replace(" ", "")}, Полученная: {result}", name="Дата", attachment_type=allure.attachment_type.TEXT)
                assert result == data.replace(" ", ""), f'Ошибка: неверное значение {name},должно:{data}, получено: {result}'
                # делаем скриншот
                screenshot = self.driver.get_screenshot_as_png()
                # добавляем скриншот в Allure
                allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def setting_click(self):  # Переход в карточку тарифа
        with allure.step('Переход в карточку тарифа'):
            # Переход в карточку тарифа -> клик по настройки тарифа
            name = "настройки тарифа"
            self.button_click(name)
    def change_tariff_click(self):  # Смена тарифа
        with allure.step('Переход в каталог тарифов'):
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
    def wait_changes_tariff(self, number, text):
        self.my_products.wait_changes_tariff(number, text)
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