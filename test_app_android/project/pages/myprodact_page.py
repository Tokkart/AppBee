from selenium.webdriver.common.by import By
from pages.base_app import BaseApp

# Мои продукты
class MyProdactPage(BaseApp):
    def myprodact_main(self):   #Переход на стартовую страницу
        #Переход на стартовую страницу -> клик по иконке свернуть
        self.wait_for_element(By.XPATH, "(//android.widget.FrameLayout[@resource-id='ru.beeline.services.staging:id/bottom_bar_fragment_container'])[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View", 10).click()
    def myprodact_ap(self): #АП
        self.wait_for_element(By.XPATH,'//android.widget.TextView[@text="840 ₽/мес"]',10)
    def myprodact_gb(self): #ГБ
        self.wait_for_element(By.XPATH,'//android.widget.TextView[@text="50 гб"]',10)
    def myprodact_min(self):  # Мин
        self.wait_for_element(By.XPATH, '//android.widget.TextView[@text="300 мин"]', 10)
    def myprodact_name(self):  # Имя ТП
        self.wait_for_element(By.XPATH, '//android.widget.TextView[@text="Тариф UP"]', 10)
    def myprodact_data(self):  # Дата следующего списания
        self.wait_for_element(By.XPATH, '//android.widget.TextView[@text="оплата спишется 1 января"]', 10)
    def myprodact_setting(self):  # Переход в картоку тарифа
        # Переход в картоку тарифа -> клик по настройки тарифа
        self.wait_for_element(By.XPATH,'//android.widget.TextView[@text="настройки тарифа"]',10).click()
    def myprodact_changetarif(self):  # Смена тарифа
        # Смена тарифа -> клик по сменить тариф
        self.wait_for_element(By.XPATH,'//android.widget.TextView[@text="сменить тариф"]',10).click()

#Класс моих продуктов
class MyProdact:
    def __init__(self, driver):
        self.driver = driver
        self.myprodact = MyProdactPage(driver)
#переход на стартовую страницу
    def go_main(self):
        self.myprodact.myprodact_main()
#переход в смену тарифа
    def go_changetarif(self):
        self.myprodact.myprodact_changetarif()
#переходом в настройки тарифа
    def go_settings(self):
        self.myprodact.myprodact_setting()