from time import sleep

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import locale
from datetime import datetime, timedelta
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.action_chains import ActionChains
import allure

class BaseApp:
    """Базовый класс для работы с мобильным приложением."""
    def __init__(self, driver):
        self.driver = driver
    #Поиск элемента
    def find_element(self, locator_type, locator):
        try:
            # Попытка найти элемент
            return self.driver.find_element(locator_type, locator)
        except Exception as e:
            # Обработка исключения, если элемент не найден
            print(f"Ошибка: Элемент с локатором ({locator_type}, {locator}) не найден.")
            return None
    # Поиск элементов
    def find_elements(self, locator_type, locator):
        try:
            # Попытка найти элемент
            return self.driver.find_elements(locator_type, locator)
        except Exception as e:
            # Обработка исключения, если элемент не найден
            print(f"find_elements: Элемент с локатором ({locator_type}, {locator}) не найден.")
            return None
    # Поиск элемента с ожиданием
    def wait_for_element(self, locator_type, locator, timeout=15):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator))
            )
        except Exception as e:
            # print(f"Ошибка: Элемент с локатором ({locator_type}, {locator}) не найден.")
            return None
    # Проверка на отображение объекта
    def if_element_exist(self, locator_type, locator, wait_time=5):
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located((locator_type, locator))
            )
            return element  # Возвращаем найденный элемент
        except Exception:
            return None
    # Свайп по координатам
    def swipe(self, start_x, start_y, end_x, end_y):
        actions = ActionChains(self.driver)
        actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
        actions.w3c_actions.pointer_action.release()
        actions.perform()
    # Свайп пока элемент не будет найден
    def swipe_until_element_found(self, start_x, start_y, end_x, end_y, target_locator, max_swipes):
        for i in range(max_swipes):
            try:
                element = self.driver.find_element(*target_locator)
                print(f"Элемент найден после {i + 1} свайпов")
                return element
            except NoSuchElementException:
                print(f"Элемент не найден. Выполняем свайп {i + 1}")
                self.swipe(start_x, start_y, end_x, end_y)
        print("Элемент не найден после максимального количества свайпов")
        return None
    # Клик по элементу
    def click_element(self, locator):
        try:
            element = self.find_element(*locator)
            element.click()
            print(f"Клик выполнен по элементу: {locator}")
        except NoSuchElementException:
            print(f"Элемент с локатором {locator} не найден")
    # Преобразование координат элемента в строку
    @staticmethod
    def parse_bounds(bounds_str):
        """
        Преобразовать bounds из строки "[x1,y1][x2,y2]" в кортеж координат (x1, y1, x2, y2).
        """
        bounds = bounds_str.strip('[]').split('][')
        x1, y1 = map(int, bounds[0].split(','))
        x2, y2 = map(int, bounds[1].split(','))
        return x1, y1, x2, y2

    # Поиск координат родительских элементов в которые входит начальный элемент
    @staticmethod
    def is_parent_bounds(child_bounds, parent_bounds):
        """
        Проверить, входят ли bounds дочернего элемента в bounds родителя.
        """
        x1d, y1d, x2d, y2d = child_bounds
        x1p, y1p, x2p, y2p = parent_bounds
        return x1d > x1p and y1d > y1p and x2d < x2p and y2d < y2p
    # Расчет площади родительского элемента
    @staticmethod
    def calculate_area(bounds):
        x1, y1, x2, y2 = bounds
        return (x2 - x1) * (y2 - y1)
    # Поиск родительского элемента
    def find_parent_element_by_child(self, child_element):
        # Получить bounds дочернего элемента
        child_bounds_str = child_element.get_attribute("bounds")
        child_bounds = self.parse_bounds(child_bounds_str)
        # Найти все элементы с атрибутом bounds
        all_elements = self.find_elements(AppiumBy.XPATH, '//*[@bounds]')
        parent_element = None
        for element in all_elements:
            element_bounds_str = element.get_attribute("bounds")
            element_bounds = self.parse_bounds(element_bounds_str)
            # Проверить, включают ли bounds родителя bounds дочернего
            if self.is_parent_bounds(child_bounds, element_bounds):
                # Если первый подходящий родитель, сохранить
                if parent_element is None:
                    parent_element = element
                else:
                    # Выбираем родителя с минимальной площадью
                    current_area = self.calculate_area(element_bounds)
                    previous_area = self.calculate_area(self.parse_bounds(parent_element.get_attribute("bounds")))
                    if current_area < previous_area:
                        parent_element = element
        print(f'координаты родительского элемента: {parent_element.get_attribute("bounds")}')
        return parent_element
    # Поиск дочернего элемента, по атрибутам
    def find_element_with_attribute(self, parent_element, attribute, attribute_value):
        parent_bounds_str = parent_element.get_attribute("bounds")
        parent_bounds = self.parse_bounds(parent_bounds_str)
        # Найти все дочерние элементы родителя
        child_elements = parent_element.find_elements(AppiumBy.XPATH, ".//*")
        # Фильтровать дочерние элементы
        filtered_elements = []
        for child in child_elements:
            clickable = child.get_attribute(attribute)
            bounds_str = child.get_attribute("bounds")
            bounds = self.parse_bounds(bounds_str)
            # Условие: текст содержит '₽/мес' и элемент clickable
            if clickable == attribute_value and self.is_inside_bounds(bounds, parent_bounds):
                filtered_elements.append(child)
        return filtered_elements
    # Поиск дочернего элемента, по координатам
    @staticmethod
    def is_inside_bounds(child_bounds, parent_bounds):
        """
        Проверить, входят ли bounds дочернего элемента в bounds родителя.
        """
        x1d, y1d, x2d, y2d = child_bounds
        x1p, y1p, x2p, y2p = parent_bounds
        return x1d > x1p and y1d > y1p and x2d < x2p and y2d < y2p
    # Поиск дочернего элемента, который отображает АП
    def find_element_with_conditions(self, parent_element, text_part):
        parent_bounds_str = parent_element.get_attribute("bounds")
        parent_bounds = self.parse_bounds(parent_bounds_str)
        # Найти все дочерние элементы родителя
        child_elements = parent_element.find_elements(AppiumBy.XPATH, ".//*")
        # Фильтровать дочерние элементы
        filtered_elements = []
        for child in child_elements:
            text = child.get_attribute("text")
            bounds_str = child.get_attribute("bounds")
            bounds = self.parse_bounds(bounds_str)
            # Условие: текст содержит '₽/мес'
            if text_part in text and self.is_inside_bounds(bounds, parent_bounds):
                filtered_elements.append(child)
        if filtered_elements:
            return filtered_elements
        else:
            return None
    def scroll_down(self):
        # Пример реализации прокрутки вниз
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2
        start_y = window_size['height'] * 0.8
        end_y = window_size['height'] * 0.2
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)# Прокрутка вниз
        sleep(1)
    def scroll_up(self):
        # Пример реализации прокрутки вниз
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2
        start_y = window_size['height'] * 0.2
        end_y = window_size['height'] * 0.8
        self.driver.swipe(start_x, start_y, start_x, end_y, 800)  # Прокрутка вниз
        sleep(1)
    @staticmethod
    def extract_y_from_bounds(bounds):
        # Извлекаем координату Y из bounds (например, [x1,y1][x2,y2])
        if bounds:
            coordinates = bounds.split("][")
            y1 = int(coordinates[0].split(",")[1].replace("[", ""))
            y2 = int(coordinates[1].split(",")[1].replace("]", ""))
            return (y1 + y2) / 2  # Среднее значение Y для более точного сравнения
        else:
            print('Координаты не переданы')
            return None
    def swipe_right(self, gb_y):
        # Пример свайпа вправо по координатам Y
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.2
        end_x = window_size['width'] * 0.8
        start_y = end_y = gb_y  # Используем координату Y элемента "гб"
        self.driver.swipe(start_x, start_y, end_x, end_y, 800)
        sleep(1)
    def swipe_left(self, gb_y):
        # Пример свайпа влево по координатам Y
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.8
        end_x = window_size['width'] * 0.2
        start_y = end_y = gb_y  # Используем координату Y элемента "гб"
        self.driver.swipe(start_x, start_y, end_x, end_y, 800)
        sleep(1)
    def get_element_by_text(self, text):
        element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")')
        if element:
            print(f'Элемент "{text}" найден.')
            return element
        else:
            print(f'Элемент "{text}" не найден.')
        return None
    def get_element_by_prefixes(self, text):
        try:
            return self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textStartsWith("{text}")')
        except Exception as e:
            print(f'"{text}": не найден')
            return None

    @staticmethod
    def get_element_bounds(element): #Поиск элементов находящихся на одном уровне по оси X
        try:
            bounds = element.get_attribute("bounds")
            print(f'Координаты "{bounds}" найдены')
            return bounds
        except AttributeError:
            print(f'Координаты "{element}" не найдены')
            return None
    def find_number_to_click(self, gb_y, value_gb):
        # Находим все элементы с текстом, которые являются числами
        numbers = self.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{value_gb}")')
        # Ищем нужное число
        for num in numbers:
            num_text = num.text
            num_bounds = num.get_attribute('bounds')
            num_y = self.extract_y_from_bounds(num_bounds)
            # Проверяем, находится ли элементы с ГБ на одном уровне по Y
            if abs(gb_y - num_y) < 40:
                if int(num_text) == value_gb:
                    return num  # Возвращаем найденный элемент для клика
        return None# Если число не найдено
    def find_number(self, element, text_part):
        # Находим все элементы с текстом, которые являются числами
        numbers = self.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{text_part}")')

        # Ищем нужное число (например, "100")
        for num in numbers:
            num_text = num.get_attribute("text")
            num_bounds = self.get_element_bounds(num)
            num_y = self.extract_y_from_bounds(num_bounds)
            element_y = self.extract_y_from_bounds(element)

            # Проверяем, находится ли элементы с ГБ на одном уровне по Y
            if (abs(element_y - num_y) < 40) and text_part in num_text:
               return num  # Возвращаем найденный элемент для клика
        return None  # Если число не найдено
    def find_element_by_y(self, parent, class_name, max_distance, direction):
        """
        Ищет элемент по оси Y рядом с parent элементом.

        Args:
        - parent: Элемент, рядом с которым нужно искать.
        - class_name: Имя класса искомых элементов.
        - max_distance: Максимальное расстояние в пикселях.
        - direction: Направление поиска ('above' для поиска сверху, 'below' для поиска снизу).

        Returns:
        - Найденный элемент или None, если элемент не найден.
        """
        # Находим все элементы с заданным классом
        find_elements = self.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().className("{class_name}")')
        parent_y = self.extract_y_from_bounds(parent)

        for element in find_elements:
            element_bounds = self.get_element_bounds(element)
            element_y = self.extract_y_from_bounds(element_bounds)

            if direction == "above" and 0 < parent_y - element_y <= max_distance:
                print(f'Найден элемент сверху с координатами {element_bounds}')
                return element
            elif direction == "below" and 0 < element_y - parent_y <= max_distance:
                print(f'Найден элемент снизу с координатами {element_bounds}')
                return element

        return None  # Если элемент не найден
    def repeat_search_for_number(self, gb_y, value_gb):
        # Повторный поиск и клик по числовому элементу после свайпа
        number_to_click = self.find_number_to_click(gb_y, value_gb)
        try:
            assert number_to_click, f'Число "{value_gb}" не найдено после свайпа.'
            number_to_click.click()
        except AssertionError as e: # Перехватываем именно AssertionError
            allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
            raise # Важно пробросить исключение дальше
        except Exception as e: # Обрабатываем другие возможные исключения
            allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
            screenshot = self.driver.get_screenshot_as_png()
            allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def swipe_to_find_number(self, number, value_gb):
        # Находим все элементы с текстом, которые являются числами
        numbers = self.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.TextView")'
        )

        # Ищем нужное число (например, "100")
        for num in numbers:
            num_text = num.get_attribute("text")
            num_bounds = num.get_attribute("bounds")
            num_y = self.extract_y_from_bounds(num_bounds)

            # Проверяем, находится ли элементы с ГБ на одном уровне по Y
            if number == num_y:
                if num_text.isdigit():
                    first_visible_number = int(num_text)
                    if first_visible_number < int(value_gb):
                        self.swipe_left(number)
                    elif first_visible_number > int(value_gb):
                        self.swipe_right(number)
                    else:
                        return num  # Возвращаем найденный элемент
                break  # Проверяем только первое найденное число
        return None  # Если число не найдено

    def find_text_with_prefix(self, prefix):
        try:
            # Поиск элемента, текст которого начинается с "При изменении тарифа"
            element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textStartsWith("{prefix}")')
            return element
        except Exception as e:
            print(f"Элемент с текстом, начинающимся с '{prefix}', не найден: {e}")
            return None

    def find_text_with_prefixes(self, prefixes):
        for prefix in prefixes:
            # Поиск элемента с префиксом
            element = self.get_element_by_prefixes(prefix)
            if element is None:
                # Если элемент не найден для текущего префикса
                continue  # Переход к следующему префиксу
            # Возврат найденного элемента
            return element
            # Если ни один элемент не найден, возвращаем None
        print("Элемент с указанными префиксами не найден.")
        return None
    def check_name_price(self, name, text_part):  # Поиск стоимости cправа от нужного элемента
        # Получаем элемент с заданным текстом
        parent = self.get_element_by_text(name)
        if parent is None:
            print(f'Не найден элемент с текстом "{name}"')
            return None
        element = self.get_element_bounds(parent)
        if element is None:
            print(f'Не найдены координаты "{name}"')
            return None
        # Ищем стоимость ДТМ
        price_element = int(self.find_number(element, text_part).text.replace(text_part, "").replace(" ", ""))
        if price_element is None:
            return None
        return price_element
    def find_nearby_element(self, name, class_name, y_coordinate, direction):  # Поиск элемента, который находится радом от заданного, по имени класса и расстоянию
        # Получаем элемент с заданным текстом
        parent = self.get_element_by_text(name)
        if parent is None:
            return None
        element = self.get_element_bounds(parent)
        if element is None:
            print(f'Не найдены координаты "{name}"')
            return None
        # Ищем элемент с заданным классом
        nearby_element = self.find_element_by_y(element, class_name, y_coordinate, direction)
        if nearby_element is None:
            return None
        return nearby_element

    def check_info_click(self):
        info_button = self.find_element(AppiumBy.ACCESSIBILITY_ID, 'info')
        if info_button:
            info_button.click()
        else:
            print('Иконка "info" не найдена')

    def button_understand_click(self):
        try:
            understand_button = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("понятно")')
            understand_button.click()
            print('Клик по кнопке с текстом "понятно"')
        except NoSuchElementException:
            print('Ошибка: Кнопка с текстом "Понятно" не найдена.')
            # Логика обработки отсутствия элемента:
            # Например, сделать скриншот или завершить текущий шаг
            self.driver.save_screenshot("element_not_found.png")

    def button_click(self, name):   #Клик по кнопке оплатить
       with allure.step(f'Клик по кнопке "{name}"'):
            try:
                button = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().text("{name}")')
                assert button, f'Ошибка: кнопка "{name}" не найдена'
                button.click()
            except AssertionError as e: # Перехватываем именно AssertionError
                allure.attach(str(e), name="Ошибка сравнения цен", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                raise # Важно пробросить исключение дальше
            except Exception as e: # Обрабатываем другие возможные исключения
                allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                screenshot = self.driver.get_screenshot_as_png()
                allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def find_text_part_element(self, text_part): #Поиск значения нужного элемента
        price = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR,f'new UiSelector().textContains("{text_part}")')
        if price:
            return price.text.replace(text_part, '').replace(' ', '')
        else:
            return None
    @staticmethod
    def data_through_30d():  # Дата следующего списания через 30д
        # Устанавливаем локализацию на русский
        locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
        # Текущая дата плюс 30 дней
        future_date = datetime.now() + timedelta(days=30)
        # Словарь склонений месяцев
        months_genitive = {
            "январь": "января",
            "февраль": "февраля",
            "март": "марта",
            "апрель": "апреля",
            "май": "мая",
            "июнь": "июня",
            "июль": "июля",
            "август": "августа",
            "сентябрь": "сентября",
            "октябрь": "октября",
            "ноябрь": "ноября",
            "декабрь": "декабря",
        }
        # Получение названия месяца в именительном падеже
        month_nominative = future_date.strftime("%B").lower()
        # Замена на форму в родительном падеже
        month_genitive = months_genitive[month_nominative]
        # Форматирование итоговой строки
        data_future_30d = f"{str(future_date.strftime('%#d'))} {month_genitive}"
        return data_future_30d
    def find_element_with_swipe(self, value, name):  #Поиск и выбор элемента при помощи свайпа в карусели (ГБ/МИН)
        gb_element = self.get_element_by_text(name)
        gb_bounds = self.get_element_bounds(gb_element)
        gb_y = self.extract_y_from_bounds(gb_bounds)

        # Поиск нужного числа и клик по нему
        number_to_click = self.find_number_to_click(gb_y, value)

        # Если число найдено, кликнуть по нему
        if number_to_click:
            number_to_click.click()
            print(f"Кликнуто по элементу {value} {name}.")
        else:
            # Если нужного числа нет, выполните свайп
            self.swipe_to_find_number(gb_y, value)
            # Поиск нужного числа и клик по нему
            number_to_click = self.find_number_to_click(gb_y, value)
            if number_to_click:
                number_to_click.click()
                print(f"Кликнуто по элементу {value} {name}.")
            else:
            # Если нужного числа нет, выполните свайп
                self.swipe_to_find_number(gb_y, value)
            # Повторяем поиск после свайпа
                self.repeat_search_for_number(gb_y, value)
    def child_element_ap(self, name, text_part):  # АП ДТМ опции
        # Найти дочерний элемент
        child_element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')

        # Найти родительский элемент
        parent_element = self.find_parent_element_by_child(child_element)
        children_with_conditions = self.find_element_with_conditions(parent_element, text_part)
        for child in children_with_conditions:
            if child:
                return child.text
            else:
                return None
    def element_click(self, name, attribute, attribute_value):  # Выбор ДТМ опции
        # Найти дочерний элемент через Android UIAutomator
        child_element = self.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')
        if child_element is None:
            print(f"Не найден child_element '{name}'")
            return None
        # Найти родительский элемент
        parent_element = self.find_parent_element_by_child(child_element)
        if parent_element is None:
            print(f"Не найден parent_element '{name}'")
            return None
        # Кликнуть только по первому элементу
        children_with_conditions = self.find_element_with_attribute(parent_element, attribute, attribute_value)
        if children_with_conditions is None:
            print(f"Не найдены children_with_conditions '{name}'")
            return None
        for child in children_with_conditions:
            with allure.step(f'Клик по кнопке "{name}"'):
                try:
                    assert child, f'Ошибка: элемент от "{name}" не найден'
                    child.click()
                except AssertionError as e: # Перехватываем именно AssertionError
                    allure.attach(str(e), name="Ошибка поиска элемента", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
                    raise # Важно пробросить исключение дальше
                except Exception as e: # Обрабатываем другие возможные исключения
                    allure.attach(str(e), name="Непредвиденная ошибка", attachment_type=allure.attachment_type.TEXT)
                    screenshot = self.driver.get_screenshot_as_png()
                    allure.attach(screenshot, name="Скриншот", attachment_type=allure.attachment_type.PNG)
    def generate_changing_tariff_text(self, value_gb, value_gb_old, value_min, value_min_old, delta, price, price_dtm): #Генерация текста изменения тарифа конструктора
        data = self.data_through_30d() #получаем дату через 30 дней
        #Текст про изменение пакетов
        first_parts = []
        #Если один из пакетов увеличивается
        increase_parts = []
        if value_gb > value_gb_old or value_min > value_min_old:
            if value_gb > value_gb_old:
                increase_parts.append(f'{value_gb} ГБ')
            if value_min > value_min_old:
                increase_parts.append(f'{value_min} минут')
            increase_text = f'Сейчас увеличим ваш пакет до {" и ".join(increase_parts)}. Однократная доплата составит {delta} ₽.'
            first_parts.append(increase_text)
        #Если один из пакетов уменьшается
        decrease_parts = []
        if value_gb < value_gb_old or value_min < value_min_old:
            if value_gb < value_gb_old:
                decrease_parts.append('ГБ')
            if value_min < value_min_old:
                decrease_parts.append('минут')
            leftover_text = f'Остаток текущего пакета {" и ".join(decrease_parts)} будет доступен до {data}.'
            first_parts.append(leftover_text)
        first_text = f'{" ".join(first_parts)}'
        #Текс с датой следующего обновления пакетов
        next_parts = []
        if value_gb != 0 or value_min != 0:
            if value_gb != 0:
                next_parts.append(f'{value_gb} ГБ')
            if value_min != 0:
                next_parts.append(f'{value_min} минут')
            next_text = f'\r\nС {data} будут предоставлены новые {" и ".join(next_parts)}. '
        elif value_gb == 0 and value_min == 0 and price_dtm == 0:
            next_text = f' С {data} доступ в интернет будет ограничен. Звонки будут оплачиваться поминутно.'
        else:
            next_text = ''
        #Текст про оплату
        if value_gb != 0 or value_min != 0:
            if value_gb != 0 and value_min == 0:
                last_text = f'Стоимость тарифа составит {price} ₽/мес. Звонки будут оплачиваться поминутно.'
            elif value_gb == 0 and value_min != 0:
                last_text = f'Стоимость тарифа составит {price} ₽/мес. Доступ в интернет будет ограничен.'
            else:
                last_text = f'Стоимость тарифа составит {price} ₽/мес.'
        elif value_gb == 0 and value_min == 0 and price_dtm != 0:
            last_text = f'\r\nСтоимость тарифа составит {price} ₽/мес. С {data} доступ в интернет будет ограничен. Звонки будут оплачиваться поминутно.'
        else:
            last_text = ''
        name = f'{first_text}{next_text}{last_text}' #склейка всех частей в одну строку
        return name
    def generate_check_text(self, value_gb, value_gb_old, value_min, value_min_old): #Генерация текста изменения тарифа конструктора
        data = self.data_through_30d() #получаем дату через 30 дней
        #Текст про изменение пакетов
        text_parts = []
        if value_gb > value_gb_old or value_min > value_min_old:
            if value_gb > value_gb_old:
                text_parts.append('ГБ')
            if value_min > value_min_old:
                text_parts.append('минут')
            check_text = f'Увеличение пакета {" и ".join(text_parts)}'
        elif value_gb <= value_gb_old and value_min <= value_min_old:
            check_text = f'Новые условия с {data} —\r\n{value_gb} ГБ и {value_min} минут'
        return check_text
    def wait_page(self, name):
        max_attempts = 5
        attempt = 0
        error_found = True
        while attempt < max_attempts and error_found:
            try:
                # Попытка проверить страницу чека
                page = self.wait_for_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{name}")')
                error_found = False  # Если страница загружена, выходим из цикла
                if page:
                    return page
            except WebDriverException:
                attempt += 1
                print(f"Попытка обновления: {attempt}")
                # Нажатие на кнопку обновить
                try:
                    button = 'Обновить'
                    self.button_click(button)
                except WebDriverException:
                    pytest.fail("Кнопка обновления недоступна.")
        if error_found:
            pytest.fail("Ошибка: при загрузке  страницы.")