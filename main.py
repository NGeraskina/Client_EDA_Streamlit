import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


@st.cache_data
def open_data(path="data/clients.csv"):
    df = pd.read_csv(path)
    df = df.drop(columns = ['Unnamed: 0', 'ID_CLIENT'])
    return df


st.title('EDA проект Надежды Гераськиной')

'## Узнаем профиль типичного клиента банка'


df = open_data()

st.dataframe(df.describe(), use_container_width=True)
st.dataframe(df.describe(include = 'object'), use_container_width=True)


st.write('Распределение клиентов')
col1, col2 = st.columns(2)

with col1:
    st.write('По полу')
    fig = px.histogram(df, x='GENDER', color='MARITAL_STATUS')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.write('По возрасту')
    # fig = plt.figure(figsize=(10, 4))
    fig = px.histogram(df, x='AGE', color = 'CNT_TARGET')
    fig.add_annotation(x=60, y=410,
                       text=f"Среднее = {df.AGE.mean():0.1f}",
                       showarrow=False, )
    fig.add_annotation(x=60, y=390,
                       text=f"Медиана = {df.AGE.median():0.1f}",
                       showarrow=False, )
    st.plotly_chart(fig, use_container_width=True)
    # fig = sns.histplot(x="AGE", data=df, kde = True)
    # st.pyplot(fig.plot)
'''
    Мужчин почти в 2 раза больше женщин, в основном состоящие в браке (как и женщины в основном замужем)
    
    Возраст варьируется от 21 до 65 лет, в среднем клиенты банка 40 летние 
    
    Распределение тех, кто откликнулся на маркетинговую капманию похоже на общее распределение, аномалий нет
    
'''

'По образованию'
fig = px.histogram(df, x='EDUCATION', color = 'CNT_TARGET', category_orders={
    'EDUCATION': ['Неполное среднее', 'Среднее', 'Среднее специальное',
                  'Неоконченное высшее', 'Высшее', 'Два и более высших образования',
                  'Ученая степень']})
st.plotly_chart(fig, use_container_width=True)

'Чаще кредиты берут люди без высшего образования'

'В какой области работают клиенты банка'
value_counts = df['GEN_INDUSTRY'].value_counts().reset_index()
value_counts.columns = ['GEN_INDUSTRY', 'count']

# Sort the DataFrame by count in ascending order
sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

grouped = df.groupby(['GEN_INDUSTRY', 'CNT_TARGET']).count()[['EDUCATION']].reset_index()
grouped = grouped.merge(df.groupby(['GEN_INDUSTRY']).count()[['EDUCATION']].reset_index(), on = 'GEN_INDUSTRY')

grouped = grouped.sort_values(by='EDUCATION_y', ascending=True)

grouped['TARGET_SHARE'] = (grouped['EDUCATION_x'] / grouped['EDUCATION_y']).round(2)
grouped['TARGET_SHARE'] = grouped['TARGET_SHARE'].apply(lambda x: f'{x:0.0%}')
grouped = grouped[grouped.CNT_TARGET == 1]
grouped = grouped.sort_values(by='EDUCATION_y', ascending=False)

# Create a histogram using Plotly Express
fig = px.histogram(df, y='GEN_INDUSTRY', color = 'CNT_TARGET', category_orders={'GEN_INDUSTRY': sorted_value_counts['GEN_INDUSTRY'].tolist()})
fig.data[1].text = grouped['TARGET_SHARE']
fig.update_traces(textposition='outside', textfont_size=14)
st.plotly_chart(fig, use_container_width=True)

'Больше всего людей, берущих кредит, работают в торговле'
'Это интересный инсайт, так как возможно они берут в кредит те товары, которыми потом торгуют'
'Также много клиентов работает на гос.службе или в мед. учреждениях, что может свидетельствовать о том, что их доходы не высоки (раз они берут кредиты), но их заработок стабилен, так как они с уверенностью могут закрыть кредит'
'Что касается отклика на маркетинговую компанию, то есть в целом распределение похоже на исходное (без раскраски по целевой переменной), откликнувшихся 10-15% во всех многочисленных категориях'

'На каких должностях работают клиенты'
value_counts = df['GEN_TITLE'].value_counts().reset_index()
value_counts.columns = ['GEN_TITLE', 'count']

# Sort the DataFrame by count in ascending order
sorted_value_counts = value_counts.sort_values(by='count', ascending=True)

# Create a histogram using Plotly Express
fig = px.histogram(df, y='GEN_TITLE', color = 'CNT_TARGET', category_orders={'GEN_TITLE': sorted_value_counts['GEN_TITLE'].tolist()})
st.plotly_chart(fig, use_container_width=True)
'Напрашивается вывод, что чем ниже должность, тем больше люди берут кредиты, чтот логично, от должность напрямую зависит доход клиента и его потребность в кредита'


'Распределение семейного дохода среди клиентов'

fig = px.histogram(df, x='FAMILY_INCOME', color = 'CNT_TARGET', category_orders={'FAMILY_INCOME': ['до 5000 руб.', 'от 5000 до 10000 руб.',
                                                                             'от 10000 до 20000 руб.','от 20000 до 50000 руб.',
                                                                             'свыше 50000 руб.'
                                                                             ]})
