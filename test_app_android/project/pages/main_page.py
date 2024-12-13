from appium.webdriver.common.appiumby import AppiumBy
from beeline.AppBee.AppBee.test_app_android.project.pages.base_app import BaseApp

# Стартовая страница main_page.py
class MainPage(BaseApp):
    def go_my_product(self):   #Переход в мои продукты
        #Переход в мои продукты -> клик по иконке развернуть
        profile = self.wait_for_element(AppiumBy.ACCESSIBILITY_ID, 'Профиль')
        if profile:
            print('Профиль найден')
        else:
            print('Профиль не найден')
        go_my_product = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(23)')
        if go_my_product:
            go_my_product.click()
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
