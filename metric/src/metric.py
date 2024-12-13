# metric.py

import pika
import json
import pandas as pd
import os

# Инициализация файла metric_log.csv
log_file_path = './logs/metric_log.csv'
if not os.path.exists(log_file_path):
    with open(log_file_path, 'w') as log_file:
        log_file.write('id,y_true,y_pred,absolute_error\n')

# Словари для хранения y_true и y_pred
y_true_dict = {}
y_pred_dict = {}

try:
    # Создаём подключение к серверу на локальном хосте
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # Объявляем очереди
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')

    # Создаём функцию callback для обработки данных из очереди
    def callback(ch, method, properties, body):
        message = json.loads(body)
        message_id = message['id']

        if method.routing_key == 'y_true':
            y_true = message['body']
            y_true_dict[message_id] = y_true
        elif method.routing_key == 'y_pred':
            y_pred = message['body']
            y_pred_dict[message_id] = y_pred

        # Проверяем, есть ли соответствующие y_true и y_pred
        if message_id in y_true_dict and message_id in y_pred_dict:
            y_true = y_true_dict[message_id]
            y_pred = y_pred_dict[message_id]
            absolute_error = abs(y_true - y_pred)

            # Записываем в файл
            with open(log_file_path, 'a') as log_file:
                log_file.write(f'{message_id},{y_true},{y_pred},{absolute_error}\n')

            # Удаляем обработанные сообщения
            del y_true_dict[message_id]
            del y_pred_dict[message_id]

    # Извлекаем сообщения из очередей
    channel.basic_consume(queue='y_true', on_message_callback=callback, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback, auto_ack=True)

    print('...Ожидание сообщений, для выхода нажмите CTRL+C')
    channel.start_consuming()
except Exception as e:
    print(f'Не удалось подключиться к очереди: {e}')