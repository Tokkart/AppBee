from test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy
import allure

# Страница чека
@allure.parent_suite("Страница Чека")
class CheckPage(BaseApp):
    def wait_check_page(self, name):
        with allure.step(f'Ожидание чека "{name}"'):
            tariff_up = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')
            assert tariff_up, f'Страница чека "{name}" не найдена.'
    def dtm_name(self, name):   #Проверка отключаемых услуг
        with allure.step(f'Проверка отключаемых услуг "{name}"'):
            if name == '100 SMS':
                name = 'Пакет 100 SMS'
            element = self.get_element_by_text(name)
            try:
                assert element.text, f'"{name}" услуга не найдена.'
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка поиска услуги", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
    def dtm_price(self, name, price, text_part):  #Поиск дтм опций в чеке и их стоимость
        # Поиск стоимости ДТМ
        with allure.step(f'Проверка стоимости услуги "{name}"'):
            if name == '100 SMS':
                name = 'Пакет 100 SMS'
            dtm = self.check_name_price(name, text_part)
            try:
                allure.attach(f"Ожидаемая: {price}, Полученная: {dtm}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert dtm == price, f'Ошибка: неверное значение {name},должно:{price}, получено: {dtm}'
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
    def mobil_text(self, value_gb, value_gb_old, value_min, value_min_old, text_part):   #Проверка текст мобильной связи
        with allure.step('Проверка описания мобильной связи в чеке'):
            prefixes = ["Увеличение", "Новые", f"{value_gb}"]
            element = self.find_text_with_prefixes(prefixes)
            mobil_text = element.text
            if text_part == '₽/мес':
                generate_text = f'{value_gb} ГБ и {value_min} минут'
            else:
                generate_text = self.generate_check_text(value_gb, value_gb_old, value_min, value_min_old)
                print (generate_text)
            if element:
                try:
                    allure.attach(f"Ожидаемый: {generate_text}\nПолученный: {mobil_text}", name="Текст изменений тарифа в чеке", attachment_type=allure.attachment_type.TEXT)
                    assert str(generate_text) == str(mobil_text), f'Ошибка: текст не совпадает\nДолжно: {repr(generate_text)}\nПолученное: {repr(mobil_text)}'
                except AssertionError as e: # Перехватываем именно AssertionError
                    allure.attach(str(e), name="Ошибка, при проверке текста изменений тарифа", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                    raise # Важно пробросить исключение дальше
                except Exception as e: # Обрабатываем другие возможные исключения
                    allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                return mobil_text
    def mobil_price(self, price_tp, price_tp_old, value_gb, value_gb_old, value_min, value_min_old, text_part):
        with allure.step(f'Проверка стоимости мобильной связи'):
            name = self.mobil_text(value_gb, value_gb_old, value_min, value_min_old, text_part)
            delta = price_tp - price_tp_old #Находим сумму доплаты
            if delta <= 0:
                if value_gb > value_gb_old or value_min > value_min_old:
                    delta = 30
                else:
                    delta = 0
            try:
                mobil = self.check_name_price(name, text_part)
                allure.attach(f"Ожидаемая: {delta}, Полученная: {mobil}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert mobil == delta, f'Ошибка: неверное значение "{name}", должно:{delta}, получено: {mobil}'
            except AssertionError as e: # Перехватываем именно AssertionError
                # allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
    def info_text(self, value_gb, value_min, price_tp, value_gb_old, value_min_old, price_tp_old, price_dtm):  #Проверка текста в иконке Инфо
        with allure.step(f'Проверка описания в тултипе info'):
            #Получение текста
            prefixes = ["Остаток", "Сейчас", "Однократная"]
            price = price_tp + price_dtm #итоговая цена
            delta = price_tp - price_tp_old#Находим сумму доплаты
            if delta <= 0:
                if value_gb > value_gb_old or value_min > value_min_old:
                    delta = 30
                else:
                    delta = 0
            self.check_info_click()   #Клик по иконке инфо
            self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("понятно")')
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            element = self.find_text_with_prefixes(prefixes).text
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
    def button_understand_click(self):
        name = "понятно"
        with allure.step(f'Клик по кнопке "{name}"'):
            self.button_click(name)
    def button_price(self, price):  #Поиск дтм опций в чеке и их стоимость
        button = "Оплатить"
        with allure.step(f'Проверка стоимости на кнопке "{button}"'):
            text_part = "₽"
            self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("Оплатить")')
            # Проверка стоимости на кнопке оплатить
            try:
                ap = self.check_name_price(button, text_part)
                allure.attach(f"Ожидаемая: {price}, Полученная: {ap}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert ap == price, f'Ошибка: неверное значение {button}, должно:{price}, получено: {ap}'
            except AssertionError as e: # Перехватываем именно AssertionError
                # allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
    def single_payment(self, price = 200):  #Проверка разового платежа
        element = "Разовый платеж"
        with allure.step(f'Проверка стоимости элемента "{element}"'):
            text_part = "₽"
            # Проверка стоимости 200р
            try:
                ap = self.check_name_price(element, text_part)
                allure.attach(f"Ожидаемая: {price}, Полученная: {ap}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert ap == price, f'Ошибка: неверное значение {element}, должно:{price}, получено: {ap}'
            except AssertionError as e: # Перехватываем именно AssertionError
                # allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
    def button_pay_click(self):
        name = "Оплатить"
        with allure.step(f'Клик по кнопке "{name}"'):
            self.button_click(name)
    def button_save_click(self):
        name = "Сохранить"
        with allure.step(f'Клик по кнопке "{name}"'):
            self.button_click(name)

@allure.feature('Тестирование тарифа UP')
#Класс предчека
class Check:
    def __init__(self, driver):
        self.driver = driver
        self.check = CheckPage(driver)
#Ожидание страницы чека
    def wait_check_page(self, name):
        self.check.wait_check_page(name)
# Стоимость мобильной связи
    def mobil_price(self, price_tp, price_tp_old, value_gb, value_gb_old, value_min, value_min_old, text_part):
        self.check.mobil_price(price_tp, price_tp_old, value_gb, value_gb_old, value_min, value_min_old, text_part)
#Текст мобильной связи, описание изменений
    def mobil_text(self, value_gb, value_gb_old, value_min, value_min_old, text_part):
        self.check.mobil_text(value_gb, value_gb_old, value_min, value_min_old, text_part)
#Проверка наличия опций в чеке
    def dtm_name(self, name):
        self.check.dtm_name(name)
#Стоимость опции дтм
    def dtm_price(self, name, price, text_part):
        self.check.dtm_price(name, price, text_part)
#Проверка стоимости разового платежа
    def single_payment(self):
        self.check.single_payment()
# Проверка текста в иконке Инфо
    def info_text(self, value_gb, value_min, price_tp, value_gb_old, value_min_old, price_tp_old, price_dtm):
        self.check.info_text(value_gb, value_min, price_tp, value_gb_old, value_min_old, price_tp_old, price_dtm)
#Клик по кнопке понятно
    def button_understand_click(self):
        self.check.button_understand_click()
# Проверка цены на кнопке оплатить
    def button_price(self, price):
        self.check.button_price(price)
#Клик по кнопке оплатить
    def button_pay_click(self):
        self.check.button_pay_click()
#Клик по кнопке Сохранить
    def button_save_click(self):
        self.check.button_save_click()

