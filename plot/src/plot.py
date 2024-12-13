# plot.py

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
import os

log_file_path = './logs/metric_log.csv'

while True:
    if os.path.exists(log_file_path):
        # Читаем данные из CSV файла
        data = pd.read_csv(log_file_path)

        # Проверяем, есть ли данные для построения графика
        if not data.empty:
            plt.figure(figsize=(10, 6))

            # Построение гистограммы и KDE
            sns.histplot(data['absolute_error'], bins=10, color='orange', kde=True, stat="count", alpha=0.6)
            sns.kdeplot(data['absolute_error'], color='orange', linewidth=2)

            # Настройка осей и подписи
            plt.xlabel('absolute_error')
            plt.ylabel('Count')
            plt.grid(True)

            # Сохраняем график
            plt.savefig('./logs/error_distribution.png')
            plt.close()

    # Задержка перед следующей итерацией
    time.sleep(5)