from selenium.webdriver.common.by import By
from beeline.AppBee.AppBee.test_app_android.project.pages.base_app import BaseApp

# Класс c шагами авторизации в МП
class LoginPage(BaseApp):
    def login(self, phone, password):

        self.wait_for_element(By.XPATH, "//android.widget.TextView[@text='войти']").click()
        self.wait_for_element(By.XPATH, "//android.widget.TextView[@text='или по логину и паролю']").click()
        self.find_element(By.XPATH, "//android.widget.EditText[@text='+7']").click()
        self.find_element(By.XPATH, "//android.widget.EditText[@text='+7']").send_keys(phone)
        self.find_element(By.XPATH,"//android.widget.ScrollView/android.widget.EditText[2]").send_keys(password)
        self.find_element(By.XPATH, "//android.widget.TextView[@text='войти']").click()

#Класс с тестами авторизации в МП
class TestLoginApp:
    def __init__(self, driver):
        self.driver = driver
        self.login_page = LoginPage(driver)

    def test_login(self, phone, password):
        self.login_page.login(phone, password)