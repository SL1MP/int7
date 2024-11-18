import csv
from nicegui import ui

# Функция для записи данных в файл CSV
def write_to_csv(data):
    file_exists = False
    try:
        with open('incidents.csv', 'r', newline='') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open('incidents.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        # Если файл не существует, записываем заголовки
        if not file_exists:
            writer.writerow(['Дата сообщения', 'Источник', 'Название организации', 'Тип инцидента', 'Методы атаки', 'Описание данных', 'Возможные последствия'])
        # Записываем данные формы в CSV
        writer.writerow([
            data['Дата сообщения'],
            data['Источник'],
            data['Название организации'],
            data['Тип инцидента'],
            data['Методы атаки'],
            data['Описание данных'],
            data['Возможные последствия'],
        ])

# Функция для обработки данных формы
def submit_form(date, source, organization, incident, methods, data_desc, consequences):
    # Проверка на обязательные поля
    if not date or not source or not organization or not incident or not consequences:
        ui.notify('Пожалуйста, заполните все обязательные поля!', color='red')
        return
    
    # Дополнительные проверки для специфичных полей
    if incident == 'Взлом' and not methods:
        ui.notify('Пожалуйста, укажите методы атаки для инцидента "Взлом"!', color='red')
        return
    if incident == 'Утечка данных' and not data_desc:
        ui.notify('Пожалуйста, укажите описание данных для инцидента "Утечка данных"!', color='red')
        return
    
    # Составляем данные для записи в CSV
    data = {
        'Дата сообщения': date,
        'Источник': source,
        'Название организации': organization,
        'Тип инцидента': incident,
        'Методы атаки': methods if incident == 'Взлом' else None,
        'Описание данных': data_desc if incident == 'Утечка данных' else None,
        'Возможные последствия': consequences,
    }
    
    write_to_csv(data)  # Записываем данные в CSV
    ui.notify('Данные успешно записаны в файл incidents.csv!', color='green')

@ui.page('/')
def main_page():
    ui.label('Форма для фиксации инцидентов безопасности')
    
    # Поля формы
    date_input = ui.date()
    source_input = ui.input(label='Источник сообщения(обязательно)').style('margin-bottom: 15px; width: 500px;')
    organization_input = ui.input(label='Название организации(обязательно)').style('margin-bottom: 15px; width: 500px;')
    incident_type = ui.select(['Призыв к атаке', 'Утечка данных', 'Взлом'], label='Тип инцидента(обязательно)').style('margin-bottom: 15px; width: 500px;')
    attack_methods = ui.select([
        'Нарушение контроля доступа', 'Недостатки криптографии', 'Инъекции',
        'Небезопасный дизайн архитектуры приложения', 'Небезопасная конфигурация',
        'Использование уязвимых или устаревших компонентов', 'Ошибки идентификации и аутентификации',
        'Нарушения целостности программного обеспечения и данных', 'Ошибки логирования и мониторинга безопасности',
        'Подделка запросов на стороне сервера'
    ], label='Методы атаки(обязательно)', multiple=True).style('margin-bottom: 15px; width: 500px;')
    attack_methods.visible = False  # Скрываем поле при инициализации
    
    data_description = ui.input(label='Какие данные находятся в базе данных(обязательно)').style('margin-bottom: 15px; width: 500px;')
    data_description.visible = False  # Скрываем поле при инициализации
    
    consequences = ui.textarea(label='Возможные последствия для организации(обязательно)').style('margin-bottom: 15px; width: 500px;')
    
    # Используем таймер для слежения за изменением incident_type
    def check_incident_type():
        attack_methods.visible = (incident_type.value == 'Взлом')
        data_description.visible = (incident_type.value == 'Утечка данных')
        attack_methods.update()
        data_description.update()

    ui.timer(0.5, check_incident_type)  # Проверяем каждые 0.5 секунды
    
    # Кнопка для отправки формы
    ui.button('Отправить', on_click=lambda: submit_form(
        date=date_input.value,
        source=source_input.value,
        organization=organization_input.value,
        incident=incident_type.value,
        methods=attack_methods.value,
        data_desc=data_description.value,
        consequences=consequences.value,
    ))

ui.run()
