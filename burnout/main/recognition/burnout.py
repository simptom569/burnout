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


def get_burnout_employees() -> list:
    employee_data = load_data('main/data/employee_data.csv')
    recent_data = load_data('main/data/new_employee_data.csv')

    unique_employees = employee_data['id сотрудника'].unique()

    burnout_employees = []

    for employee in unique_employees:
        employee_data_filtered = employee_data[employee_data['id сотрудника'] == employee]
        recent_data_filtered = recent_data[recent_data['id сотрудника'] == employee].tail(7)

        burnout_percentage = calculate_burnout(employee_data_filtered, recent_data_filtered)

        employee = int(employee)
        employee_name = employee_data_filtered['Сотрудник'].iloc[0]

        employee = {
            'id': int(employee),
            'name': employee_name,
            'chance': f'{burnout_percentage:.2f}'
        }

        burnout_employees.append(employee)
    
    return burnout_employees

def get_burnout_employee(employee_id: int) -> dict:
    employee_data = load_data('main/data/employee_data.csv')
    recent_data = load_data('main/data/new_employee_data.csv')

    employee_data_filtered = employee_data[employee_data['id сотрудника'] == employee_id]
    recent_data_filtered = recent_data[recent_data['id сотрудника'] == employee_id].tail(7)

    burnout_percentage = calculate_burnout(employee_data_filtered, recent_data_filtered)

    employee_name = employee_data_filtered['Сотрудник'].iloc[0]

    result = {
        'id': int(employee_id),
        'name': employee_name,
        'chance': f'{burnout_percentage:.2f}'
    }

    return result

def get_average_parameters(employee_id: int) -> dict:
    employee_data = load_data('main/data/employee_data.csv')
    employee_data_filtered = employee_data[employee_data['id сотрудника'] == employee_id]

    if employee_data_filtered.empty:
        return {'error': 'Employee not found'}
    
    column_mapping = {
        'Частота сообщения': 'frequencyData',
        'Объем сообщения': 'volumeData',
        'Настрой сообщения': 'settingData',
        'Регулярность коммитов': 'commitFrequencyData',
        'Интенсивность коммитов': 'commitIntensityData',
        'Статус задачи': 'commitTask_statusData',
        'Приоритетные изменения': 'commitPriority_changesData',
        'Продолжительность активности': 'commitDuration_activityyData',
        'Активность ночью': 'commitActivity_nightData'
    }

    parameters = list(column_mapping.keys())

    average_values = {}

    for parameter in parameters:
        english_column_name = column_mapping[parameter]
        average_value = employee_data_filtered[parameter].mean()
        average_values[english_column_name] = round(average_value, 2)

    return average_values