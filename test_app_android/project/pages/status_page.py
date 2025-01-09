from selenium.webdriver.common.by import By
from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure

@allure.feature('Тестирование тарифа UP')
@allure.title('Страница успеха')
# Стартовая страница main_page.py
class StatusPage(BaseApp):
    def success_text(self):
        with allure.step(f'Проверка страницы успеха'):
            #Проверка на наличие запроса на оставления отзыва в гугл
            feedback = self.if_element_exist(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Не сейчас")')
            if feedback:
                feedback.click()
            #Ожидание кнопки понятно
            self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("понятно")')
            #Проверка корректности текста заголовка
            heading_success_page = self.get_element_by_text("Всё получилось") #Заголовок
            text_success_page = self.get_element_by_text("Изменения вступят в силу в течение 10 минут. \nМы пришлём SMS с деталями") #Текст
            try:
                assert heading_success_page and text_success_page, f'Ошибка: неверный текст страницы успеха'
                # делаем скриншот
                screenshot = self.driver.get_screenshot_as_png()
                # добавляем скриншот в Allure
                allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка текста страницы", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def low_balance_text(self):
        with allure.step(f'Проверка страницы недостаточности баланса'):
            #Ожидание страницы недостаточности баланса
            self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("На балансе не хватает денег")')
            #Проверка корректности текста заголовка
            heading_success_page = self.get_element_by_text("На балансе не хватает денег") #Заголовок
            text_success_page = self.get_element_by_text("Пополните баланс или воспользуйтесь «Доверительным платежом»") #Текст
            try:
                assert heading_success_page and text_success_page, f'Ошибка: неверный текст страницы недостаточности баланса'
                # делаем скриншот
                screenshot = self.driver.get_screenshot_as_png()
                # добавляем скриншот в Allure
                allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка текста страницы", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def pay_balance(self):
        with allure.step(f'Проверка пополнения баланса'):
            #Клик по кнопке пополнения баланса
            self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("android.widget.Button")').click()
            #Ожидание страницы пополнения баланса
            pay_balance = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("что пополним")')
            try:
                assert pay_balance, f'Ошибка: не открылась страница пополнения баланса баланса'
                # делаем скриншот
                screenshot = self.driver.get_screenshot_as_png()
                # добавляем скриншот в Allure
                allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка текста страницы", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def button_understand_click(self):
        name = "понятно"
        with allure.step(f'Клик по кнопке {name}'):
            self.button_click(name)

#Класс Экран с различными статусами
class Success:
    def __init__(self, driver):
        self.driver = driver
        self.status = StatusPage(driver)
#Экран успеха
    def success_text(self):
        self.status.success_text()
#Экран недостаточности баланса
    def low_balance_text(self):
        self.status.low_balance_text()
#Переход в пополнение баланса
    def pay_balance(self):
        self.status.pay_balance()
#Клик по кнопке продолжить
    def button_understand_click(self):
        self.status.button_understand_click()
