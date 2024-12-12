from selenium.webdriver.common.by import By
from pages.base_app import BaseApp
from appium.webdriver.common.appiumby import AppiumBy

# Тариф UP -> Объекты страницы
class TarifUpPage(BaseApp):

    def gb(self, value_gb):  #Поиск и выбор ГБ
        gb_element = self.get_element_by_text("гб")
        gb_y = self.get_element_y_coordinate(gb_element)

        # Поиск нужного числа и клик по нему
        number_to_click = self.find_number_to_click(gb_y, value_gb)

        # Если число найдено, кликнуть по нему
        if number_to_click:
            number_to_click.click()
            print(f"Кликнуто по элементу {value_gb} ГБ.")
        else:
            # Если нужного числа нет, выполните свайп
            print(f"{value_gb} ГБ не найдены. Выполняется свайп...")
            self.swipe_to_find_number(gb_y, value_gb)
            # Повторяем поиск после свайпа
            self.repeat_search_for_number(gb_y, value_gb)

    def min(self, value_gb):  #Поиск и выбор Мин
        gb_element = self.get_element_by_text("мин")
        gb_y = self.get_element_y_coordinate(gb_element)

        # Поиск нужного числа и клик по нему
        number_to_click = self.find_number_to_click(gb_y, value_gb)

        # Если число найдено, кликнуть по нему
        if number_to_click:
            number_to_click.click()
            print(f"Кликнуто по элементу {value_gb} МИН.")
        else:
            # Если нужного числа нет, выполните свайп
            print(f"{value_gb} МИН не найдены. Выполняется свайп...")
            self.swipe_to_find_number(gb_y, value_gb)
            # Повторяем поиск после свайпа
            self.repeat_search_for_number(gb_y, value_gb)
    def button_next(self):   #Кнопка далее
        #Кнопка далее -> клик

        self.find_element(By.XPATH, '//android.widget.TextView[@text="Продолжить"]').click()
    def button_ap(self):    #АП на кнопке далее
        ap = self.find_element(AppiumBy.ACCESSIBILITY_ID, '\d+ рублей/мес')
        return ap.get_attribute('text')

    def dtm_select(self, name_dtm):  # Выбор ДТМ опции
        try:

            # Найти дочерний элемент через Android UIAutomator
            child_element = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{name_dtm}")'
            )

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
    def dtm_scroll(self): #Прокрутка экрана вниз для проверки ДТМ
        print(f"Выполняется прокрутка вниз...")
        self.scroll_down()
    def dtm_ap(self, name_dtm):  # АП ДТМ опции
        try:

            # Найти дочерний элемент
            child_element = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().text("{name_dtm}")'
            )

            # Найти родительский элемент
            parent_element = self.find_parent_element_by_child(child_element)

            children_with_conditions = self.find_ap_dtm_with_conditions(parent_element)
            for child in children_with_conditions:
                ap_value = child.get_attribute('text')
                print(f"Получено значение АП '{ap_value}' за опцию '{name_dtm}'")
                return ap_value
            # Вернуть экран в исходное положение

        except Exception as e:
            print(f"Ошибка при получении АП за опцию '{name_dtm}': {e}")
            return None



#Класс Тариф UP -> Действия с объектами
class TarifUp:
    def __init__(self, driver):
        self.driver = driver
        self.up = TarifUpPage(driver)
#Выбор ГБ
    def select_gb(self, value_gb):
        self.up.gb(value_gb)
#Выбор МИН
    def select_min(self, value_gb):
        self.up.min(value_gb)
#Клик по кнопке далее
    def select_button_next(self):
        self.up.button_next()
#Получение АП за выбранные параметры
    def button_ap(self):
        self.up.button_ap()
    def dtm_scroll(self):
        self.up.dtm_scroll()
# Выбор ДТМ опции
    def dtm_select(self, name_dtm):
        self.up.dtm_select(name_dtm)
# Получение АП за ДТМ опцию
    def dtm_ap(self, name_dtm):
        return self.up.dtm_ap(name_dtm)