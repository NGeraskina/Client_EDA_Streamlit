import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np


@st.cache_data
def open_data(path="data/clients.csv"):
    df = pd.read_csv(path)
    df = df.drop(columns=['Unnamed: 0', 'ID_CLIENT'])
    return df


st.title('EDA проект Надежды Гераськиной')

'## Узнаем профиль типичного клиента банка'

df = open_data()

st.dataframe(df.describe(), use_container_width=True)
st.dataframe(df.describe(include='object'), use_container_width=True)

st.write('### Распределение клиентов')
col1, col2 = st.columns(2)

with col1:
    st.write('#### По полу')
    fig = px.histogram(df, x='GENDER', color='MARITAL_STATUS')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write('#### По возрасту')
    # fig = px.histogram(df, x='AGE', color = 'CNT_TARGET')
    # fig.add_annotation(x=60, y=410,
    #                    text=f"Среднее = {df.AGE.mean():0.1f}",
    #                    showarrow=False, )
    # fig.add_annotation(x=60, y=390,
    #                    text=f"Медиана = {df.AGE.median():0.1f}",
    #                    showarrow=False, )
    # st.plotly_chart(fig, use_container_width=True)
    # fig = sns.histplot(x="AGE", data=df, kde = True)
    # fig = px.box(df, y='AGE', x = 'CNT_TARGET')
    # fig.add_box(df, y='AGE')
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
    Мужчин почти в 2 раза больше женщин, в основном состоящие в браке (как и женщины в основном замужем)
    
    Возраст варьируется от 21 до 67 лет, медианный возраст клиента банка - 39 лет 
    
    Распределение тех, кто откликнулся на маркетинговую кампанию похоже на общее распределение, аномалий нет, но можно отметить, что люди, откликнувшиеся на кампанию, моложе
    
