import pandas as pd
import numpy as np
from datetime import timedelta, datetime

# Установка начальной даты и количества дней
start_date = datetime(2023, 1, 1)
num_days = 365

# Генерация случайных данных для трех сотрудников
employees = ['Вася', 'Андрей', 'Егор', 'Максим', 'Алексей', 'Иван', 'Дмитрий']
data = []

for employee in employees:
    for day in range(num_days):
        # Генерация случайных метаданных сообщений
        message_frequency = np.random.randint(50, 80)
        message_volume = np.random.randint(10, 30)
        message_tone = np.random.choice(['Позитивное', 'Нейтральное', 'Негативное'], p=[0.7, 0.2, 0.1])
        message_tone_encoding = {'Позитивное': 1, 'Нейтральное': 0, 'Негативное': -1}
        message_tone = message_tone_encoding[message_tone]
        communication_data = {'Частота сообщения': message_frequency, 'Объем сообщения': max(1, message_volume), 'Настрой сообщения': message_tone}

        # Генерация случайных метаданных о коммитах
        commit_regularity = np.random.randint(1, 5)
        commit_intensity = int(np.random.normal(loc=commit_regularity, scale=2))
        commit_intensity = max(1, commit_intensity)
        commit_data = {'Регулярность коммитов': commit_regularity, 'Интенсивность коммитов': commit_intensity}

        # Генерация случайных метаданных о задачах
        task_status = np.random.choice(['Выполнено', 'Отложено', 'Просрочено'], p=[0.7, 0.2, 0.1])
        task_status_encoding = {'Выполнено': 1, 'Отложено': 0, 'Просрочено': -1}
        task_status = task_status_encoding[task_status]
        task_priority_changes = np.random.randint(0, 3)
        task_data = {'Статус задачи': task_status, 'Приоритетные изменения': task_priority_changes}

        # Генерация случайных данных о времени активности приложений
        activity_duration = int(np.random.normal(loc=8, scale=2))
        activity_duration = max(1, activity_duration)
        late_night_activity = np.random.choice(['Да', 'Нет'], p=[0.1, 0.9])
        late_night_activity_encoding = {'Да': 1, 'Нет': 0}
        late_night_activity = late_night_activity_encoding[late_night_activity]
        app_activity_data = {'Продолжительность активности': activity_duration, 'Активность ночью': late_night_activity}

        # Создание строки данных для дня
        day_data = {'Дата': start_date + timedelta(days=day),
                    'Сотрудник': employee,
                    **communication_data,
                    **commit_data,
                    **task_data,
                    **app_activity_data}

        data.append(day_data)

# Создание DataFrame и запись в CSV
df = pd.DataFrame(data)
df.to_csv('employee_data.csv', index=False)