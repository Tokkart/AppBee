from selenium.webdriver.common.by import By
from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure

@allure.feature('Тестирование тарифа UP')
@allure.title('Страница предчека')
# Стартовая страница main_page.py
class PreCheckPage(BaseApp):
    def wait_page_precheck(self):
        with allure.step('Ожидание страницы предчека'):
            name = "Проверим, что меняется"
            precheck = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')
            assert precheck, 'Ошибка: страницы предчека не найдена'
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def delete_dtm(self, name):   #Проверка отключаемых услуг
        with allure.step('Проверка отключаемых услуг в предчеке'):
            prefixes = ["При изменении тарифа"]
            element = self.find_text_with_prefixes(prefixes)
            if element:
                try:
                    assert name in element.text, f'Ошибка: опция "{name}" не найдена'
                except AssertionError as e: # Перехватываем именно AssertionError
                    allure.attach(str(e), name="Ошибка проверки отображения услуги", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                    raise # Важно пробросить исключение дальше
                except Exception as e: # Обрабатываем другие возможные исключения
                    allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def changing_tariff(self, value_gb, value_min, price_tp, value_gb_old, value_min_old, price_tp_old, price_dtm):   #Проверка текста, при изменении пакетов тарифа
        with (allure.step('Проверка описания изменений тарифа в предчеке')):
            prefixes = ["Остаток", "Сейчас"]
            price = price_tp + price_dtm #итоговая цена
            delta = price_tp - price_tp_old#Находим сумму доплаты
            if delta <= 0:
                if value_gb > value_gb_old or value_min > value_min_old:
                    delta = 30
                else:
                    delta = 0
            element = self.find_text_with_prefixes(prefixes).text #Поиск текста по первому слову (префиксу)
            name = self.generate_changing_tariff_text(value_gb, value_gb_old, value_min, value_min_old, delta, price, price_dtm) #Создаем ожидаемый текст на основе параметров
            if element:
                try:
                    allure.attach(f"Ожидаемый: {name}\nПолученный: {element}", name="Текст изменений тарифа", attachment_type=allure.attachment_type.TEXT)
                    assert str(name) == str(element), f'Ошибка: текст не совпадает\nДолжно: {repr(name)}\nПолученное: {repr(element)}'
                except AssertionError as e: # Перехватываем именно AssertionError
                    allure.attach(str(e), name="Ошибка, при проверке текста изменений тарифа", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                    raise # Важно пробросить исключение дальше
                except Exception as e: # Обрабатываем другие возможные исключения
                    allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def button_next(self):
        with allure.step('Переход в чек'):
            next_button = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)')
            try:
                assert next_button, 'Ошибка: не найден кнопка "Продолжить"'
                next_button.click()
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
#Класс предчека
class Precheck:
    def __init__(self, driver):
        self.driver = driver
        self.precheck = PreCheckPage(driver)
#Ожидание предчека
    def wait_page_precheck(self):
        self.precheck.wait_page_precheck()
#Текст с отключаемыми услугами
    def dtm_delete(self, name):
        self.precheck.delete_dtm(name)
#Текст с изменением тарифа
    def changing_tariff(self, value_gb, value_min, price_tp, value_gb_old, value_min_old, price_tp_old, price_dtm):
        self.precheck.changing_tariff(value_gb, value_min, price_tp, value_gb_old, value_min_old, price_tp_old, price_dtm)
#Клик по кнопке продолжить
    def button_next(self):
        self.precheck.button_next()
