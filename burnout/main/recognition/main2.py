import pandas as pd

def load_data(file_path):
    return pd.read_csv(file_path)

def calculate_burnout(employee_data, recent_data):
    parameters = ['Частота сообщения', 'Объем сообщения', 'Настрой сообщения', 'Регулярность коммитов', 'Интенсивность коммитов', 'Статус задачи', 'Приоритетные изменения', 'Продолжительность активности', 'Активность ночью']

    diff_sum = 0
    total_params = 0

    for parameter in parameters:
        min_value_employee = employee_data[parameter].min()
        max_value_employee = employee_data[parameter].max()

        min_value_recent = recent_data[parameter].min()
        max_value_recent = recent_data[parameter].max()

        range_employee = max_value_employee - min_value_employee
        range_recent = max_value_recent - min_value_recent

        if range_employee == 0:
            range_employee = 1

        relative_diff = abs((range_recent - range_employee) / range_employee)

        diff_sum += relative_diff
        total_params += 1

    average_diff = diff_sum / total_params
    burnout_percentage = average_diff * 100

    return burnout_percentage

def main():
    employee_data = load_data('employee_data.csv')
    recent_data = load_data('new_employee_data.csv')

    unique_employees = employee_data['Сотрудник'].unique()

    for employee in unique_employees:
        employee_data_filtered = employee_data[employee_data['Сотрудник'] == employee]
        recent_data_filtered = recent_data[recent_data['Сотрудник'] == employee].tail(7)

        burnout_percentage = calculate_burnout(employee_data_filtered, recent_data_filtered)

        print(f"Сотрудник: {employee}, Выгорание: {burnout_percentage:.2f}%")

if __name__ == "__main__":
    main()