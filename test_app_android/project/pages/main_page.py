from appium.webdriver.common.appiumby import AppiumBy
from test_app_android.project.pages.base_app import BaseApp
import allure

@allure.feature('Тестирование тарифа UP')
@allure.title('Страница Главного экрана')
# Стартовая страница main_page.py
class MainPage(BaseApp):
    def go_my_product(self):   #Переход в мои продукты
        #Переход в мои продукты
        go_my_product = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(20)')
        if go_my_product:
            go_my_product.click()
            print('Переход в "Мои продукты"')
        else:
            print('Кнопка для перехода в "Мои продукты" не найдена')
#Класс стартовой страницы
class Main:
    def __init__(self, driver):
        self.driver = driver
        self.page_main = MainPage(driver)
#Переходом из стартовой страницы в мои продукты
    def go_my_product(self):
        self.page_main.go_my_product()
