import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_burnout(employee_data, recent_data) -> float:
    parameters = ['Частота сообщения', 'Объем сообщения', 'Настрой сообщения', 'Регулярность коммитов', 'Интенсивность коммитов', 'Статус задачи', 'Приоритетные изменения', 'Продолжительность активности', 'Активность ночью']

    weights = {'Частота сообщения': 1, 'Объем сообщения': 1, 'Настрой сообщения': 4, 
               'Регулярность коммитов': 3, 'Интенсивность коммитов': 2, 'Статус задачи': 4, 
               'Приоритетные изменения': 2, 'Продолжительность активности': 1, 'Активность ночью': 4}

    diff_sum = 0
    total_weight = 0

    for parameter in parameters:
        weight = weights[parameter]

        min_value_employee = employee_data[parameter].min()
        max_value_employee = employee_data[parameter].max()

        min_value_recent = recent_data[parameter].min()
        max_value_recent = recent_data[parameter].max()

        range_employee = max_value_employee - min_value_employee
        range_recent = max_value_recent - min_value_recent

        if range_employee == 0:
            range_employee = 1

        relative_diff = abs((range_recent - range_employee) / range_employee)
        weighted_diff = relative_diff * weight

        diff_sum += weighted_diff
        total_weight += weight

    weighted_burnout_percentage = (diff_sum / total_weight) * 100

    return weighted_burnout_percentage


def get_burnout_employees() -> dict:
    employee_data = load_data('employee_data.csv')
    recent_data = load_data('new_employee_data.csv')

    unique_employees = employee_data['Сотрудник'].unique()

    burnout_employees = {}

    for employee in unique_employees:
        employee_data_filtered = employee_data[employee_data['Сотрудник'] == employee]
        recent_data_filtered = recent_data[recent_data['Сотрудник'] == employee].tail(7)

        burnout_percentage = calculate_burnout(employee_data_filtered, recent_data_filtered)

        print(f"Сотрудник: {employee}, Выгорание: {burnout_percentage:.2f}%")
        burnout_employees[employee] = f'{burnout_employees:.2f}'
    
    return burnout_employees