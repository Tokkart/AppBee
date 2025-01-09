import allure
import pandas as pd

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

        #ДТМ опция
        if not pd.isna(data.get('new_options_name')):
            self.name_dtm = str(data.get('new_options_name'))  # ДТМ опция
        if not pd.isna(data.get('new_options_price')):
            self.price_dtm = int(data.get('new_options_price'))
        else:
            self.price_dtm = 0  # Цена ДТМ опции
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
    def test_go_settings_tariff(self):
        #Стартовая страница -> переход в мои продукты
        self.app_pages.main.go_my_product()
        # Мои продукты -> переход в настройки тарифа
        self.app_pages.my_products.settings_click()
        # Ожидание страницы UP
        self.app_pages.tariff_up.wait_page(self.name_tp)
    def test_go_new_tariff(self):
        #Стартовая страница -> переход в мои продукты
        self.app_pages.main.go_my_product()
        # Мои продукты -> переход на страницу смены тариф
        self.app_pages.my_products.change_tariff_click()
    def test_select_tariff(self, app_pages):
        # Выбор тарифа
        self.app_pages.list.go_tariff(self.name_tp)
        # Ожидание страницы UP
        self.app_pages.tariff_up.wait_page(self.name_tp)
    def test_select_data(self):
        # Выбор ГБ
        self.app_pages.tariff_up.select_gb(self.value_gb)

    def test_select_voice(self):
        # выбор МИН
        self.app_pages.tariff_up.select_min(self.value_min)

    def test_select_dtm(self):
        # Скролл вниз
        self.app_pages.tariff_up.scroll_down_up()
        # Поиск клик по тоглу дтм опции
        self.app_pages.tariff_up.dtm_toggle_click(self.name_dtm)
        # Проверка АП дтм опции
        try:
            self.app_pages.tariff_up.dtm_price(self.name_dtm, self.price_dtm)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_dtm_price(self):
        # Скролл вниз
        self.app_pages.tariff_up.scroll_down_up()
        # Проверка АП дтм опции
        try:
            self.app_pages.tariff_up.dtm_price(self.name_dtm, self.price_dtm)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_tariff_price(self, name):#Проверка общей АП ТП + ДТМ
        try:
            self.app_pages.tariff_up.button_price(self.price_total, name)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        # Клик далее
        self.app_pages.tariff_up.button_next_click(name)

    def test_precheck(self, old_dtm_name, changing_tariff):# Ожидание предчека
        self.app_pages.precheck.wait_page_precheck()
        if old_dtm_name is None:
            try:
                if changing_tariff is not None:
                    self.app_pages.precheck.changing_tariff(self.value_gb, self.value_min, self.price_tp, self.value_gb_old, self.value_min_old, self.price_tp_old,  self.price_dtm)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
            self.app_pages.precheck.button_next()
        else:
            try:
                self.app_pages.precheck.dtm_delete(old_dtm_name)
                if changing_tariff is not None:
                    self.app_pages.precheck.changing_tariff(self.value_gb, self.value_min, self.price_tp, self.value_gb_old, self.value_min_old, self.price_tp_old,  self.price_dtm)
            except Exception as e:
                allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
            self.app_pages.precheck.button_next()

    def test_check_text(self, text_part):
        self.app_pages.check.wait_check_page(self.name_tp)
        try:
            self.app_pages.check.mobil_text(self.value_gb, self.value_gb_old, self.value_min, self.value_min_old, text_part)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    def test_check_mobile_price(self, text_part):
        self.app_pages.check.wait_check_page(self.name_tp)
        try:
            self.app_pages.check.mobil_price(self.price_tp, self.price_tp_old, self.value_gb, self.value_gb_old, self.value_min, self.value_min_old, text_part)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_check_dtm(self, price, text_part):
        self.app_pages.check.wait_check_page(self.name_tp)
        try:
            if price is not None:
                self.app_pages.check.dtm_price(self.name_dtm, self.price_dtm, text_part)
            else:
                self.app_pages.check.dtm_name(self.name_dtm_old)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    def test_single_payment(self):
        try:
            self.app_pages.check.single_payment()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)

    def test_check_info(self):
        try:
            self.app_pages.check.info_text(self.value_gb, self.value_min, self.price_tp, self.value_gb_old, self.value_min_old, self.price_tp_old,  self.price_dtm)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
        self.app_pages.check.button_understand_click()
    def test_check_price(self, payment, price):
        try:
            self.app_pages.check.button_price(price + payment + self.price_dtm)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    #Клик по кнопке оплаты
    def test_button_pay_click(self):
        self.app_pages.check.button_pay_click()
    #Клик по кнопке Сохранить
    def test_button_save_click(self):
        self.app_pages.check.button_save_click()
    # Проверка страницы успеха
    def test_success_page(self):
        try:
            self.app_pages.status.success_text()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    #Проверка страницы недостаточности средств
    def test_low_balance_page(self):
        #Проверка текста недостаточности средств
        self.app_pages.status.low_balance_text()
        #Проверка перехода на страницу пополнения баланса
        self.app_pages.status.pay_balance()
    # Клик по кнопке Понятно
    def test_status_button_understand_click(self):
        self.app_pages.status.button_understand_click()
    #Переход на главную страницу
    def test_go_main(self):
        self.app_pages.my_products.go_main()
    #Ожидание изменения тарифа
    def test_wait_tariff(self, param):
        if param == 1:
            number = self.value_gb_total
            text = 'гб'
            self.app_pages.my_products.wait_changes_tariff(number, text)
        elif param == 2:
            number = self.value_min_total
            text = 'мин'
            self.app_pages.my_products.wait_changes_tariff(number, text)
        elif param == 3:
            number = self.price_total
            text = '₽/мес'
            self.app_pages.my_products.wait_changes_tariff(number, text)

    # Проверка АП тарифа после смены
    def test_ap_tariff(self):
        try:
            self.app_pages.my_products.ap(self.price_total)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка ГБ тарифа после смены
    def test_gb_tariff(self):
        try:
            self.app_pages.my_products.gb(self.value_gb_total)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка МИН тарифа после смены
    def test_min_tariff(self):
        try:
            self.app_pages.my_products.min(self.value_min_total)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка названия тарифа после смены
    def test_name_tariff(self):
        try:
            self.app_pages.my_products.name(self.name_tp)
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)
    # Проверка Даты списания следующего списания АП
    def test_date_tariff(self):
        try:
            self.app_pages.my_products.data()
        except Exception as e:
            allure.attach(str(e), name="Ошибка", attachment_type=allure.attachment_type.TEXT)



