# plot.py

import pandas as pd
import matplotlib.pyplot as plt
import time
import os

log_file_path = './logs/metric_log.csv'

while True:
    if os .path.exists(log_file_path):
        # Читаем данные из CSV файла
        data = pd.read_csv(log_file_path)

        # Проверяем, есть ли данные для построения графика
        if not data.empty:
            plt.figure(figsize=(10, 6))
            plt.hist(data['absolute_error'], bins=30, color='blue', alpha=0.7)
            plt.title('Распределение абсолютных ошибок')
            plt.xlabel('Абсолютная ошибка')
            plt.ylabel('Частота')
            plt.grid(True)

            # Сохраняем график
            plt.savefig('./logs/error_distribution.png')
            plt.close()

    # Задержка перед следующей итерацией
    time.sleep(5)