# Applied Python Homework 1 - Streamlit Weather dashboard with OpenWeather API

Описание задания:
Вы аналитик в компании, занимающейся изучением климатических изменений и мониторингом температур в разных городах. Вам нужно провести анализ исторических данных о температуре для выявления сезонных закономерностей и аномалий. Также необходимо подключить API OpenWeatherMap для получения текущей температуры в выбранных городах и сравнить её с историческими данными.

Цели задания:
Провести анализ временных рядов, включая:

Вычисление скользящего среднего и стандартного отклонения для сглаживания температурных колебаний.
Определение аномалий на основе отклонений температуры от  скользящее среднее±2σ .
Построение долгосрочных трендов изменения температуры.
Любые дополнительные исследования будут вам в плюс.
Осуществить мониторинг текущей температуры:

Получить текущую температуру через OpenWeatherMap API.
Сравнить её с историческим нормальным диапазоном для текущего сезона.
Разработать интерактивное приложение:

Дать пользователю возможность выбрать город.
Отобразить результаты анализа температур, включая временные ряды, сезонные профили и аномалии.
Провести анализ текущей температуры в контексте исторических данных.

## Files

- `app.py`: streamlit app file
- `temperature_data.csv` : data file with historical weather information
- `requirements.txt`: package requirements files
- `Dockerfile` for docker deployment

## Run Demo Locally 

### Shell

To directly run streamlit locally execute below commands in the repo root folder

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ streamlit run app.py
```
Open http://localhost:8501 to view the app.

### Docker

To build and run the docker image:

```
$ docker build -t homework1 .
$ docker run -it --rm -p '8501:8501' homework1
```

`-it` keeps the terminal interactive

`--rm` removes the image once the command is stopped (e.g. using control + c)

Open http://localhost:8501/ to view the app.

## Streamlit Cloud Deployment
 
1. Put your app on GitHub (like this repo)
Make sure it's in a public folder and that you have a `requirements.txt` file.
 
2. Sign into Streamlit Cloud
Sign into share.streamlit.io with your GitHub email address, you need to have access to Streamlit Cloud service.
 
3. Deploy and share!  
Click "New app", then fill in your repo, branch, and file path, choose a Python version (3.9 for this demo) and click "Deploy", then you should be able to see your app.