@allure.feature("Тестирование тарифа UP")
def test_smena_pr(driver, file_data, app_pages):
    """
    Запускает тесты на основе данных из файла.
    """
    # for row in file_data:
    #     execute_scenario(driver, row, app_pages)

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
            #Переход на страницу смены тарифа
            test_plan.test_go_new_tariff()
            #Выбираем тариф
            test_plan.test_select_tariff(app_pages)
            #Выбираем гб и минуты, если пресеты не дефолтные
            if row['default'] == 'no':
                test_plan.test_select_data()
                test_plan.test_select_voice()

            #Проверка ДТМ (цена/подключение опции)
            if not pd.isna(row['new_options_price']):
                if row['new_options_price'] > 0:
                    test_plan.test_select_dtm()
                else:
                    test_plan.test_dtm_price()
            #Проверка итоговой цены за тариф и переход далее
            if row['old_tariff_soc'] == row['new_tariff_soc']:
                test_plan.test_tariff_price(name = 'Продолжить')
            else:
                test_plan.test_tariff_price(name = 'подключить')
            #Проверка предчека и переход далее
            if not pd.isna(row['old_options_name']):
                test_plan.test_precheck(old_dtm_name = row['old_options_name'], changing_tariff = None)
            #Проверка чека
            #Проверка в чеке описания изменений тарифа (Текс/цена)
            test_plan.test_check_mobile_price(text_part = '₽/мес')
            #Проверка дтм опции в чеке (Имя/цена)
            if not pd.isna(row['new_options_price']):
                test_plan.test_check_dtm(price = 1, text_part = '₽/мес')
            #Проверка разового платежа за смену тарифа
            test_plan.test_single_payment()
            #Проверка цены на кнопке оплатить и переход далее
            price = row['new_tariff_price']
            payment = 200
            test_plan.test_check_price(payment, price)
            test_plan.test_button_pay_click()
            if row['balance'] <= 200:
                #Проверка при недостаточности средств
                test_plan.test_low_balance_page()
            else:
                #Проверка экрана успеха и переход далее (возврат на главный экран)
                test_plan.test_success_page()
                test_plan.test_status_button_understand_click()
                test_plan.test_go_main()
                #Ожидание изменения тарифа на главном экране
                if row['new_gb_value'] > 0:
                    param = 1 #проверяем по гб
                elif row['new_min_value'] > 0:
                    param = 2 #проверяем по минутам
                else:
                    param = 3   #проверяем по АП
                test_plan.test_wait_tariff(param)
                #Проверка данных тарифа поле подключения
                test_plan.test_ap_tariff()
                if row['new_gb_value'] > 0:
                    test_plan.test_gb_tariff()
                if row['new_min_value'] > 0:
                    test_plan.test_min_tariff()
                test_plan.test_name_tariff()
                test_plan.test_date_tariff()

    # Проверка смены пресета
    elif row['old_tariff_soc'] == row['new_tariff_soc']:
        with allure.step(f'Тест-кейс: смена пресета "{row['new_tariff_name']}"'):
            if (row['old_gb_value'] != row['new_gb_value']) or (row['old_min_value'] != row['new_min_value']):
                #Переходим в карточку тарифа
                test_plan.test_go_settings_tariff()
                #Подключаем ГБ и МИН если необходимо
                if row['old_gb_value'] != row['new_gb_value']:
                    test_plan.test_select_data()
                if row['old_min_value'] != row['new_min_value']:
                    test_plan.test_select_voice()
                #Проверка ДТМ (цена/подключение опции)
                if not pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    if row['new_options_price'] > row['old_options_price']:
                        test_plan.test_select_dtm()
                    else:
                        test_plan.test_dtm_price()
                elif pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price']):
                    if row['new_options_price'] > 0:
                        test_plan.test_select_dtm()
                    else:
                        test_plan.test_dtm_price()
                #Проверка итоговой цены за тариф и переход далее
                if row['old_tariff_soc'] == row['new_tariff_soc']:
                    test_plan.test_tariff_price(name = 'Продолжить')
                else:
                    test_plan.test_tariff_price(name = 'подключить')
                #Проверка предчека и переход далее
                if not pd.isna(row['old_options_name']) and pd.isna(row['new_options_name']):
                    test_plan.test_precheck(old_dtm_name = row['old_options_name'], changing_tariff = 1)
                else:
                    test_plan.test_precheck(old_dtm_name = None, changing_tariff = 1)
                #Проверка описания изменений тарифа (Текс/цена)
                if (row['new_gb_value'] <= row['old_gb_value']) and (row['new_min_value'] <= row['old_min_value']):
                    test_plan.test_check_text(text_part = '₽')
                else:
                    test_plan.test_check_mobile_price(text_part = '₽')
                #Проверка дтм опции в чеке (Имя/цена)
                if not pd.isna(row['old_options_price']) and pd.isna(row['new_options_price']):
                    test_plan.test_check_dtm(price = None, text_part = '₽')
                elif (pd.isna(row['old_options_price']) and not pd.isna(row['new_options_price'])) or (row['old_options_price'] < row['new_options_price']):
                    test_plan.test_check_dtm(price = 1, text_part = '₽')
                test_plan.test_check_info()
                #Проверка цены на кнопке оплатить и переход далее
                if (row['new_gb_value'] <= row['old_gb_value'] and row['new_min_value'] < row['old_min_value']) and pd.isna(row['new_options_price']):
                    test_plan.test_button_save_click()
                else:
                    price = row['new_tariff_price'] - row['old_tariff_price']
                    if price < 0:
                        price = 0
                    payment = 0
                    test_plan.test_check_price(payment, price)
                    test_plan.test_button_pay_click()
                #Проверка экрана успеха и переход далее (возврат на главный экран)
                test_plan.test_success_page()
                test_plan.test_status_button_understand_click()
                test_plan.test_go_main()
                #Ожидание изменения тарифа на главном экране
                if row['new_gb_value'] > 0:
                    param = 1 #проверяем по гб
                elif row['new_min_value'] > 0:
                    param = 2 #проверяем по минутам
                else:
                    param = 3   #проверяем по АП
                test_plan.test_wait_tariff(param)
                #Проверка данных тарифа поле подключения
                test_plan.test_ap_tariff()
                if row['new_gb_value'] > 0:
                    test_plan.test_gb_tariff()
                if row['new_min_value'] > 0:
                    test_plan.test_min_tariff()
                test_plan.test_name_tariff()
                test_plan.test_date_tariff()


