from appium.webdriver.common.appiumby import AppiumBy
from test_app_android.project.pages.base_app import BaseApp
import allure

@allure.feature('Тестирование тарифа UP')
@allure.title('Страница со списком тарифов доступных для смены тп')
# Стартовая страница main_page.py
class ListPage(BaseApp):

        def go_tariff(self, name):   #Переход в карточку тарифа
            with allure.step(f'Поиск и выбор тарифа "{name}"'):
                #Ожидание загрузки страницы
                self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("тарифы")')
                #Поиск и выбор тарифа
                max_attempts = 3
                attempt = 0
                tariff = None
                while attempt < max_attempts and not tariff:
                    tariff = self.find_nearby_element(name, class_name = "android.widget.Button", y_coordinate = 500, direction='below')
                    if not tariff:
                        attempt += 1
                        print(f"Попытка скролла вниз: {attempt}")
                        self.scroll_down()
                try:
                    assert tariff, f'Ошибка: тариф не найден'
                    tariff.click()
                except AssertionError as e: # Перехватываем именно AssertionError
                    allure.attach(str(e), name="Ошибка поиска карточки тарифа", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                    raise # Важно пробросить исключение дальше
                except Exception as e: # Обрабатываем другие возможные исключения
                    allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
#Класс стартовой страницы
class List:
    def __init__(self, driver):
        self.driver = driver
        self.list = ListPage(driver)
#Переходом из стартовой страницы в мои продукты
    def go_tariff(self, name):
        self.list.go_tariff(name)
