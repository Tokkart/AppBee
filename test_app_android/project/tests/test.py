import allure
import pandas as pd

from test_app_android.project.tests.conftest import app_pages


@allure.feature("Тестирование тарифа UP")
class TestChangePlan:
    def __init__(self, data, app_pages):

        self.data = data
        self.app_pages = app_pages
        #Переменные из файла
        #Тариф
        self.name_tp = str(data.get('new_tariff_name')) # Название тарифа
        self.value_gb = int(data.get('new_gb_value')) # Подключаемый пакет ГБ
        self.value_min = int(data.get('new_min_value')) # Подключаемый пакет Мин
        self.price_tp = int(data.get('new_tariff_price')) # Стоимость за мобильную связь
        self.price_tp_day = data.get('new_tariff_price_day')
        if self.price_tp_day.is_integer():
            self.price_tp_day = int(self.price_tp_day)
        else:
            self.price_tp_day = str(data.get('new_tariff_price_day')).replace(",", ".")
            self.price_tp_day = float(self.price_tp_day) #  Стоимость за день

        #ДТМ опция
        if not pd.isna(data.get('new_options_name')):
            self.name_dtm = str(data.get('new_options_name'))  # ДТМ опция
        if not pd.isna(data.get('new_options_price')):
            self.price_dtm = int(data.get('new_options_price'))
        else:
            self.price_dtm = 0  # Цена ДТМ опции
            self.price_dtm_day = 0
        if not pd.isna(data.get('new_options_price_day')):
            self.price_dtm_day = data.get('new_options_price_day')
            if self.price_dtm_day.is_integer():
                self.price_dtm_day = int(self.price_dtm_day)
            else:
                self.price_dtm_day = str(self.price_dtm_day).replace(",", ".")
                self.price_dtm_day = float(self.price_dtm_day)
        if not pd.isna(data.get('old_options_name')):
            self.name_dtm_old = str(data.get('old_options_name')) #Старая дтп опция

        #Данные старого тарифа
        # Стоимость тарифа
        old_tariff_price = data.get('old_tariff_price')
        if pd.isna(old_tariff_price):
            self.price_tp_old = 0
        else:
            self.price_tp_old = int(old_tariff_price)
        # Начисленные ГБ
        old_gb_value = data.get('old_gb_value')
        if pd.isna(old_gb_value):
            self.value_gb_old = 0
        else:
            self.value_gb_old = int(old_gb_value)
        # Начисленные Мин
        old_min_value = data.get('old_min_value')
        if pd.isna(old_min_value):
            self.value_min_old = 0
        else:
            self.value_min_old = int(old_min_value)

        #Итоговая данные тарифа
        self.price_total = self.price_tp + self.price_dtm #общая цена тп + дтм опция
        if self.value_gb < self.value_gb_old:
            self.value_gb_total = self.value_gb_old
        else:
            self.value_gb_total = self.value_gb
        if self.value_min < self.value_min_old:
            self.value_min_total = self.value_min_old
        else:
            self.value_min_total = self.value_min

        #Цикл списания
        if data.get('cycle') == 'month':
            self.cycle = 'm'
        else:
            self.cycle = 'd'

        #Тип тест-кейса
        if data.get('old_tariff_soc') != data.get('new_tariff_soc'):
            self.type_case = 'tariff'
            print(f'тип тест-кейса: {self.type_case}')
        elif (data.get('old_tariff_soc') == data.get('new_tariff_soc')) and (data.get('old_gb_value') != data.get('new_gb_value') or data.get('old_min_value') != data.get('new_min_value')):
            self.type_case = 'preset'
            print(f'тип тест-кейса: {self.type_case}')
        else:
            self.type_case = 'options'
            print(f'тип тест-кейса: {self.type_case}')
    def test_go_my_product(self, app_pages):
        #Стартовая страница -> переход в мои продукты
        self.app_pages.main.go_my_product()
    def test_go_settings_tariff(self, app_pages):
        # Мои продукты -> переход в настройки тарифа
        self.app_pages.my_products.settings_click()
    def test_go_new_tariff(self, app_pages):
        # Мои продукты -> переход на страницу смены тариф
        self.app_pages.my_products.change_tariff_click()
    def test_select_tariff(self, app_pages):
        # Выбор тарифа
        self.app_pages.list.go_tariff(self.name_tp)
    #Ожидание загрузки конструктора тарифа UP
    def test_wait_tariff_up(self, app_pages):
        self.app_pages.tariff_up.wait_page(self.name_tp)
    def test_select_data(self, app_pages):
        # Выбор ГБ
        self.app_pages.tariff_up.select_gb(self.value_gb)

    def test_select_voice(self, app_pages):
        # выбор МИН
        self.app_pages.tariff_up.select_min(self.value_min)

    def test_select_dtm(self, app_pages, status):
        # Скролл вниз
        self.app_pages.tariff_up.scroll_down_up()
        if status == 'on':
            # Поиск клик по тоглу дтм опции
            self.app_pages.tariff_up.dtm_toggle_click(self.name_dtm)
            # Проверка АП дтм опции
            try:
                self.app_pages.tariff_up.dtm_price(self.name_dtm, self.price_dtm)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        elif status == 'off':
            # Поиск клик по тоглу дтм опции
            self.app_pages.tariff_up.dtm_toggle_click(self.name_dtm_old)

    def test_dtm_price(self, app_pages):
        # Скролл вниз
        self.app_pages.tariff_up.scroll_down_up()
        # Проверка АП дтм опции
        try:
            self.app_pages.tariff_up.dtm_price(self.name_dtm, self.price_dtm)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_tariff_price(self, app_pages, name):#Проверка общей АП ТП + ДТМ
        try:
            self.app_pages.tariff_up.button_price(self.price_total, name)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        # Клик далее
        self.app_pages.tariff_up.button_next_click(name)
    # Проверка предчека
    def test_precheck(self, app_pages, old_dtm_name, changing_tariff):
        self.app_pages.precheck.wait_page_precheck()# Ожидание предчека
        if old_dtm_name is not None:#Проверка отключаемой опции в предчеке
            try:
                self.app_pages.precheck.dtm_delete(self.name_dtm_old)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        if changing_tariff is not None: #Проверка изменения ТП в предчеке
            try:
                self.app_pages.precheck.changing_tariff(self.value_gb, self.value_min, self.price_tp, self.value_gb_old, self.value_min_old, self.price_tp_old,  self.price_dtm, self.cycle)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        self.app_pages.precheck.button_next()

    def test_check_text(self, app_pages, text_part):
        self.app_pages.check.wait_check_page(self.name_tp)
        try:
            self.app_pages.check.mobil_text(self.value_gb, self.value_gb_old, self.value_min, self.value_min_old, text_part, self.cycle)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    def test_check_mobile_price(self, app_pages, text_part):
        self.app_pages.check.wait_check_page(self.name_tp)
        try:
            self.app_pages.check.mobil_price(self.price_tp, self.price_tp_old, self.value_gb, self.value_gb_old, self.value_min, self.value_min_old, text_part, self.cycle)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_check_dtm(self, app_pages, price, text_part):
        if self.cycle == 'd' and self.type_case == 'options':
           if isinstance(self.price_dtm_day, float):
                self.price_dtm = "{:.2f}".format(self.price_dtm_day)
                self.price_dtm = float(self.price_dtm)
           else:
               self.price_dtm = float(self.price_dtm_day)
        self.app_pages.check.wait_check_page(self.name_tp)
        try:
            if price is not None:
                self.app_pages.check.dtm_price(self.name_dtm, self.price_dtm, text_part)
            else:
                self.app_pages.check.dtm_name(self.name_dtm_old)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    def test_single_payment(self, app_pages):
        try:
            self.app_pages.check.single_payment()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_check_info(self, app_pages):
        if self.cycle == 'd' and self.type_case == 'options':
            self.price_dtm = self.price_dtm_day
        try:
            self.app_pages.check.info_text(self.value_gb, self.value_min, self.price_tp, self.value_gb_old, self.value_min_old, self.price_tp_old,  self.price_dtm, self.cycle)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        self.app_pages.check.button_understand_click()
    def test_check_price(self, app_pages):
        payment = 0
        if self.type_case == 'options':
            self.price_tp = 0
            if self.cycle == 'd':
                self.price_dtm = float("{:.2f}".format(self.price_dtm_day)) if isinstance(self.price_dtm_day, float) else self.price_dtm_day
        elif self.type_case == 'preset':
            if self.cycle == 'm':
                self.price_tp = max(0, self.price_tp - self.price_tp_old)
                if self.price_tp == 0 and (self.value_gb > self.value_gb_old or self.value_min > self.value_min_old):
                    self.price_tp = 30
                if not pd.isna(self.data.get('old_options_price')) and not pd.isna(self.data.get('new_options_price')):
                    self.price_dtm = 0
        elif self.type_case == 'tariff':
            payment = 200
        try:
            self.app_pages.check.button_price(self.price_tp + payment + self.price_dtm)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    #Клик по кнопке оплаты
    def test_button_pay_click(self, app_pages):
        self.app_pages.check.button_pay_click()
    #Клик по кнопке Сохранить
    def test_button_save_click(self, app_pages):
        self.app_pages.check.button_save_click()
    # Проверка страницы успеха
    def test_success_page(self, app_pages):
        try:
            self.app_pages.status.success_text()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    #Проверка страницы недостаточности средств
    def test_low_balance_page(self, app_pages):
        #Проверка текста недостаточности средств
        self.app_pages.status.low_balance_text()
        #Проверка перехода на страницу пополнения баланса
        self.app_pages.status.pay_balance()
    # Клик по кнопке Понятно
    def test_status_button_understand_click(self, app_pages):
        self.app_pages.status.button_understand_click()
    #Переход на главную страницу
    def test_go_main(self, app_pages):
        self.app_pages.my_products.go_main()
    #Ожидание изменения тарифа
    def test_wait_tariff(self, app_pages):
        text = ""
        if not pd.isna(self.data.get('new_options_name')) and pd.isna(self.data.get('old_options_name')) and self.data.get('new_options_price') == '100 SMS':
            text = '100 смс из 100 доп'
        elif (self.value_gb >0 or self.value_gb_total > 0) and (self.type_case != 'options') and (self.value_gb != self.value_gb_old) and (self.value_gb != self.value_min):
            text = f'из {self.value_gb}'
        elif (self.value_min >0 or self.value_min_total > 0) and (self.type_case != 'options') and (self.value_min != self.value_min_old) and (self.value_gb != self.value_min):
            number = self.value_min
            text = f'из {self.value_min}'
        elif (self.price_total > 0 and self.cycle == 'm') or self.cycle == 'd':
            if self.cycle == 'd' and self.type_case == 'options':
                number = self.price_tp_day + self.price_dtm_day
                number = f"{number:.2f}".replace('.', ',')
                text = f"{number} ₽/сут"
            else:
                text = f'{self.price_total} ₽/мес'
        else:
            text = self.data.get('new_tariff_name')
        self.app_pages.my_products.wait_changes_tariff(text)
    # Проверка АП тарифа после смены
    def test_ap_tariff(self, app_pages):
        if (self.price_total > 0 and self.cycle == 'm') or self.cycle == 'd':
            if self.cycle == 'd' and self.type_case == 'options':
                price = self.price_tp_day + self.price_dtm_day
                if not price.is_integer():
                    price = f"{price:.2f}"
                    price = float(price)
                print(f'price: {self.price_tp_day}')
                print(f'price: {self.price_dtm_day}')
                print(f'price: {price}')
            else:
                price = self.price_total
            try:
                self.app_pages.my_products.ap(price, self.cycle)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка ГБ тарифа на главном экране
    def test_gb_tariff(self, app_pages):
         if (self.value_gb >0 or self.value_gb_total > 0) and self.type_case != 'options':
            try:
                self.app_pages.my_products.gb(self.value_gb_total, self.value_gb)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка МИН на главном экране
    def test_min_tariff(self, app_pages):
        if (self.value_min >0 or self.value_min_total > 0) and self.type_case != 'options':
            try:
                self.app_pages.my_products.min(self.value_min_total, self.value_min)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка пакета смс на главном экране
    def test_sms_tariff(self, app_pages):
         if not pd.isna(self.data.get('new_options_name')) and self.name_dtm == '100 SMS':
            try:
                self.app_pages.my_products.sms()
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка названия тарифа на главном экране
    def test_name_tariff(self, app_pages):
        try:
            self.app_pages.my_products.name(self.name_tp)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка Даты списания следующего списания АП на главном экране
    def test_date_tariff(self, app_pages):
        try:
            self.app_pages.my_products.data()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)



