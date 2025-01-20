from time import sleep

from appium.webdriver.common.appiumby import AppiumBy
from test_app_android.project.pages.base_app import BaseApp
import allure

@allure.feature('Тестирование тарифа UP')
@allure.title('Страница Главного экрана')
# Стартовая страница main_page.py
class MainPage(BaseApp):
    with allure.step(f'Переход в Мои продукты'):
        def go_my_product(self):   #Переход в мои продукты
            #Переход в мои продукты
            go_my_product = self.wait_for_element(AppiumBy.XPATH, '(//android.widget.FrameLayout[@resource-id="ru.beeline.services:id/bottom_bar_fragment_container"])[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.widget.ScrollView/android.view.View[2]/android.widget.ScrollView/android.view.View[1]/android.view.View[2]')
            try:
                assert go_my_product, 'Кнопка для перехода в мои продукты не найдена'
                go_my_product.click()
                sleep(1)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
#Класс стартовой страницы
class Main:
    def __init__(self, driver):
        self.driver = driver
        self.page_main = MainPage(driver)
#Переходом из стартовой страницы в мои продукты
    def go_my_product(self):
        self.page_main.go_my_product()
