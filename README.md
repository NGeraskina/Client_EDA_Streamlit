# Streamlit EDA проект: исследование клиентов банка

Просмотр приложения [here](https://clienteda.streamlit.app/)!

## Файлы

- `main.py`: streamlit app file
- `data/clients.csv` and `model_weights.mw`: data file and pre-trained model
- `requirements.txt`: package requirements files
- 'db/data_preparation.py'
- 'db/insert_data_to_psgr.py'

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
