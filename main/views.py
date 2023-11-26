from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.cache import cache_control

import pandas as pd

from .recognition import burnout


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def get_name_and_procent(file_path, employee_id):
    df = pd.read_csv(file_path)

    # Фильтрация данных по id сотрудника и временному интервалу
    filtered_data = df[(df['id сотрудника'] == employee_id)].tail(7)

    data = {
        'name': filtered_data['Сотрудник'].iloc[1],
        'procent': burnout.get_burnout_employee(employee_id)['chance'],
    }

    return data

def get_data_for_last_7_days(file_path, employee_id):
    # Чтение данных из CSV файла в DataFrame
    df = pd.read_csv(file_path)

    # Фильтрация данных по id сотрудника и временному интервалу
    filtered_data = df[(df['id сотрудника'] == employee_id)].tail(7)

    # Преобразование отфильтрованных данных в словарь
    employee_data = {}
    for _, row in filtered_data.iterrows():
        employee_data[row['Дата']] = {
            'frequencyData': row['Частота сообщения'],
            'volumeData': row['Объем сообщения'],
            'settingData': row['Настрой сообщения'],
            'commitFrequencyData': row['Регулярность коммитов'],
            'commitIntensityData': row['Интенсивность коммитов'],
            'commitTask_statusData': row['Статус задачи'],
            'commitPriority_changesData': row['Приоритетные изменения'],
            'commitDuration_activityyData': row['Продолжительность активности'],
            'commitActivity_nightData': row['Активность ночью'],
        }

    return employee_data

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def main(request):
    if is_ajax(request): 
        employees_burnout = burnout.get_burnout_employees()

        response = {
            'response': employees_burnout
        }

        return JsonResponse(response)

    return render(request, 'main/main.html')

@cache_control(max_age=0, no_cache=True, no_store=True, must_revalidate=True)
def user(requset, pk):
    file_path = 'main/data/new_employee_data.csv'
    employee_id = int(pk)

    if is_ajax(requset):
        data_7_days = get_data_for_last_7_days(file_path, employee_id)
        average_data = burnout.get_average_parameters(employee_id)

        response = {
            'data_7_days': data_7_days,
            'average_data': average_data,
        }

        return JsonResponse(response)
    
    user_info = get_name_and_procent(file_path, employee_id)
    average = burnout.get_average_parameters(employee_id)

    context = {
        'name': user_info['name'],
        'procent': user_info['procent'],
        'pk': pk,
    }
    
    return render(requset, 'main/user.html', context=context)