st.plotly_chart(fig, use_container_width=True)
'Кредиты берут люди с доходом около уровня МРОТ и выше до 2*МРОТ'
'Это также логично, ведь люди с таким доходом не могут позволить себе дорогостоящие покупки, поэтому берут кредит, а поскольку (см.выше) они работают в гос. учреждениях, то они способны ганатировано закрыть кредит'
'Люди с семейным доходом ниже МРОТ с меньшей вероятностью смогут выплатить кредит, поэтому и банк редко выдает им кредиты'
'Людям с семейным доходом выше 50к рублей кредиты редко нужны, чаще всего на что-то дорогостоящее (например, на машину)'


st.write('Какая кредитная история у клиентов')
fig = px.histogram(df, x='CLOSED_LOANS', color = 'CNT_TARGET')
st.plotly_chart(fig, use_container_width=True)



'## Исследование связи признаков с целевой переменной (отклик на маркетинговую кампанию)'
col1, col2, col3 = st.columns(3)
with col1:
    st.write('Мужчины')
    fig = px.pie(df[df.GENDER == 'Мужчина'], 'CNT_TARGET')
    st.plotly_chart(fig, use_container_width=True)
with col2:
    st.write('Женщины')
    fig = px.pie(df[df.GENDER == 'Женщина'], 'CNT_TARGET')
    st.plotly_chart(fig, use_container_width=True)
with col3:
    st.write('Вне зависимости от пола')
    fig = px.pie(df, 'CNT_TARGET')
    st.plotly_chart(fig, use_container_width=True)

'В среднем 12% людей откликнулось на маркетинговые предложения'
'Данные цифры подртверждаются графиками из первого раздела, не удалось выявить необычной зависимости таргета от категориальных признаков'
'В следующем разделе попробуем найтивзаимосвязи среди вещественных признаков'




'## Корреляция числовых признаков'

corr = df.corr(numeric_only=True)

# Use the built-in bool type instead of np.bool
color_scale = px.colors.diverging.RdYlBu
max_corr = max(corr.abs().max())
fig = px.imshow(corr, text_auto=True, color_continuous_scale=color_scale, zmin=-max_corr, zmax=max_corr,)
st.plotly_chart(fig, use_container_width=True)

'Более скоррелированные признаки это:'
'* Срок кредита и сумма кредита\n'
'* Сумма кредита и первый платеж\n'
'* Кол-во детей и кол-во иждивенцев\n'
'Все эти зависимости вполне логичны\n'
'Наблюдается несильная положительная связь дохода и суммы кредита, стоит проверить, почему корреляция всего 0.3 (кажется, что связь должна быть повыше)'
'Также любопытным является то, что возраст немного антикоррелирует с количеством иждивенцев, и немного коррелирует с количеством детей, когда кол-во детей и иждивенцев коррелируют (хоть и не сильно)'

'*Целевая переменная не коррелирует ни с одним числовым признаком*'

fig = px.scatter(df, x='PERSONAL_INCOME', y = 'CREDIT')
st.plotly_chart(fig, use_container_width=True)

'Видим, что люди с большим (очень даже) доходом брали кредит на (относительно дохода) небольшие суммы, а люди со средним доходом брали кредиты на суммы очень близкие к их доходу, отсюда и корреляция не больше 0.3'
'Введу новую метрику - доля суммы кредита в доходе клиента'


df['SHARE_CREDIT_IN_INCOME'] = df.CREDIT/df.PERSONAL_INCOME
fig = px.scatter(df, x='SHARE_CREDIT_IN_INCOME')
st.plotly_chart(fig, use_container_width=True)

'Видим, что у нас есть выброс, нельзя достоверно сказать, ошибка это или нет, может официально человек действительно получает так мало'
'Но для дальнейшего анализа этой метрики я удалю эту строку'
fig = px.histogram(df[df['SHARE_CREDIT_IN_INCOME'] < df['SHARE_CREDIT_IN_INCOME'].max()], x='SHARE_CREDIT_IN_INCOME')
fig.add_annotation(x=2, y=410,
                   text=f"Среднее = {df.SHARE_CREDIT_IN_INCOME.mean():0.1f}",
                   showarrow=False, )
fig.add_annotation(x=2, y=390,
                   text=f"Медиана = {df.SHARE_CREDIT_IN_INCOME.median():0.1f}",
                   showarrow=False, )
fig.add_vline(x = df.SHARE_CREDIT_IN_INCOME.mean())
st.plotly_chart(fig, use_container_width=True)

'Собственно, что и требовалось доказать: достаточно большая группа людей берет кредит на сумму в 2 и более раз превышающую их доход, отсюда и такая невысокая корреляция'
'*Данная метрика имеет распределение с тяжелым хвостом!*'


'Также интересно распределение суммы кредита на 1 год'
'Введем для этого метрика - сумма кредит / срок кредита'

df['CREDIT_IN_YEAR'] = df.CREDIT/df.TERM
fig = px.histogram(df, x='CREDIT_IN_YEAR')
fig.add_annotation(x=4600, y=410,
                   text=f"Среднее = {df.CREDIT_IN_YEAR.mean():0.1f}",
                   showarrow=False, )
fig.add_annotation(x=4600, y=380,
                   text=f"Медиана = {df.CREDIT_IN_YEAR.median():0.1f}",
                   showarrow=False, )
fig.add_vline(x = df.CREDIT_IN_YEAR.mean())
st.plotly_chart(fig, use_container_width=True)

'*Данная метрика также имеет распределение с тяжелым хвостом!*'
