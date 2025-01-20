from time import sleep
from test_app_android.project.pages.base_app import BaseApp
import allure


@allure.feature('Тестирование тарифа UP')
@allure.title('Конструктор тарифа UP')
# Тариф UP -> Объекты страницы
class TariffUpPage(BaseApp):
    def wait_page_up(self, name):
        name = name.lower()
        with allure.step(f'Ожидание загрузки страницы "{name}"'):
            tariff_up = self.wait_page(name)
            try:
                assert tariff_up, f'Ошибка: карточка тарифа "{name}" не найдена'
                # делаем скриншот
                screenshot = self.driver.get_screenshot_as_png()
                # добавляем скриншот в Allure
                allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка загрузки страницы", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
            sleep(1)
    def gb(self, value):  #Поиск и выбор ГБ
        with allure.step(f'Выбираем ГБ "{value}"'):
            name = "гб"
            self.find_element_with_swipe(value, name)
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def min(self, value):  #Поиск и выбор Мин
        with allure.step(f'Выбираем МИН "{value}"'):
            name = "мин"
            self.find_element_with_swipe(value, name)
            # делаем скриншот
            screenshot = self.driver.get_screenshot_as_png()
            # добавляем скриншот в Allure
            allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
    def dtm_toggle_click(self, name_dtm):  # Выбор ДТМ опции
        with allure.step(f'Клик по тогглу "{name_dtm}"'):
            attribute = 'clickable'
            attribute_value = 'true'
            self.element_click(name_dtm, attribute, attribute_value)
    def scroll_down_up(self): #Прокрутка экрана вниз
        with allure.step('Скролл страницы вниз'):
            self.scroll_down()
    def dtm_price(self, name, price):  # АП ДТМ опции
        with allure.step(f'Проверяем стоимость "{name}"'):
            text_part = "₽/мес"
            # Получаем строку, содержащую цену
            ap_dtm = self.child_element_ap(name, text_part)
            # Если не удалось найти цену, вернем None
            if not ap_dtm:
                print(f"Не удалось найти стоимость для опции '{name}'.")
                return None
            # Убираем "₽/мес" и пробелы из строки с ценой
            ap = int(ap_dtm.replace(text_part, "").replace(" ", ""))
            # Сравниваем полученную цену с ожидаемой
            try:
                allure.attach(f"Ожидаемая: {price}, Полученная: {ap}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert ap == price, f'Ошибка: неверное значение "{name}", должно: {price}, получено: {ap}.'
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
    def check_button_price(self, price, name):  # Поиск дтм опций в чеке и их стоимость
        with allure.step('Проверяем стоимости на кнопке "Продолжить"'):
            text_part = "₽/мес"
            # Поиск стоимости ДТМ
            ap = self.check_name_price(name, text_part)
            try:
                allure.attach(f"Ожидаемая: {price}, Полученная: {ap}", name="Значения цен", attachment_type=allure.attachment_type.TEXT)
                assert ap == price, f'Ошибка: неверное значение {name},должно:{price}, получено: {ap}'
                # делаем скриншот
                screenshot = self.driver.get_screenshot_as_png()
                # добавляем скриншот в Allure
                allure.attach(screenshot, "screenshot", allure.attachment_type.PNG)
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def button_next_click(self, name):   #Кнопка далее
        #Клик кнопки продолжить
        with allure.step(f'Клик по кнопке "{name}"'):
            self.button_click(name)

#Класс Тариф UP -> Действия с объектами
class TariffUp:
    def __init__(self, driver):
        self.driver = driver
        self.up = TariffUpPage(driver)
#Ожидание страницы тарифа UP
    def wait_page(self, name):
        self.up.wait_page_up(name)
#Выбор ГБ
    def select_gb(self, value_gb):
        self.up.gb(value_gb)
#Выбор МИН
    def select_min(self, value_gb):
        self.up.min(value_gb)
#Скролл вниз
    def scroll_down_up(self):
        self.up.scroll_down_up()
# Выбор ДТМ опции
    def dtm_toggle_click(self, name_dtm):
        self.up.dtm_toggle_click(name_dtm)
# Получение АП за ДТМ опцию
    def dtm_price(self, name, price):
        return self.up.dtm_price(name, price)
#Получение АП за выбранные параметры
    def button_price(self, price, name):
        self.up.check_button_price(price, name)
#Клик по кнопке далее
    def button_next_click(self, name):
        self.up.button_next_click(name)

