from selenium.webdriver.common.by import By
from beeline.AppBee.AppBee.test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy

# Стартовая страница main_page.py
class SuccessPage(BaseApp):
    def page_text(self):
        self.wait_for_element( AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.TextView")', 20)
        heading_success_page = self.get_element_by_text("Всё получилось")
        text_success_page = self.get_element_by_text("Изменения вступят в силу в течение 10 минут. \nМы пришлём SMS с деталями")
        if heading_success_page and text_success_page:
           print(f'Проверка экрана успеха, изменение успешно, текст экрана:\n{heading_success_page.text}\n{text_success_page.text}')
        else:
            print("Проверка экрана успеха, ошибка, текст экрана:")
            # Найти все элементы с текстом
            elements = self.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.TextView")'
            )
            # Получить первые два элемента и вывести их текст
            for element in elements[:2]:
                print(element.text)
    def button_understand(self):
        self.button_understand_click()

#Класс Экран успеха
class Success:
    def __init__(self, driver):
        self.driver = driver
        self.success_page = SuccessPage(driver)
#Текст с отключаемыми услугами
    def page_text(self):
        self.success_page.page_text()
#Клик по кнопке продолжить
    def button_understand(self):
        self.success_page.button_understand()
