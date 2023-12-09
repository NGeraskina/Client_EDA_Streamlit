import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


@st.cache_data
def open_data(path="data/clients.csv"):
    df = pd.read_csv(path)
    df = df.drop(columns=['Unnamed: 0', 'ID_CLIENT'])
    return df


def perc_of_target(df, param_group: str, counted: str):
    value_counts = df[param_group].value_counts().reset_index()
    value_counts.columns = [param_group, 'count']

    sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

    grouped = df.groupby([param_group, 'CNT_TARGET']).count()[[counted]].reset_index()
    grouped = grouped.merge(df.groupby([param_group]).count()[[counted]].reset_index(), on=param_group)

    grouped = grouped.sort_values(by=f'{counted}_y', ascending=True)

    grouped['TARGET_SHARE'] = (grouped[f'{counted}_x'] / grouped[f'{counted}_y']).round(2)
    grouped['TARGET_SHARE'] = grouped['TARGET_SHARE'].apply(lambda x: f'{x:0.0%}')
    grouped = grouped[grouped.CNT_TARGET == 1]
    return grouped, sorted_value_counts


def client_info(df):
    st.write('## Узнаем профиль типичного клиента банка')

    st.dataframe(df.describe(), use_container_width=True)

    'Сумма кредита варьируется от 2к до 120к рублей, срок от 3 месяцев до 3 лет - значит клиенты банка берут только *потребительские кредиты*'

    st.dataframe(df.describe(include='object'), use_container_width=True)

    st.write('### Распределение клиентов')
    col1, col2 = st.columns(2)

    with col1:
        st.write('#### По полу')
        fig = px.histogram(df, x='GENDER', color='MARITAL_STATUS')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write('#### По возрасту')
        fig = go.Figure()
        fig.add_trace(go.Box(y=df[df.CNT_TARGET == 0]['AGE'], name='Реакции нет',
                             ))
        fig.add_trace(go.Box(y=df[df.CNT_TARGET == 1]['AGE'], name='Реакция есть',
                             ))
        fig.add_trace(go.Box(y=df['AGE'], name='Всего',
                             ))
        fig.update_layout(xaxis_title="Реакция на маркетинговую рассылку",
                          yaxis_title="AGE", )
        st.plotly_chart(fig, use_container_width=True)
    '''
        Мужчин почти в 2 раза больше женщин, в основном они состоят в браке (как и женщины в основном замужем)
        
        Возраст варьируется от 21 до 67 лет, медианный возраст клиента банка - 39 лет 
        
        Распределение тех, кто откликнулся на маркетинговую кампанию похоже на общее распределение, аномалий нет, но можно отметить, что *люди, откликнувшиеся на кампанию, моложе*
        
    '''

    '> Далее на графики выведу процент откликнувшихся на маркетинговую кампанию по различным срезам: CNT_TARGET = 1 - был отклик, CNT_TARGET = 0 - не было отклика'

    '#### По образованию'
    fig = px.histogram(df, x='EDUCATION', color='CNT_TARGET', category_orders={
        'EDUCATION': ['Неполное среднее', 'Среднее', 'Среднее специальное',
                      'Неоконченное высшее', 'Высшее', 'Два и более высших образования',
                      'Ученая степень']})

    grouped, sorted_value_counts = perc_of_target(df, 'EDUCATION', 'GEN_INDUSTRY')
    dict_edu = {'Неполное среднее': 0, 'Среднее': 1, 'Среднее специальное': 2,
                'Неоконченное высшее': 3, 'Высшее': 4, 'Два и более высших образования': 5,
                'Ученая степень': 6}
    grouped['sort'] = grouped['EDUCATION'].map(dict_edu)
    grouped = grouped.sort_values(by='sort', ascending=True)

    fig.data[1].text = grouped['TARGET_SHARE']
    fig.update_traces(textposition='outside', textfont_size=14)

    st.plotly_chart(fig, use_container_width=True)

    'Чаще кредиты берут люди без высшего образования'

    '### В какой области работают клиенты банка'

    grouped, sorted_value_counts = perc_of_target(df, 'GEN_INDUSTRY', 'EDUCATION')
    grouped = grouped.sort_values(by='EDUCATION_y', ascending=False)

    # Create a histogram using Plotly Express
    fig = px.histogram(df, y='GEN_INDUSTRY', color='CNT_TARGET',
                       category_orders={'GEN_INDUSTRY': sorted_value_counts['GEN_INDUSTRY'].tolist()})
    fig.data[1].text = grouped['TARGET_SHARE']
    fig.update_traces(textposition='outside', textfont_size=14)
    st.plotly_chart(fig, use_container_width=True)

    'Больше всего людей, берущих кредит, работают в торговле'
    'Это интересный инсайт, так как возможно они берут в кредит те товары, которыми потом торгуют'
    'Также много клиентов работает на гос.службе или в мед. учреждениях, что может свидетельствовать о том, что их доходы не высоки (раз они берут кредиты), но их заработок стабилен, поэтому они с уверенностью могут закрыть кредит'
    'Что касается отклика на маркетинговую компанию, то в целом распределение похоже на исходное (без раскраски по целевой переменной), откликнувшихся 10-15% во всех многочисленных категориях'

    '### На каких должностях работают клиенты'
    value_counts = df['GEN_TITLE'].value_counts().reset_index()
    value_counts.columns = ['GEN_TITLE', 'count']

    # Sort the DataFrame by count in ascending order
    sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

    # Create a histogram using Plotly Express
    fig = px.histogram(df, y='GEN_TITLE', color='CNT_TARGET',
                       category_orders={'GEN_TITLE': sorted_value_counts['GEN_TITLE'].tolist()})
    st.plotly_chart(fig, use_container_width=True)
    'Напрашивается вывод, что чем ниже должность, тем больше люди берут кредиты, что логично, от должности напрямую зависит доход клиента и его потребность в кредита'

    '### Как долго клиенты работают на текущем месте'
    col1, col2 = st.columns(2)
    with col1:
        fig = px.scatter(df, x='WORK_TIME')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        value_counts = df['WORK_TIME'].value_counts().reset_index()
        value_counts.columns = ['WORK_TIME', 'count']

        # sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

        fig = px.histogram(df, x='WORK_TIME', color = 'CNT_TARGET')
        st.plotly_chart(fig, use_container_width=True)
    'Видим выбросы, но нельзя однозачно сказать, что эти люди не могут так долго работать на текущем месте, вполне возможно, что они работают всю жизнь в одном месте'
    'Закон распределения поход на экспоненциальный - большинство работает мало времени на текущем месте работы, есть длинный хвост состоящий из сторожил на рабочем месте'
    '*Интересный факт*: большинство людей стали клиентами банка менее чем через месяц после трудоустройства'


    '### Распределение семейного дохода среди клиентов'

    fig = px.histogram(df, x='FAMILY_INCOME', color='CNT_TARGET',
                       category_orders={'FAMILY_INCOME': ['до 5000 руб.', 'от 5000 до 10000 руб.',
                                                          'от 10000 до 20000 руб.', 'от 20000 до 50000 руб.',
                                                          'свыше 50000 руб.'
                                                          ]})

    grouped, sorted_value_counts = perc_of_target(df, 'FAMILY_INCOME', 'GEN_INDUSTRY')
    dict_edu = {'до 5000 руб.': 0, 'от 5000 до 10000 руб.': 1,
                'от 10000 до 20000 руб.': 2, 'от 20000 до 50000 руб.': 3,
                'свыше 50000 руб.': 4}
    grouped['sort'] = grouped['FAMILY_INCOME'].map(dict_edu)
    grouped = grouped.sort_values(by='sort', ascending=True)

    fig.data[1].text = grouped['TARGET_SHARE']
    fig.update_traces(textposition='outside', textfont_size=14)

    st.plotly_chart(fig, use_container_width=True)

    'Кредиты берут люди с доходом около уровня 1 МРОТ до 2 МРОТ'
    'Это закономерно, ведь люди с таким доходом не могут позволить себе дорогостоящие покупки, поэтому берут кредит, а поскольку (см.выше) они работают в гос. учреждениях, то они способны гарантировано закрыть кредит'
    'Люди с семейным доходом ниже МРОТ с меньшей вероятностью смогут выплатить кредит, поэтому и банк редко выдает им кредиты'
    'Людям с семейным доходом выше 50к рублей кредиты редко нужны, чаще всего на что-то дорогостоящее (например, на телевизор), судя по максимальной сумме кредита (см. табл. в начале) необходимое до получения зарплаты'

    st.write('### Кредитная история клиентов')
    col1, col2 = st.columns(2)
    with col1:
        '#### Общее кол-во кредитов'
        fig = px.histogram(df, x='CNT_LOANS', color='CNT_TARGET')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        '#### Кол-во закрытых кредитов'
        fig = px.histogram(df, x='CLOSED_LOANS', color='CNT_TARGET')
        st.plotly_chart(fig, use_container_width=True)

    'Большинство клиентов не имеют закрытых кредитов при этом чаще всего у них в банке всего 1 кредит, отклик на маркетинговую рассылку не зависит от кредитной истории'

    f'Кол-во клиентов, которые имеют более 1 незакрытого кредита одновременно: {df[(df.CNT_LOANS - df.CLOSED_LOANS)>=2].shape[0]}'
    'Таковых должников около 1-2% от всех клиентов'


