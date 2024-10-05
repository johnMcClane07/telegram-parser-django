# telegram-parser-django

Сайт для парсинга и анализа коментариев в телеграм каналах конкурентов

## Описание
<img width="1470" alt="Снимок экрана 2024-10-04 в 21 45 54" src="https://github.com/user-attachments/assets/dda882a7-4887-4e88-a25c-2cce6d7f349f">

Этот проект представляет собой сайт, созданный для парсинга комментариев в Telegram каналах конкурентов нашей компании. Основная цель проекта - собирать контакты (ники, номера телефонов) клиентов конкурентов, которые оставляют мнения и вопросы в комментариях к публикациям в этих каналах.

Цель проекта - предоставить инструмент для сбора контактов потенциальных и действующих клиентов конкурентов, которые могут быть использованы в сервисах нашей компании для улучшения маркетинговых стратегий, повышения конверсии и увеличения продаж.

## Установка

1)Клонировать репозиторий:
```bash
git clone https://github.com/johnMcClane07/telegram-parser-django
```
2)Активация виртуальной среды:
```bash
source parserenv/bin/activate
```

3)Заполнить данные в settings.py:
  ```python
API_ID='your api_id'
API_HASH='your api_hash'

#mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your db name', 
        'USER': 'your username',  
        'PASSWORD': 'your password', 
        'HOST': 'localhost',  
        'PORT': '3306',  
    }
}
```
api_id и api_hash мы берем с [оффициального сайта Telegram](https://my.telegram.org/auth)

4)Выполнить миграции:
```bash
python3 manage.py migrate
```



## Использование

Для начала я, как начальник компании, создаю через админку аккаунты для своих сотрудников и раздаю им данные от их аккаунтов. Сотрудники входят в свои аккаунты (аутентификация, кстати, реализована через JWT) и начинают работу по целевым телеграм-каналам конкурентов. Через историю запросов они могут более детально изучать, какую реакцию аудитории вызвал пост конкурентов (общее число комментариев, сколько негативных, положительных и нейтральных комментариев). Также сотрудники могут удалять посты из истории запросов, если они уже не нужны. После сбора всей необходимой информации, мы можем посмотреть список всех телефонных номеров пользователей, оставлявших комментарии конкурентам, а также список всех недовольных комментариев. Все данные можно скачать в виде Excel-таблицы и начать парсинг уже другого телеграм-канала конкурента.


## Скриншоты
Главная страница 
<img width="1470" alt="Снимок экрана 2024-10-05 в 12 52 21" src="https://github.com/user-attachments/assets/44b8c20a-2d20-4bfe-a42a-608c422d17a3">

Ввод URL поста 
<img width="1470" alt="Снимок экрана 2024-10-05 в 12 53 49" src="https://github.com/user-attachments/assets/8e15f871-a194-459a-b0f0-aceeac3e7b98">

Парсинг завершен 
<img width="1470" alt="Снимок экрана 2024-10-05 в 12 56 15" src="https://github.com/user-attachments/assets/26319c03-521c-4b46-a6d4-8d774fa0f17f">

Переходим в историю запросов 
<img width="1470" alt="Снимок экрана 2024-10-05 в 12 58 03" src="https://github.com/user-attachments/assets/eb322a5b-fbb7-441b-b566-664cff8ad5dd">

Получаем делальную информацию о посте 
<img width="1470" alt="Снимок экрана 2024-10-05 в 12 58 51" src="https://github.com/user-attachments/assets/4d2ab13f-d5b4-4fc2-8252-47b148609277">

Смотрим список всех полученных номеров. Скачиваем их в формате excel
<img width="1470" alt="Снимок экрана 2024-10-05 в 13 15 25" src="https://github.com/user-attachments/assets/6483fccb-e57c-483d-a99c-ec4c8e918288">

Также получаем список негативных коментариев и скачиваем его
<img width="1470" alt="Снимок экрана 2024-10-05 в 13 07 07" src="https://github.com/user-attachments/assets/9a167f9f-d43f-4648-8b09-920a96412f83">



## Контакты


Глазков Даниил

Telegram: @daniil_glazk

email: glazkov.daniil2004@gmail.com

## Спасибо

Если вам понравился проект, пожалуйста, оставьте звездочку на GitHub.
