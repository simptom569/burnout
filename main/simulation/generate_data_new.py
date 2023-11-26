import pandas as pd
import numpy as np
from datetime import timedelta, datetime

start_date = datetime(2023, 3, 2)
num_days = 10

employees = ['Вася', 'Андрей', 'Егор', 'Максим', 'Алексей', 'Иван', 'Дмитрий']
data = []
number_sotr = 0

for employee in employees:
    number_sotr += 1
    for day in range(num_days):
        message_frequency = np.random.randint(10, 40)
        message_volume = np.random.randint(10, 20)
        message_tone = np.random.choice(['Позитивное', 'Нейтральное', 'Негативное'], p=[0.1, 0.1, 0.8])
        message_tone_encoding = {'Позитивное': 1, 'Нейтральное': 0, 'Негативное': -1}
        message_tone = message_tone_encoding[message_tone]
        communication_data = {'Частота сообщения': message_frequency, 'Объем сообщения': max(1, message_volume), 'Настрой сообщения': message_tone}

        commit_regularity = np.random.randint(0, 2)
        commit_intensity = int(np.random.normal(loc=commit_regularity, scale=2))
        commit_intensity = max(1, commit_intensity)
        commit_data = {'Регулярность коммитов': commit_regularity, 'Интенсивность коммитов': commit_intensity}

        task_status = np.random.choice(['Выполнено', 'Отложено', 'Просрочено'], p=[0.1, 0.1, 0.8])
        task_status_encoding = {'Выполнено': 1, 'Отложено': 0, 'Просрочено': -1}
        task_status = task_status_encoding[task_status]
        task_priority_changes = np.random.randint(5, 10)
        task_data = {'Статус задачи': task_status, 'Приоритетные изменения': task_priority_changes}

        activity_duration = int(np.random.normal(loc=10, scale=3))
        activity_duration = max(1, activity_duration)
        late_night_activity = np.random.choice(['Да', 'Нет'], p=[0.9, 0.1])
        late_night_activity_encoding = {'Да': 1, 'Нет': 0}
        late_night_activity = late_night_activity_encoding[late_night_activity]
        app_activity_data = {'Продолжительность активности': activity_duration, 'Активность ночью': late_night_activity}

        day_data = {'id сотрудника': number_sotr,
                    'Дата': start_date + timedelta(days=day),
                    'Сотрудник': employee,
                    **communication_data,
                    **commit_data,
                    **task_data,
                    **app_activity_data}

        data.append(day_data)

df = pd.DataFrame(data)
df.to_csv('../data/new_employee_data.csv', index=False)