@allure.feature("Тестирование тарифа UP")
def test_smena_pr(driver, file_data, app_pages):
    #:param row_indices: Индекс строки для запуска (начиная с 0).
    row_indices = [0]
    # row_indices=None запускаются все строки
    # row_indices=[0] запуск одной строки, 0 эта первая строка теста
    # row_indices=[1, 2] запуск нескольких строк
    # row_indices=range(1, 4) запускается диапазон строк
    """
    Тестирование тарифа UP
    """
    if row_indices is not None:
        # Запускаем только указанные строки по индексам
        for index in row_indices:
            process_tariff_changes(driver, file_data[index], app_pages)
    else:
        # Запускаем все строки
        for row in file_data:
            process_tariff_changes(driver, row, app_pages)


def process_tariff_changes(driver, row, app_pages):

    test_plan = TestChangePlan(row, app_pages)
    # Проверка смены тарифного плана (ТП)
    if row['old_tariff_soc'] != row['new_tariff_soc']:
        with allure.step(f'Тест-кейс: смена тарифа "{row['new_tariff_name']}"'):
            if row['balance'] <= 200:
                allure.step(f'Кейс: смена тарифа при недостаточности средств')
            else:
                allure.step(f'Кейс: смена тарифа при параметрах: дефолт ({row["default"]})", ГБ ({row["new_gb_value"]}), Минуты ({row["new_min_value"]}), АП ({row["new_tariff_price"]}), ДТМ ({row["new_options_name"]} ,{row["new_options_price"]})')
            #Переход на страницу мои продукты
            test_plan.test_go_my_product(app_pages)
            #Переход на страницу смены тарифа
            test_plan.test_go_new_tariff(app_pages)
            #Выбираем тариф
            test_plan.test_select_tariff(app_pages)
            #Ожидание страницы конструктора UP
            test_plan.test_wait_tariff_up(app_pages)
            #Выбираем гб и минуты, если пресеты не дефолтные
            if row['default'] == 'no':
                test_plan.test_select_data(app_pages)
                test_plan.test_select_voice(app_pages)
            #Проверка ДТМ (цена/подключение опции)
            if not pd.isna(row['new_options_price']):
                if row['new_options_price'] > 0:
                    test_plan.test_select_dtm(app_pages, status = "on")
                else:
                    test_plan.test_dtm_price(app_pages)
            #Проверка итоговой цены за тариф и переход далее
            if row['old_tariff_soc'] == row['new_tariff_soc']:
                test_plan.test_tariff_price(app_pages, name = 'Продолжить')
            else:
                test_plan.test_tariff_price(app_pages, name = 'подключить')
            #Проверка предчека и переход далее
            if not pd.isna(row['old_options_name']):
                test_plan.test_precheck(app_pages, old_dtm_name = 1, changing_tariff = None)
            #Проверка чека
            #Проверка в чеке описания изменений тарифа (Текс/цена)
            test_plan.test_check_mobile_price(app_pages, text_part = '₽/мес')
            #Проверка дтм опции в чеке (Имя/цена)
            if not pd.isna(row['new_options_price']):
                test_plan.test_check_dtm(app_pages, price = 1, text_part = '₽/мес')
            #Проверка разового платежа за смену тарифа
            test_plan.test_single_payment(app_pages)
            #Проверка цены на кнопке оплатить и переход далее
            test_plan.test_check_price(app_pages)
            test_plan.test_button_pay_click(app_pages)
            if row['balance'] <= 200:
                #Проверка при недостаточности средств
                test_plan.test_low_balance_page(app_pages)
            else:
                #Проверка экрана успеха и переход далее (возврат на главный экран)
                test_plan.test_success_page(app_pages)
                test_plan.test_status_button_understand_click(app_pages)
                #Переход на главный экран
                test_plan.test_go_main(app_pages)
                #Ожидание изменения тарифа на странице мои продукты
                test_plan.test_wait_tariff(app_pages)
                #Проверка данных тарифа поле подключения
                test_plan.test_ap_tariff(app_pages)
                test_plan.test_gb_tariff(app_pages)
                test_plan.test_min_tariff(app_pages)
                test_plan.test_name_tariff(app_pages)
                test_plan.test_date_tariff(app_pages)

    # Проверка смены пресета/ подключение услуг
    elif row['old_tariff_soc'] == row['new_tariff_soc']:
        if (row['old_gb_value'] != row['new_gb_value']) or (row['old_min_value'] != row['new_min_value']):
            with allure.step(f'Тест-кейс: смена пресета "{row['new_tariff_name']}"'):
                #Переход на страницу мои продукты
                test_plan.test_go_my_product(app_pages)
                #Переходим в карточку тарифа
                test_plan.test_go_settings_tariff(app_pages)
                # Ожидание страницы конструктора UP
                test_plan.test_wait_tariff_up(app_pages)
                #Подключаем ГБ и МИН если необходимо
                if row['old_gb_value'] != row['new_gb_value']:
                    test_plan.test_select_data(app_pages)
                if row['old_min_value'] != row['new_min_value']:
                    test_plan.test_select_voice(app_pages)
                #Проверка ДТМ (цена/подключение опции)
                if not pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    if row['new_options_price'] != row['old_options_price'] and row['new_options_price'] > 0:
                        test_plan.test_select_dtm(app_pages, status = "on")
                    else:
                        test_plan.test_dtm_price(app_pages)
                elif pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    if row['new_options_price'] > 0:
                        test_plan.test_select_dtm(app_pages, status = "on")
                    else:
                        test_plan.test_dtm_price(app_pages)
                elif not pd.isna(row['old_options_price']) and pd.isna(row['new_options_price']) and (row['old_gb_value'] == row['new_gb_value']):
                    test_plan.test_select_dtm(app_pages, status = "off")
                #Проверка итоговой цены за тариф и переход далее
                if row['old_tariff_soc'] == row['new_tariff_soc']:
                    test_plan.test_tariff_price(app_pages, name = 'Продолжить')
                else:
                    test_plan.test_tariff_price(app_pages, name = 'подключить')
                #Проверка предчека и переход далее
                if (not pd.isna(row['old_options_name']) and pd.isna(row['new_options_name'])) and (row['old_gb_value'] != row['new_gb_value']):
                    test_plan.test_precheck(app_pages, old_dtm_name = 1, changing_tariff = 1)
                else:
                    test_plan.test_precheck(app_pages, old_dtm_name = None, changing_tariff = 1)
                #Проверка описания изменений тарифа (Текс/цена)
                if (row['new_gb_value'] <= row['old_gb_value']) and (row['new_min_value'] <= row['old_min_value']):
                    test_plan.test_check_text(app_pages, text_part = '₽')
                else:
                    test_plan.test_check_mobile_price(app_pages, text_part = '₽')
                #Проверка дтм опции в чеке (Имя/цена)
                if not pd.isna(row['old_options_price']) and pd.isna(row['new_options_price']) and (row['old_gb_value'] == row['new_gb_value']):
                    test_plan.test_check_dtm(app_pages, price = None, text_part = '₽')
                elif pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    test_plan.test_check_dtm(app_pages, price = 1, text_part = '₽')
                test_plan.test_check_info(app_pages)
                #Проверка цены на кнопке оплатить и переход далее
                if (row['new_gb_value'] <= row['old_gb_value'] and row['new_min_value'] <= row['old_min_value']) and (pd.isna(row['new_options_price']) or (not pd.isna(row['new_options_price']) and not pd.isna(row['old_options_price'])) or (not pd.isna(row['new_options_price']) and row['new_options_price'] == 0)):
                    test_plan.test_button_save_click(app_pages)
                else:
                    type_case = 'preset'
                    test_plan.test_check_price(type_case)
                    test_plan.test_button_pay_click(app_pages)
                #Проверка экрана успеха и переход далее (возврат на главный экран)
                test_plan.test_success_page(app_pages)
                test_plan.test_status_button_understand_click(app_pages)
                #Переход на главный экран
                test_plan.test_go_main(app_pages)
                # Ожидание изменения тарифа на странице мои продукты
                test_plan.test_wait_tariff(app_pages)
                #Проверка данных тарифа поле подключения
                test_plan.test_ap_tariff(app_pages)
                test_plan.test_gb_tariff(app_pages)
                test_plan.test_min_tariff(app_pages)
                test_plan.test_name_tariff(app_pages)
                test_plan.test_date_tariff(app_pages)
        else:
            if not pd.isna(row['new_options_name']):
                text_case = f'Тест-кейс: подключение услуги "{row['new_options_name']}"'
            else:
                text_case = f'Тест-кейс: отключение услуги "{row["old_options_name"]}"'
            with allure.step(text_case):
                #Переход на страницу мои продукты
                test_plan.test_go_my_product(app_pages)
                #Переходим в карточку тарифа
                test_plan.test_go_settings_tariff(app_pages)
                # Ожидание страницы конструктора UP
                test_plan.test_wait_tariff_up(app_pages)
                #Проверка ДТМ (цена/подключение опции)
                if not pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    if row['new_options_price'] > row['old_options_price']:
                        test_plan.test_select_dtm(app_pages, status = "on")
                    else:
                        test_plan.test_dtm_price(app_pages)
                elif pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    if row['new_options_price'] > 0:
                        test_plan.test_select_dtm(app_pages, status = "on")
                    else:
                        test_plan.test_dtm_price(app_pages)
                elif not pd.isna(row['old_options_price']) and pd.isna(row['new_options_price']):
                    test_plan.test_select_dtm(app_pages, status = "off")
                #Проверка итоговой цены за тариф и переход далее
                if row['old_tariff_soc'] == row['new_tariff_soc']:
                    test_plan.test_tariff_price(app_pages, name = 'Продолжить')
                else:
                    test_plan.test_tariff_price(app_pages, name = 'подключить')
                #Проверка дтм опции в чеке (Имя/цена)
                if not pd.isna(row['old_options_price']) and pd.isna(row['new_options_price']):
                    price = None
                    text_part = '₽'
                    test_plan.test_check_dtm(app_pages, price , text_part)
                elif (pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price'])) or (row['old_options_price'] < row['new_options_price']):
                    price = 1
                    text_part = '₽'
                    test_plan.test_check_dtm(app_pages, price , text_part)
                if not pd.isna(row['new_options_price']):
                    test_plan.test_check_info(app_pages)
                #Проверка цены на кнопке оплатить и переход далее
                if not pd.isna(row['old_options_name']) and pd.isna(row['new_options_name']):
                    test_plan.test_button_save_click(app_pages)
                else:
                    type_case = 'options'
                    test_plan.test_check_price(type_case)
                    test_plan.test_button_pay_click(app_pages)
                #Проверка экрана успеха и переход далее (возврат на главный экран)
                test_plan.test_success_page(app_pages)
                test_plan.test_status_button_understand_click(app_pages)
                test_plan.test_go_main(app_pages)
                #Ожидание изменения тарифа на главном экране
                test_plan.test_wait_tariff(app_pages)
                #Проверка данных тарифа поле подключения
                test_plan.test_ap_tariff(app_pages)
                if not pd.isna(row['new_options_name']) and row['new_options_name'] == '100 SMS':
                    test_plan.test_sms_tariff(app_pages)