'''

'> Далее на графики выведу процент откликнувшихся на маркетинговую кампанию по различным срезам: CNT_TARGET = 1 - был отклик, CNT_TARGET = 0 - не было отклика'

'#### По образованию'
fig = px.histogram(df, x='EDUCATION', color='CNT_TARGET', category_orders={
    'EDUCATION': ['Неполное среднее', 'Среднее', 'Среднее специальное',
                  'Неоконченное высшее', 'Высшее', 'Два и более высших образования',
                  'Ученая степень']})

value_counts = df['EDUCATION'].value_counts().reset_index()
value_counts.columns = ['EDUCATION', 'count']

# Sort the DataFrame by count in ascending order
sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

grouped = df.groupby(['EDUCATION', 'CNT_TARGET']).count()[['GEN_INDUSTRY']].reset_index()
grouped = grouped.merge(df.groupby(['EDUCATION']).count()[['GEN_INDUSTRY']].reset_index(), on='EDUCATION')

grouped = grouped.sort_values(by='GEN_INDUSTRY_y', ascending=True)

grouped['TARGET_SHARE'] = (grouped['GEN_INDUSTRY_x'] / grouped['GEN_INDUSTRY_y']).round(2)
grouped['TARGET_SHARE'] = grouped['TARGET_SHARE'].apply(lambda x: f'{x:0.0%}')
grouped = grouped[grouped.CNT_TARGET == 1]
dict_edu = {'Неполное среднее':0, 'Среднее':1, 'Среднее специальное':2,
                  'Неоконченное высшее':3, 'Высшее':4, 'Два и более высших образования':5,
                  'Ученая степень':6}
grouped['sort'] = grouped['EDUCATION'].map(dict_edu)
grouped = grouped.sort_values(by='sort', ascending=True)
print(grouped)

fig.data[1].text = grouped['TARGET_SHARE']
fig.update_traces(textposition='outside', textfont_size=14)

st.plotly_chart(fig, use_container_width=True)

'Чаще кредиты берут люди без высшего образования'


'### В какой области работают клиенты банка'

value_counts = df['GEN_INDUSTRY'].value_counts().reset_index()
value_counts.columns = ['GEN_INDUSTRY', 'count']

# Sort the DataFrame by count in ascending order
sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

grouped = df.groupby(['GEN_INDUSTRY', 'CNT_TARGET']).count()[['EDUCATION']].reset_index()
grouped = grouped.merge(df.groupby(['GEN_INDUSTRY']).count()[['EDUCATION']].reset_index(), on='GEN_INDUSTRY')

grouped = grouped.sort_values(by='EDUCATION_y', ascending=True)

grouped['TARGET_SHARE'] = (grouped['EDUCATION_x'] / grouped['EDUCATION_y']).round(2)
grouped['TARGET_SHARE'] = grouped['TARGET_SHARE'].apply(lambda x: f'{x:0.0%}')
grouped = grouped[grouped.CNT_TARGET == 1]
grouped = grouped.sort_values(by='EDUCATION_y', ascending=False)

# Create a histogram using Plotly Express
fig = px.histogram(df, y='GEN_INDUSTRY', color='CNT_TARGET',
                   category_orders={'GEN_INDUSTRY': sorted_value_counts['GEN_INDUSTRY'].tolist()})
fig.data[1].text = grouped['TARGET_SHARE']
fig.update_traces(textposition='outside', textfont_size=14)
st.plotly_chart(fig, use_container_width=True)

'Больше всего людей, берущих кредит, работают в торговле'
'Это интересный инсайт, так как возможно они берут в кредит те товары, которыми потом торгуют'
'Также много клиентов работает на гос.службе или в мед. учреждениях, что может свидетельствовать о том, что их доходы не высоки (раз они берут кредиты), но их заработок стабилен, так как они с уверенностью могут закрыть кредит'
'Что касается отклика на маркетинговую компанию, то есть в целом распределение похоже на исходное (без раскраски по целевой переменной), откликнувшихся 10-15% во всех многочисленных категориях'

'### На каких должностях работают клиенты'
value_counts = df['GEN_TITLE'].value_counts().reset_index()
value_counts.columns = ['GEN_TITLE', 'count']

# Sort the DataFrame by count in ascending order
sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

# Create a histogram using Plotly Express
fig = px.histogram(df, y='GEN_TITLE', color='CNT_TARGET',
                   category_orders={'GEN_TITLE': sorted_value_counts['GEN_TITLE'].tolist()})
st.plotly_chart(fig, use_container_width=True)
'Напрашивается вывод, что чем ниже должность, тем больше люди берут кредиты, чтот логично, от должности напрямую зависит доход клиента и его потребность в кредита'

'### Распределение семейного дохода среди клиентов'

fig = px.histogram(df, x='FAMILY_INCOME', color='CNT_TARGET',
                   category_orders={'FAMILY_INCOME': ['до 5000 руб.', 'от 5000 до 10000 руб.',
                                                      'от 10000 до 20000 руб.', 'от 20000 до 50000 руб.',
                                                      'свыше 50000 руб.'
                                                      ]})

value_counts = df['FAMILY_INCOME'].value_counts().reset_index()
value_counts.columns = ['FAMILY_INCOME', 'count']

# Sort the DataFrame by count in ascending order
sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

grouped = df.groupby(['FAMILY_INCOME', 'CNT_TARGET']).count()[['GEN_INDUSTRY']].reset_index()
grouped = grouped.merge(df.groupby(['FAMILY_INCOME']).count()[['GEN_INDUSTRY']].reset_index(), on='FAMILY_INCOME')

grouped = grouped.sort_values(by='GEN_INDUSTRY_y', ascending=True)

grouped['TARGET_SHARE'] = (grouped['GEN_INDUSTRY_x'] / grouped['GEN_INDUSTRY_y']).round(2)
grouped['TARGET_SHARE'] = grouped['TARGET_SHARE'].apply(lambda x: f'{x:0.0%}')
grouped = grouped[grouped.CNT_TARGET == 1]
dict_edu = {'до 5000 руб.':0, 'от 5000 до 10000 руб.':1,
                                                      'от 10000 до 20000 руб.':2, 'от 20000 до 50000 руб.':3,
                                                      'свыше 50000 руб.':4}
grouped['sort'] = grouped['FAMILY_INCOME'].map(dict_edu)
grouped = grouped.sort_values(by='sort', ascending=True)
print(grouped)

fig.data[1].text = grouped['TARGET_SHARE']
fig.update_traces(textposition='outside', textfont_size=14)


st.plotly_chart(fig, use_container_width=True)

'Кредиты берут люди с доходом около уровня 1 МРОТ и выше до 2 МРОТ'
'Это также логично, ведь люди с таким доходом не могут позволить себе дорогостоящие покупки, поэтому берут кредит, а поскольку (см.выше) они работают в гос. учреждениях, то они способны ганатировано закрыть кредит'
'Люди с семейным доходом ниже МРОТ с меньшей вероятностью смогут выплатить кредит, поэтому и банк редко выдает им кредиты'
'Людям с семейным доходом выше 50к рублей кредиты редко нужны, чаще всего на что-то дорогостоящее (например, на машину)'

st.write('### Какая кредитная история у клиентов')
fig = px.histogram(df, x='CLOSED_LOANS', color='CNT_TARGET')
st.plotly_chart(fig, use_container_width=True)

'## Исследование связи признаков с целевой переменной (отклик на маркетинговую кампанию)'
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
    st.write('#### Вне зависимости от пола')
    fig = px.pie(df, 'CNT_TARGET')
    st.plotly_chart(fig, use_container_width=True)

'В среднем 12% людей откликнулось на маркетинговые предложения'
'Данные цифры подртверждаются графиками из первого раздела, не удалось выявить необычной зависимости таргета от категориальных признаков'
'В следующем разделе попробуем найтивзаимосвязи среди вещественных признаков'

'### Посмотрим процент клиентов по статусам'
col1, col2, col3 = st.columns(3)
with col1:
    st.write('#### Нахождение на пенсии')
    fig = px.histogram(df, 'status_pens', color = 'CNT_TARGET')

    grouped = df.groupby(['status_pens', 'CNT_TARGET']).count()['AGE'].reset_index()

    fig.data[1].text = [f"{grouped[(grouped.status_pens == 'не пенсионер')&(grouped.CNT_TARGET == 1)]['AGE'].sum()/grouped[(grouped.status_pens == 'не пенсионер')]['AGE'].sum():0.2%}",
                        f"{grouped[(grouped.status_pens == 'пенсионер') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_pens == 'пенсионер')]['AGE'].sum():0.2%}",
                        ]
    fig.update_traces(textposition='outside', textfont_size=14)
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.write('#### Трудоустроенность')
    fig = px.histogram(df, 'status_work', color = 'CNT_TARGET')
    grouped = df.groupby(['status_work', 'CNT_TARGET']).count()['AGE'].reset_index()

    fig.data[1].text = [
        f"{grouped[(grouped.status_work == 'работает') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_work == 'работает')]['AGE'].sum():0.2%}",
        f"{grouped[(grouped.status_work == 'не работает') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.status_work == 'не работает')]['AGE'].sum():0.2%}",
        ]
    fig.update_traces(textposition='outside', textfont_size=14)
    st.plotly_chart(fig, use_container_width=True)
with col3:
    st.write('#### Владение квартирой')
    fig = px.histogram(df, 'FL_PRESENCE_FL', color = 'CNT_TARGET')
    grouped = df.groupby(['FL_PRESENCE_FL', 'CNT_TARGET']).count()['AGE'].reset_index()

    fig.data[1].text = [
        f"{grouped[(grouped.FL_PRESENCE_FL == 'Есть') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.FL_PRESENCE_FL == 'Есть')]['AGE'].sum():0.2%}",
        f"{grouped[(grouped.FL_PRESENCE_FL == 'Нет') & (grouped.CNT_TARGET == 1)]['AGE'].sum() / grouped[(grouped.FL_PRESENCE_FL == 'Нет')]['AGE'].sum():0.2%}",
    ]
    fig.update_traces(textposition='outside', textfont_size=14)
    st.plotly_chart(fig, use_container_width=True)

f'Большинство клиентов не на пенсии и работают, работающих пенсионеров всего {df[(df.status_pens == "пенсионер") & (df.status_work == "работает")].shape[0]}'
'Квартирой владеет примерно 70% клиентов, так что кредит они берут скорее всего не на покупку квартиры'
'На маркетинговую кампанию значительно больше реагировали не пенсионеры и работающие клиенты, значительного отличия реакции на маркетинговую кампанию по признаку наличия квартиры не наблюдается'



'## Корреляция числовых признаков'

corr = df.corr(numeric_only=True)

# Use the built-in bool type instead of np.bool
color_scale = px.colors.diverging.RdYlBu
max_corr = max(corr.abs().max())
fig = px.imshow(corr, text_auto=True, color_continuous_scale=color_scale, zmin=-max_corr, zmax=max_corr, )
st.plotly_chart(fig, use_container_width=True)

'Более скоррелированные признаки это:'
'* Срок кредита и сумма кредита\n'
'* Сумма кредита и первый платеж\n'
'* Кол-во детей и кол-во иждивенцев\n'
'Все эти зависимости вполне логичны\n'
'Наблюдается несильная положительная связь дохода и суммы кредита, стоит проверить, почему корреляция всего 0.3 (кажется, что связь должна быть повыше)'
'Также любопытным является то, что возраст немного антикоррелирует с количеством иждивенцев, и немного коррелирует с количеством детей, когда кол-во детей и иждивенцев коррелируют (хоть и не сильно)'

'*Целевая переменная не коррелирует ни с одним числовым признаком*'

fig = px.scatter(df, x='PERSONAL_INCOME', y='CREDIT')
st.plotly_chart(fig, use_container_width=True)

'Видим, что люди с большим (очень даже) доходом брали кредит на (относительно дохода) небольшие суммы, а люди со средним доходом брали кредиты на суммы очень близкие к их доходу, отсюда и корреляция не больше 0.3'
'Введу новую метрику - доля суммы кредита в доходе клиента'

df['SHARE_CREDIT_IN_INCOME'] = df.CREDIT / df.PERSONAL_INCOME
fig = px.scatter(df, x='SHARE_CREDIT_IN_INCOME')
st.plotly_chart(fig, use_container_width=True)

# 'Видим, что у нас есть выброс, нельзя достоверно сказать, ошибка это или нет, может официально человек действительно получает так мало'
# 'Но для дальнейшего анализа этой метрики я удалю эту строку'
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
'Введем для этого метрика - сумма кредит / срок кредита'

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
