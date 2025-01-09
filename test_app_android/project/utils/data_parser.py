import pandas as pd


def parse_test_data(file_path):
    """
    Функция для чтения и фильтрации данных из Excel.
    """
    data = pd.ExcelFile(file_path)
    sheet_data = data.parse('Global')
    # filtered_data = sheet_data.dropna(subset=['Сценарий'])
    return  sheet_data.to_dict(orient='records')
