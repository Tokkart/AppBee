from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from appium.webdriver.common.appiumby import AppiumBy

class BaseApp:
    """Базовый класс для работы с мобильным приложением."""
    def __init__(self, driver):
        self.driver = driver
    #Поиск элемента
    def find_element(self, locator_type, locator):
        return self.driver.find_element(locator_type, locator)
    # Поиск элементов
    def find_elements(self, locator_type, locator):
        return self.driver.find_elements(locator_type, locator)
    # Поиск элемента с ожиданием
    def wait_for_element(self, locator_type, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((locator_type, locator))
        )
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
            element = self.driver.find_element(*locator)
            element.click()
            print(f"Клик выполнен по элементу: {locator}")
        except NoSuchElementException:
            print(f"Элемент с локатором {locator} не найден")

    # Преобразование координат элемента в строку
    def parse_bounds(self, bounds_str):
        """
        Преобразовать bounds из строки "[x1,y1][x2,y2]" в кортеж координат (x1, y1, x2, y2).
        """
        bounds = bounds_str.strip('[]').split('][')
        x1, y1 = map(int, bounds[0].split(','))
        x2, y2 = map(int, bounds[1].split(','))
        return x1, y1, x2, y2

    # Поиск координат родительских элементов в которые входит начальный элемент
    def is_parent_bounds(self, child_bounds, parent_bounds):
        """
        Проверить, входят ли bounds дочернего элемента в bounds родителя.
        """
        x1d, y1d, x2d, y2d = child_bounds
        x1p, y1p, x2p, y2p = parent_bounds
        return x1d > x1p and y1d > y1p and x2d < x2p and y2d < y2p

    # Расчет площади родительского элемента
    def calculate_area(self, bounds):
        """
        Рассчитать площадь элемента по его bounds.
        """
        x1, y1, x2, y2 = bounds
        return (x2 - x1) * (y2 - y1)

    # Поиск родительского элемента элемента
    def find_parent_element_by_child(self, child_element):
        """
        Найти родительский элемент для заданного дочернего элемента.
        :param driver: Appium WebDriver
        :param child_element: WebElement дочернего элемента
        :return: WebElement родительского элемента или None
        """
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

        return parent_element

    # Поиск дочернего элемента, которого можно включить (тогл)
    def find_toggl_with_conditions(self, parent_element):
        """
        Найти дочерние элементы с clickable='true'.
        :param driver: Appium WebDriver
        :param parent_element: WebElement родительского элемента
        :return: Список WebElement, удовлетворяющих условиям
        """
        parent_bounds_str = parent_element.get_attribute("bounds")
        parent_bounds = self.parse_bounds(parent_bounds_str)

        # Найти все дочерние элементы родителя
        child_elements = parent_element.find_elements(AppiumBy.XPATH, ".//*")

        # Фильтровать дочерние элементы
        filtered_elements = []
        for child in child_elements:
            clickable = child.get_attribute("clickable")
            bounds_str = child.get_attribute("bounds")
            bounds = self.parse_bounds(bounds_str)

            # Условие: текст содержит '₽/мес' и элемент clickable
            if clickable == "true" and self.is_inside_bounds(bounds, parent_bounds):
                filtered_elements.append(child)

        return filtered_elements

    # Поиск дочернего элемента, по координатам
    def is_inside_bounds(self, child_bounds, parent_bounds):
        """
        Проверить, входят ли bounds дочернего элемента в bounds родителя.
        """
        x1d, y1d, x2d, y2d = child_bounds
        x1p, y1p, x2p, y2p = parent_bounds
        return x1d > x1p and y1d > y1p and x2d < x2p and y2d < y2p

    # Поиск дочернего элемента, который отображает АП
    def find_ap_dtm_with_conditions(self, parent_element):
        """
        Найти дочерние элементы с текстом '₽/мес'.
        :param driver: Appium WebDriver
        :param parent_element: WebElement родительского элемента
        :return: Список WebElement, удовлетворяющих условиям
        """
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
            if text and "₽/мес" in text and self.is_inside_bounds(bounds, parent_bounds):
                filtered_elements.append(child)

        return filtered_elements

    def scroll_down(self):
        # Пример реализации прокрутки вниз
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2
        start_y = window_size['height'] * 0.7
        end_y = window_size['height'] * 0.4

        self.driver.swipe(start_x, start_y, start_x, end_y, 800)  # Прокрутка вниз

    def scroll_up(self):
        # Пример реализации прокрутки вверх
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] / 2
        start_y = window_size['height'] * 0.2
        end_y = window_size['height'] * 0.8

        self.driver.swipe(start_x, start_y, start_x, end_y, 800)  # Прокрутка вверх

    def extract_y_from_bounds(self, bounds):
        # Извлекаем координату Y из bounds (например, [x1,y1][x2,y2])
        coordinates = bounds.split("][")
        y1 = int(coordinates[0].split(",")[1].replace("[", ""))
        y2 = int(coordinates[1].split(",")[1].replace("]", ""))
        return (y1 + y2) / 2  # Среднее значение Y для более точного сравнения

    def swipe_right(self, gb_y):
        # Пример свайпа вправо по координатам Y
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.1
        end_x = window_size['width'] * 0.9
        start_y = end_y = gb_y  # Используем координату Y элемента "гб"

        self.driver.swipe(start_x, start_y, end_x, end_y, 800)

    def swipe_left(self, gb_y):
        # Пример свайпа влево по координатам Y
        window_size = self.driver.get_window_size()
        start_x = window_size['width'] * 0.9
        end_x = window_size['width'] * 0.1
        start_y = end_y = gb_y  # Используем координату Y элемента "гб"

        self.driver.swipe(start_x, start_y, end_x, end_y, 800)

    def get_element_by_text(self, text):
        return self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiSelector().text("{text}")'
        )

    def get_element_y_coordinate(self, element):
        bounds = element.get_attribute("bounds")
        return self.extract_y_from_bounds(bounds)

    def find_number_to_click(self, gb_y, value_gb):
        # Находим все элементы с текстом, которые являются числами
        numbers = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.TextView")'
        )

        # Ищем нужное число (например, "100")
        for num in numbers:
            num_text = num.get_attribute("text")
            num_bounds = num.get_attribute("bounds")
            num_y = self.extract_y_from_bounds(num_bounds)

            # Проверяем, находится ли элементы с ГБ на одном уровне по Y
            if gb_y == num_y:
                if num_text == value_gb:
                    print(f"Найден элемент с текстом: {num_text}")
                    return num  # Возвращаем найденный элемент для клика

        return None  # Если число не найдено

    def repeat_search_for_number(self, gb_y, value_gb):
        # Повторный поиск и клик по числовому элементу после свайпа
        number_to_click = self.find_number_to_click(gb_y, value_gb)

        if number_to_click:
            number_to_click.click()
            print("Повторный клик по числу выполнен.")
        else:
            print("Число не найдено после свайпа.")

    def swipe_to_find_number(self, gb_y, value_gb):
        # Находим все элементы с текстом, которые являются числами
        numbers = self.driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().className("android.widget.TextView")'
        )

        # Ищем нужное число (например, "100")
        for num in numbers:
            num_text = num.get_attribute("text")
            num_bounds = num.get_attribute("bounds")
            num_y = self.extract_y_from_bounds(num_bounds)

            # Проверяем, находится ли элементы с ГБ на одном уровне по Y
            if gb_y == num_y:
                if num_text.isdigit():
                    first_visible_number = int(num_text)
                    print(f"Первое найденное число: {first_visible_number}")

                    if first_visible_number < int(value_gb):
                        self.swipe_left(gb_y)
                        print("Свайп влево, так как первое число меньше искомого.")
                    elif first_visible_number > int(value_gb):
                        self.swipe_right(gb_y)
                        print("Свайп вправо, так как первое число больше искомого.")
                    else:
                        print(f"Число {value_gb} найдено, свайп не требуется.")
                        return num  # Возвращаем найденный элемент

                break  # Проверяем только первое найденное число

        return None  # Если число не найдено

    def find_text_with_prefix(self, prefix):
        try:
            # Поиск элемента, текст которого начинается с "При изменении тарифа"
            element = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().textStartsWith("{prefix}")'
            )
            return element
        except Exception as e:
            print(f"Элемент с текстом, начинающимся с '{prefix}', не найден: {e}")
            return None

    def find_text_with_prefixes(self, prefixes):
        for prefix in prefixes:
            try:
                # Поиск элемента, текст которого начинается с текущего префикса
                element = self.driver.find_element(
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    f'new UiSelector().textStartsWith("{prefix}")'
                )
                print(f"Элемент с префиксом '{prefix}' найден.")
                return element
            except Exception as e:
                print(f"Элемент с префиксом '{prefix}' не найден: {e}")
        return None  # Если ни один префикс не подошел