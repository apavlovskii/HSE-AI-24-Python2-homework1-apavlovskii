import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor


# Расчет скользящего среднего
def calc_moving_avg(data, window=30):
    return data['temperature'].rolling(window=window).mean()


# Анализ данных
def analyze_temperature(data):
    grouped = data.groupby(['city', 'season'])
    results = []
    for (city, season), group in grouped:
        mean_temp = group['temperature'].mean()
        std_temp = group['temperature'].std()
        anomalies = group[(group['temperature'] < mean_temp - 2 * std_temp) |
                          (group['temperature'] > mean_temp + 2 * std_temp)]
        results.append({
            'city': city,
            'season': season,
            'mean': mean_temp,
            'std': std_temp,
            'anomalies': anomalies
        })
    return results


# Работа с OpenWeatherMap API
def fetch_current_temperature(city, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"temp": data['main']['temp']}
    elif response.status_code == 401:
        return {"error": "Invalid API key"}
    else:
        return {"error": "Unable to fetch data"}


# Streamlit App
st.title("Анализ температурных данных и мониторинг текущей температуры через OpenWeatherMap API")
st.sidebar.title("Опции на выбор")

# Загрузка файла с историческими данными
data_file = st.sidebar.file_uploader("Загрузите файл данных (CSV)", type=["csv"])

if data_file:
    data = pd.read_csv(data_file, parse_dates=['timestamp'])
    st.write("### Исторические данные температуры воздуха")
    st.write(data.head())

    # Выбор города
    cities = sorted(data['city'].unique())
    selected_city = st.sidebar.selectbox("Выберите город", cities)

    # Анализ данных
    st.write(f"### Анализ данных {selected_city}")
    city_data = data[data['city'] == selected_city]
    city_data['moving_average'] = calc_moving_avg(city_data)

    with ThreadPoolExecutor() as executor:
        seasonal_analysis = executor.submit(analyze_temperature, city_data).result()

    # Отображение статистики
    for result in seasonal_analysis:
        if result['city'] == selected_city:
            st.write(f"#### Время года: {result['season']}")
            st.write(f"Средняя температура: {result['mean']:.2f} °C")
            st.write(f"СКО: {result['std']:.2f} °C")
            st.write(f"Аномалии: {len(result['anomalies'])}")

    # График временного ряда
    st.write("### Временной ряд температур с аномалиями")
    plt.figure(figsize=(10, 6))
    plt.plot(city_data['timestamp'], city_data['temperature'], label='Температура')
    plt.plot(city_data['timestamp'], city_data['moving_average'], label='Скользящее среднее за 30 дней', color='red')
    anomalies = city_data[
        (city_data['temperature'] < city_data['temperature'].mean() - 2 * city_data['temperature'].std()) |
        (city_data['temperature'] > city_data['temperature'].mean() + 2 * city_data['temperature'].std())
        ]
    plt.scatter(anomalies['timestamp'], anomalies['temperature'], label='Аномалии', color='orange')
    plt.legend()
    plt.xlabel('Дата')
    plt.ylabel('Температура (°C)')
    plt.title(f"Временной ряд температур для города: {selected_city}")
    st.pyplot(plt)

    # Сезонная сводка
    st.write("### Сезонный профиль")
    season_data = city_data.groupby('season').agg({
        'temperature': ['mean', 'std']
    }).reset_index()
    st.write(season_data)

    # Подключение к OpenWeatherMap API
    st.sidebar.write("### OpenWeatherMap API")
    api_key = st.sidebar.text_input("Введите ваш ключ для OpenWeatherMap API")
    if api_key:
        response = fetch_current_temperature(selected_city, api_key)
        if "error" in response:
            st.sidebar.error(response["error"])
        else:
            current_temp = response["temp"]
            st.sidebar.write(f"Текущая температура в городе {selected_city}: {current_temp} °C")
            season = city_data.loc[city_data['timestamp'].dt.month == pd.Timestamp.now().month, 'season'].iloc[0]
            season_mean = season_data.loc[season_data['season'] == season, ('temperature', 'mean')].values[0]
            if current_temp > season_mean + 2 * city_data['temperature'].std() or \
                    current_temp < season_mean - 2 * city_data['temperature'].std():
                st.sidebar.write("Текущая температура является аномальной для данного сезона.")
            else:
                st.sidebar.write("Текущая температура в пределах нормы для данного сезона.")
