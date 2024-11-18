import csv
from nicegui import ui

# Функция для записи данных в файл CSV
def write_to_csv(data):
    file_exists = False
    try:
        with open('hacker_groups.csv', 'r', newline='') as f:
            file_exists = True
    except FileNotFoundError:
        pass
    
    with open('hacker_groups.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow([ 
                'Дата атаки', 'Название группировки', 'Ссылка на канал/сообщество',
                'Язык общения', 'Регион атак', 'Альтернативные названия', 'Связи с другими группировками',
                'Атакуемые организации', 'Методы атаки', 'Какой софт и вредоносное ПО использует группировка',
                'Целевая направленность', 'Мотив', 'Регулярность атак', 'Уровень угрозы'
            ])
        writer.writerow([ 
            data['Дата атаки'], data['Название группировки'], data['Ссылка на канал/сообщество'],
            data['Язык общения'], data['Регион атак'], data['Альтернативные названия'], data['Связи с другими группировками'],
            data['Атакуемые организации'], ", ".join(data['Методы атаки']), data['Какой софт и вредоносное ПО использует группировка'],
            data['Целевая направленность'], data['Мотив'], data['Регулярность атак'],
            data['Уровень угрозы']
        ])

# Функция для обработки данных формы
def submit_form(date, name, channel, language, region, aliases, connections, incidents, methods, malware, focus, motive, frequency, threat_level):
    # Проверка на обязательные поля
    if not date or not name or not language or not region or not focus or not motive or not frequency:
        ui.notify('Пожалуйста, заполните все обязательные поля!', color='red')
        return

    # Проверка на обязательные поля для методов атаки, если они выбраны
    if not methods:
        ui.notify('Пожалуйста, выберите хотя бы один метод атаки!', color='red')
        return

    # Проверка на обязательные поля для вредоносного ПО
    if not malware:
        ui.notify('Пожалуйста, укажите, какой софт и вредоносное ПО использует группировка!', color='red')
        return

    # Проверка на обязательное поле для уровня угрозы
    if not threat_level:
        ui.notify('Пожалуйста, выберите уровень угрозы!', color='red')
        return

    # Составляем данные для записи в CSV
    data = {
        'Дата атаки': date,
        'Название группировки': name,
        'Ссылка на канал/сообщество': channel,
        'Язык общения': language,
        'Регион атак': region,
        'Альтернативные названия': aliases,
        'Связи с другими группировками': connections,
        'Атакуемые организации': incidents,
        'Методы атаки': methods,
        'Какой софт и вредоносное ПО использует группировка': malware,
        'Целевая направленность': focus,
        'Мотив': motive,
        'Регулярность атак': frequency,
        'Уровень угрозы': threat_level
    }
    write_to_csv(data)
    ui.notify('Данные успешно записаны в файл hacker_groups.csv!', color='green')

@ui.page('/')
def main_page():
    ui.label('Форма для фиксации информации о хакерских группировках') \
        .style('font-size: 24px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;')

    # Поля формы
    attack_date = ui.date().style('margin-bottom: 15px; width: 300px;')
    group_name = ui.input(label='Название группировки(обязательно)').style('margin-bottom: 15px; width: 500px;')
    channel_link = ui.input(label='Ссылка на канал или сообщество группировки').style('margin-bottom: 15px; width: 500px;')
    language = ui.input(label='Язык общения(обязательно)').style('margin-bottom: 15px; width: 500px;')
    region = ui.input(label='Регион атак(обязательно)').style('margin-bottom: 15px; width: 500px;')
    aliases = ui.input(label='Альтернативные названия').style('margin-bottom: 15px; width: 500px;')
    connections = ui.textarea(label='Связи с другими группировками').style('margin-bottom: 15px; width: 500px;')
    incidents = ui.textarea(label='Атакуемые организации').style('margin-bottom: 15px; width: 500px;')

    attack_methods = ui.select([ 
        'Нарушение контроля доступа', 'Недостатки криптографии', 'Инъекции', 
        'Небезопасный дизайн архитектуры приложения', 'Небезопасная конфигурация', 
        'Использование уязвимых или устаревших компонентов', 'Ошибки идентификации и аутентификации', 
        'Нарушения целостности программного обеспечения и данных', 'Ошибки логирования и мониторинга безопасности', 
        'Подделка запросов на стороне сервера'
    ], label='Методы атаки(обязательно)', multiple=True).style('margin-bottom: 15px; width: 500px;')

    malware_software = ui.textarea(label='Какой софт и вредоносное ПО использует группировка(обязательно)').style('margin-bottom: 15px; width: 500px;')
    focus = ui.input(label='Целевая направленность(обязательно)').style('margin-bottom: 15px; width: 500px;')
    motive = ui.input(label='Мотив(обязательно)').style('margin-bottom: 15px; width: 500px;')
    attack_frequency = ui.input(label='Регулярность атак(обязательно)').style('margin-bottom: 15px; width: 500px;')
    threat_level = ui.select(['Низкий', 'Средний', 'Высокий', 'Очень высокий'], label='Уровень угрозы(обязательно)').style('margin-bottom: 15px; width: 500px;')

    # Кнопка для отправки формы
    ui.button('Отправить', on_click=lambda: submit_form(
        date=attack_date.value,
        name=group_name.value,
        channel=channel_link.value,
        language=language.value,
        region=region.value,
        aliases=aliases.value,
        connections=connections.value,
        incidents=incidents.value,
        methods=attack_methods.value,
        malware=malware_software.value,
        focus=focus.value,
        motive=motive.value,
        frequency=attack_frequency.value,
        threat_level=threat_level.value,
    )).style('background-color: #3498db; color: white; font-weight: bold; border-radius: 8px; padding: 10px 20px;')

ui.run()
