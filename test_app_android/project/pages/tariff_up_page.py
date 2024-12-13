# from dataclasses import replace
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from beeline.AppBee.AppBee.test_app_android.project.pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy

# Тариф UP -> Объекты страницы
class TariffUpPage(BaseApp):
    def wait_tariff_up_page(self, name):
        tariff_up = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name.lower()}")')
        if tariff_up:
            print(f'Страница с тарифом "{name}" найдена.')
        else:
            print(f'"{name}" страница не найдена.')
    def gb(self, value):  #Поиск и выбор ГБ
        name = "гб"
        self.find_element_with_swipe(value, name)
    def min(self, value):  #Поиск и выбор Мин
        name = "мин"
        self.find_element_with_swipe(value, name)
    def dtm_select(self, name_dtm):  # Выбор ДТМ опции
        try:

            # Найти дочерний элемент через Android UIAutomator
            child_element = self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name_dtm}")')
            # Найти родительский элемент
            parent_element = self.find_parent_element_by_child(child_element)
            #Проверка сколько находит элементов -> нужна для отладки
            # if len(children_with_conditions) > 1:
            #     print(
            #         f"Предупреждение: Найдено несколько элементов для опции '{name_dtm}': {len(children_with_conditions)}")
            # Кликнуть только по первому элементу
            children_with_conditions = self.find_toggl_with_conditions(parent_element)
            for child in children_with_conditions:
                child.click()
            print(f"Кликнуто по опции '{name_dtm}'")
        except Exception as e:
            print(f"Ошибка при выборе опции '{name_dtm}': {e}")
    def scroll_down_up(self): #Прокрутка экрана вниз
        print(f"Выполняется прокрутка вниз...")
        self.scroll_down()
    def dtm_ap(self, name, price):  # АП ДТМ опции
        text_part = "₽/мес"
        # Получаем строку, содержащую цену
        ap_dtm = self.child_element_ap(name, text_part)
        # Если не удалось найти цену, вернем None
        if not ap_dtm:
            print(f"Не удалось найти стоимость для опции '{name}'.")
            return None
        # Убираем "₽/мес" и пробелы из строки с ценой
        ap = ap_dtm.replace(text_part, "").replace(" ", "")
        # Сравниваем полученную цену с ожидаемой
        if ap == price:
            print(f'Получено значение АП "{ap_dtm}" за опцию "{name}".')
        else:
            print(f'Получено значение АП "{ap_dtm}" за опцию "{name}", но ожидаемая цена {price}.')
        # Возвращаем строку с ценой
        return ap_dtm
    def button_next(self):   #Кнопка далее
        #Кнопка далее -> клик
        self.find_element(By.XPATH, '//android.widget.TextView[@text="Продолжить"]').click()

    def check_button_price(self, price):  # Поиск дтм опций в чеке и их стоимость
        name = "Продолжить"
        text_part = "₽/мес"
        # Поиск стоимости ДТМ
        self.check_name_price(name, price, text_part)



#Класс Тариф UP -> Действия с объектами
class TariffUp:
    def __init__(self, driver):
        self.driver = driver
        self.up = TariffUpPage(driver)
#Ожидание страницы тарифа UP
    def wait_tariff_up_page(self, name):
        self.up.wait_tariff_up_page(name)
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
    def dtm_select(self, name_dtm):
        self.up.dtm_select(name_dtm)
# Получение АП за ДТМ опцию
    def dtm_ap(self, name, price):
        return self.up.dtm_ap(name, price)
#Получение АП за выбранные параметры
    def button_price(self, price):
        self.up.check_button_price(price)
#Клик по кнопке далее
    def select_button_next(self):
        self.up.button_next()

