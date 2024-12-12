from selenium.webdriver.common.by import By
from pages.base_app import BaseApp


# Стартовая страница main_page.py
class MainPage(BaseApp):
    def main_myprodact(self):   #Переход в мои продукты
        #Переход в мои продукты -> клик по иконке развернуть
        self.wait_for_element(By.XPATH, "(//android.widget.FrameLayout[@resource-id=\'ru.beeline.services.staging:id/bottom_bar_fragment_container'])[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.widget.ScrollView/android.view.View[2]/android.widget.ScrollView/android.view.View[1]/android.view.View[2]", 10).click()


#Класс стартовой страницы
class Main:
    def __init__(self, driver):
        self.driver = driver
        self.main_go_myprodact = MainPage(driver)
#переходом из стартовой страницы в мои продукты
    def go_myprodact(self):
        self.main_go_myprodact.main_myprodact()