def target_corr(df):

    st.write('## Исследование связи признаков с целевой переменной')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write('#### Мужчины')
        fig = px.pie(df[df.GENDER == 'Мужчина'], 'CNT_TARGET')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write('#### Женщины')
        fig = px.pie(df[df.GENDER == 'Женщина'], 'CNT_TARGET')
        st.plotly_chart(fig, use_container_width=True)
    with col3:
        st.write('#### Всего')
        fig = px.pie(df, 'CNT_TARGET')
        st.plotly_chart(fig, use_container_width=True)

    'В среднем 12% людей откликнулось на маркетинговые предложения'
    'Данные цифры подтверждаются графиками из первого раздела'

    '### Процент клиентов по статусам и взаимосвязь с откликом на маркетинговую кампанию'
    col1, col2 = st.columns(2)
    with col1:
        st.write('#### Нахождение на пенсии')
        fig = px.histogram(df, 'status_pens', color='CNT_TARGET')

        grouped = df.groupby(['status_pens', 'CNT_TARGET']).count()['AGE'].reset_index()

        fig.data[1].text = [
            f"{grouped[(grouped.status_pens == 'не пенсионер') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_pens == 'не пенсионер')]['AGE'].sum():0.2%}",
            f"{grouped[(grouped.status_pens == 'пенсионер') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_pens == 'пенсионер')]['AGE'].sum():0.2%}",
        ]
        fig.update_traces(textposition='outside', textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.write('#### Трудоустроенность')
        fig = px.histogram(df, 'status_work', color='CNT_TARGET')
        grouped = df.groupby(['status_work', 'CNT_TARGET']).count()['AGE'].reset_index()

        fig.data[1].text = [
            f"{grouped[(grouped.status_work == 'работает') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_work == 'работает')]['AGE'].sum():0.2%}",
            f"{grouped[(grouped.status_work == 'не работает') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_work == 'не работает')]['AGE'].sum():0.2%}",
        ]
        fig.update_traces(textposition='outside', textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    f'Большинство клиентов не на пенсии и работают, работающих пенсионеров всего {df[(df.status_pens == "пенсионер") & (df.status_work == "работает")].shape[0]}'

    col1, col2 = st.columns(2)
    with col1:
        st.write('#### Владение квартирой')
        fig = px.histogram(df, 'FL_PRESENCE_FL', color='CNT_TARGET')
        grouped = df.groupby(['FL_PRESENCE_FL', 'CNT_TARGET']).count()['AGE'].reset_index()

        fig.data[1].text = [
            f"{grouped[(grouped.FL_PRESENCE_FL == 'Есть') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.FL_PRESENCE_FL == 'Есть')]['AGE'].sum():0.2%}",
            f"{grouped[(grouped.FL_PRESENCE_FL == 'Нет') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.FL_PRESENCE_FL == 'Нет')]['AGE'].sum():0.2%}",
        ]
        fig.update_traces(textposition='outside', textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.write('#### Владение автомобилем')
        fig = px.histogram(df, 'OWN_AUTO', color='CNT_TARGET')
        grouped = df.groupby(['OWN_AUTO', 'CNT_TARGET']).count()['AGE'].reset_index()

        fig.data[1].text = [
            f"{grouped[(grouped.OWN_AUTO == 0) & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.OWN_AUTO == 0)]['AGE'].sum():0.2%}",
            f"{grouped[(grouped.OWN_AUTO == 1) & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.OWN_AUTO == 1)]['AGE'].sum():0.2%}",
            f"{grouped[(grouped.OWN_AUTO == 2) & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.OWN_AUTO == 2)]['AGE'].sum():0.2%}",
        ]
        fig.update_traces(textposition='outside', textfont_size=14)
        st.plotly_chart(fig, use_container_width=True)


    'Квартирой владеет почти 50% клиентов, так что кредит они берут скорее всего на технику/мебель необходимую для квартиры'
    'Наличие машины не влияет на отклик на маркетинговую кампанию'
    '**Вывод:** На маркетинговую кампанию значительно больше реагировали не пенсионеры и работающие клиенты, значительного отличия реакции на маркетинговую кампанию по признаку наличия квартиры не наблюдается'


def num_features(df):
    st.write('## Корреляция числовых признаков')

    corr = df.corr(numeric_only=True)

    # Use the built-in bool type instead of np.bool
    color_scale = px.colors.diverging.RdYlBu
    max_corr = max(corr.abs().max())
    fig = px.imshow(corr, text_auto=True, color_continuous_scale=color_scale, zmin=-max_corr, zmax=max_corr, )
    st.plotly_chart(fig, use_container_width=True)

    'Более скоррелированные признаки:'
    '* Срок кредита и сумма кредита\n'
    '* Сумма кредита и первый платеж\n'
    '* Кол-во детей и кол-во иждивенцев\n'
    'Все эти зависимости вполне логичны\n'
    'Наблюдается несильная положительная связь дохода и суммы кредита, стоит проверить, почему корреляция всего 0.3 (кажется, что связь должна быть повыше)'
    'Также любопытным является то, что возраст немного антикоррелирует с количеством иждивенцев, и немного коррелирует с количеством детей, когда кол-во детей и иждивенцев коррелируют (хоть и не сильно)'

    '*Целевая переменная не коррелирует ни с одним числовым признаком*'

    '### Зависимость дохода и суммы кредита'
    fig = px.scatter(df, x='PERSONAL_INCOME', y='CREDIT')
    st.plotly_chart(fig, use_container_width=True)

    'Видим, что люди с большим (очень даже) доходом брали кредит на небольшие суммы (относительно дохода), а люди со средним доходом брали кредиты на суммы очень близкие к их доходу, отсюда и корреляция не больше 0.3'
    'Введу *новую метрику* - доля суммы кредита в доходе клиента'

    '### Доля суммы кредита в доходе клиента '
    df['SHARE_CREDIT_IN_INCOME'] = df.CREDIT / df.PERSONAL_INCOME
    fig = px.scatter(df, x='SHARE_CREDIT_IN_INCOME')
    st.plotly_chart(fig, use_container_width=True)

    fig = px.histogram(df, x='SHARE_CREDIT_IN_INCOME')
    fig.add_annotation(x=2, y=410,
                       text=f"Среднее = {df.SHARE_CREDIT_IN_INCOME.mean():0.1f}",
                       showarrow=False, )
    fig.add_annotation(x=2, y=390,
                       text=f"Медиана = {df.SHARE_CREDIT_IN_INCOME.median():0.1f}",
                       showarrow=False, )
    fig.add_vline(x=df.SHARE_CREDIT_IN_INCOME.mean())
    st.plotly_chart(fig, use_container_width=True)

    'Собственно, что и требовалось доказать: достаточно большая группа людей берет кредит на сумму в 2 и более раз превышающую их доход, отсюда и такая невысокая корреляция'
    '*Данная метрика имеет распределение с тяжелым хвостом!*'

    'Также интересно распределение суммы кредита на 1 год'
    'Введем для этого метрику - сумма кредит на 1 месяц'

    '### Сумма кредита на 1 месяц'
    df['CREDIT_IN_YEAR'] = df.CREDIT / df.TERM
    fig = px.histogram(df, x='CREDIT_IN_YEAR')
    fig.add_annotation(x=4600, y=410,
                       text=f"Среднее = {df.CREDIT_IN_YEAR.mean():0.1f}",
                       showarrow=False, )
    fig.add_annotation(x=4600, y=380,
                       text=f"Медиана = {df.CREDIT_IN_YEAR.median():0.1f}",
                       showarrow=False, )
    fig.add_vline(x=df.CREDIT_IN_YEAR.mean())
    st.plotly_chart(fig, use_container_width=True)

    '*Данная метрика также имеет распределение с тяжелым хвостом!*'

    'Таким образом, клиенты могут брать кредит на большую сумму и на маленький срок (в месяцах), отсюда и тяжелый хвост в распределении'


if __name__ == '__main__':
    st.title('EDA проект: исследование клиентов банка')
    'Создатель: Надежда Гераськина, МОВС-2023'
    df = open_data()

    '**Цель проекта:** исследования основные зависимости в данных клиентов банка'

    '**Основные термины в проекте:**'
    with st.expander("Признаки клиентов"):
        """
        - AGE	— возраст клиента;
        - GENDER — пол клиента;
        - EDUCATION — образование;
        - MARITAL_STATUS — семейное положение;
        - CHILD_TOTAL	— количество детей клиента;
        - DEPENDANTS — количество иждивенцев клиента;
        - status_work	— социальный статус клиента относительно работы;
        - status_pens	— социальный статус клиента относительно пенсии;
        - REG_ADDRESS_PROVINCE — область регистрации клиента;
        - FACT_ADDRESS_PROVINCE — область фактического пребывания клиента;
        - POSTAL_ADDRESS_PROVINCE — почтовый адрес области;
        - FL_PRESENCE_FL — наличие в собственности квартиры (1 — есть, 0 — нет);
        - OWN_AUTO — количество автомобилей в собственности
        - GEN_INDUSTRY — отрасль работы клиента;
        - GEN_TITLE — должность;
        - JOB_DIR — направление деятельности внутри компании;
        - WORK_TIME — время работы на текущем месте (в месяцах);
        - FAMILY_INCOME — семейный доход (несколько категорий);
        - PERSONAL_INCOME — личный доход клиента (в рублях);
        - CREDIT — сумма последнего кредита клиента (в рублях);
        - TERM — срок кредита;
        - FST_PAYMENT — первоначальный взнос (в рублях);
        - CNT_LOANS - кол-во взятых кредитов;
        - LOANS_CLOSED - кол-во закрытых кредитов.
        
        """

    with st.expander("Целевая переменная"):
        '''
        CNT_TARGET - отклик на маркетинговую кампанию
        - 1 - отклик был
        - 0 - отклика не было
        '''
    'Метрика - показатель, не имеющий отношение к настоящей математической метрике'

    tab1, tab2, tab3 = st.tabs(["Общая инфо о клиентах", "Связь с целевой переменной", 'Корреляция вещественных признаков'])
    with tab1:
        client_info(df)
    with tab2:
        target_corr(df)
    with tab3:
        num_features(df)
