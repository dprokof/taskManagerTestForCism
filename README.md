# Документация к проекту "Task Manager"
### Общее описание
Проект "Task Manager" — это сервис для управления задачами, который позволяет создавать, отслеживать и обрабатывать задачи. Сервис включает в себя:

REST API для создания задач и получения их статуса.
RabbitMQ для создания задач через очереди сообщений.
PostgreSQL для хранения информации о задачах.
Docker для контейнеризации всего приложения. 
### Архитектура системы
Система состоит из трех основных компонентов:

Flask API — веб-приложение для взаимодействия с пользователем через REST API.
RabbitMQ — система обмена сообщениями для асинхронной обработки задач.
PostgreSQL — база данных для хранения задач и их статусов.
Компоненты взаимодействуют через:

REST API для создания и получения задач.
RabbitMQ для отправки сообщений о новых задачах, которые обрабатываются асинхронно.
PostgreSQL для хранения состояния задач. 

### Запуск проекта
#### Предварительные требования
Для запуска проекта на вашем локальном компьютере необходимо установить:

Docker

Docker Compose

### Запуск приложения с помощью Docker Compose
Клонируйте репозиторий на ваш локальный компьютер:

````
git clone https://github.com/yourusername/task-manager.git
cd task-manager
````

Создайте файл .env с необходимыми переменными окружения для подключения к базе данных и RabbitMQ:

````
touch .env
````
Пример содержимого .env:
````
FLASK_APP=app.py
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@postgres:5432/task_db
RABBITMQ_URL=amqp://rabbitmq
````
Запустите контейнеры с помощью docker-compose:

````
docker-compose up --build
````
Эта команда создаст и запустит контейнеры для Flask, PostgreSQL и RabbitMQ.

### Остановка контейнеров
Для остановки контейнеров используйте команду:

````
docker-compose down
````
### Пересборка контейнеров
Если вам нужно пересобрать контейнеры после изменения исходных файлов:

````
docker-compose up --build
````
### Структура базы данных
База данных PostgreSQL будет содержать одну таблицу для хранения задач:

````

Column	Type	Description
id	SERIAL	Уникальный идентификатор задачи
status	VARCHAR	Статус задачи (New, In Progress, Completed, Failed)
created_at	TIMESTAMP	Дата и время создания задачи
updated_at	TIMESTAMP	Дата и время последнего обновления статуса задачи
```` 

SQL-скрипт для создания таблицы:
````
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'New',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
````
### API Эндпоинты
#### POST /tasks
Описание: Создание новой задачи.

Запрос:

Метод: POST
URL: /tasks
Тело запроса: пустое

Код ответа: 201 Created
Тело ответа: ID созданной задачи.
````

{
    "id": 1
}
````
#### GET /tasks/{id}
Описание: Получение информации о задаче по ID.

Запрос:

Метод: GET
URL: /tasks/{id}
Ответ:

Код ответа: 200 OK
Тело ответа:
````
{
    "id": 1,
    "status": "New",
    "created_at": "2024-12-17T10:00:00",
    "updated_at": "2024-12-17T10:00:00"
}
````
#### GET /tasks
Описание: Получение списка задач с возможностью фильтрации по статусу.

Запрос:

Метод: GET
URL: /tasks
Параметры запроса:
status: фильтрация по статусу задачи (New, In Progress, Completed, Failed).
Ответ:

Код ответа: 200 OK
````
[
    {
        "id": 1,
        "status": "New",
        "created_at": "2024-12-17T10:00:00",
        "updated_at": "2024-12-17T10:00:00"
    },
    {
        "id": 2,
        "status": "In Progress",
        "created_at": "2024-12-17T10:05:00",
        "updated_at": "2024-12-17T10:06:00"
    }
]
````
### Создание задач через очередь сообщений (RabbitMQ)
Задачи могут быть также созданы и отправлены в очередь RabbitMQ. Для этого используйте следующий код:

Код создания задачи через RabbitMQ:

````
import pika
import json

def create_task_via_rabbitmq():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue')

    task = {
        'status': 'New'
    }

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=json.dumps(task)
    )

    connection.close()
````

Задача будет помещена в очередь RabbitMQ, и её обработка будет происходить в рабочем процессе.


### Логирование
Все события, связанные с обработкой задач, логируются с использованием стандартной библиотеки Python logging. Логи могут быть записаны в файл, который будет доступен для мониторинга и анализа.

### Документация API с использованием Swagger/OpenAPI
Для документации API используется Swagger. Для этого нужно добавить библиотеку flask-swagger-ui и настроить её в вашем Flask-приложении.

Swagger UI будет доступен по адресу http://localhost:5000/swagger.