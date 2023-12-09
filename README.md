# Streamlit EDA проект: исследование клиентов банка

Просмотр приложения [здесь](https://clienteda.streamlit.app/)!

Postgres БД находится на [neon.tech](https://neon.tech/)

## Файлы

- `main.py`: приложение streamlit 
- `requirements.txt`: requirements для скачивания
- `postgres/insert_data_to_psgr.py` - загрузка таблиц в Postgres базу данных
- `data/clients.csv`: предобработанный датасет
- `data/prepare_data.ipynb`: предобработка данных для создания финального датасета

## Запуск приложения локально 

### Консоль

Для запуска streamlit локально в репозитории сделайте следующие команды

```shell
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ streamlit run app.py
```
Приложение заработает на http://localhost:8501
