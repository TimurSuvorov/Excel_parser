import sqlite3
from random import randrange

import numpy as np
import pandas as pd
from django.conf import settings
from django.core.exceptions import ValidationError


def excel_parser(uploaded_file) -> pd.DataFrame:
    # Считываем файл и заполняем merged nan ячейки
    df = pd.read_excel(uploaded_file, header=None).fillna(method='ffill', axis=1)
    # Необходимо сделать новые заголовки из 3 первых строк
    df_top_3 = df.head(3)
    new_header = []
    for n_col, data_in_col in df_top_3.items():
        new_col_name = '_'.join(str(cell) for cell in data_in_col if str(cell) != 'nan')
        new_header.append(new_col_name)
    # Добавление нового заголовка в dataframe
    df.columns = new_header
    # Проверка соответствия эталоны
    if new_header != ['id',
                      'company',
                      'fact_Qliq_data1', 'fact_Qliq_data2',
                      'fact_Qoil_data1', 'fact_Qoil_data2',
                      'forecast_Qliq_data1', 'forecast_Qliq_data2',
                      'forecast_Qoil_data1', 'forecast_Qoil_data2']:
        raise ValidationError(message='Ошибка: несоответствие формата содержимого')

    # Удаление первых трёх строк и столбца с 'id'
    df = df.drop([0, 1, 2], axis=0).drop('id', axis=1)
    # Сброс индекса
    df = df.reset_index(drop=True)
    return df


def write_to_db(df: pd.DataFrame) -> None:
    conn = sqlite3.connect(settings.BASE_DIR / 'db.sqlite3')
    df.to_sql('Company', conn, if_exists='append', index=False)
    conn.commit()
    conn.close()


def make_pivot_with_date(df) -> pd.DataFrame:
    # Генерируем случайные даты в узком диапазоне для наглядной агрегации
    df['createddate'] = df.apply(lambda x: str(randrange(20, 30)).zfill(2) + '.03.2023', axis=1)
    # Добавляем новые метрики
    df_new = df.assign(fact_Qliq=df['fact_Qliq_data1'] + df['fact_Qliq_data2'],
                       fact_Qoil=df['fact_Qoil_data1'] + df['fact_Qoil_data2'],
                       forecast_Qliq=df['forecast_Qliq_data1'] + df['forecast_Qliq_data2'],
                       forecast_Qoil=df['forecast_Qoil_data1'] + df['forecast_Qoil_data2']
                       )
    df_pivoted = pd.pivot_table(df_new,
                                index='createddate',
                                values=['fact_Qliq_data1', 'fact_Qliq_data2',
                                        'fact_Qoil_data1', 'fact_Qoil_data2',
                                        'forecast_Qliq_data1', 'forecast_Qliq_data2',
                                        'forecast_Qoil_data1', 'forecast_Qoil_data2',
                                        'fact_Qliq', 'fact_Qoil',
                                        'forecast_Qliq', 'forecast_Qoil'
                                        ],
                                aggfunc=np.sum,
                                margins=True,
                                margins_name='Total',
                                )
    return df_pivoted