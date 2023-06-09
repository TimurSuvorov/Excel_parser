import os.path

import pandas as pd
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from .utils import excel_parser, write_to_db, make_pivot_with_date
from .models import Company


def upload_parse(request):
    context: dict = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['uploaded_file']
        # Проверка расширения файла
        file_extension: str = os.path.splitext(uploaded_file.name)[1]
        if file_extension not in ['.xls', '.xlsx']:
            return render(request, 'ursip_parser/upload_page.html', {'error_message': 'Формат файла должен быть .xls, .xlsx'})
        try:
            parsed_df: pd.DataFrame = excel_parser(uploaded_file)  # Парсим данные и оперируем далее с df
            write_to_db(parsed_df)  # Записываем df в БД
        except (ValueError, ValidationError) as err:
            return render(request, 'ursip_parser/upload_page.html', {'error_message': err})

        pivoted_df = make_pivot_with_date(parsed_df)  # Добавляем случайные даты к исходному и делаем агрегации

        parsed_html = parsed_df.to_html()  # Форматирование распарсенного df с датами в html для рендеринга
        pivoted_html = pivoted_df.to_html()  # Форматирование агрегированого df в html для рендеринга

        context = {'parsed_html': parsed_html,
                   'pivoted_html': pivoted_html}
    return render(request, 'ursip_parser/upload_page.html', context)


def show_db(request):
    db_data = Company.objects.all()
    if db_data:
        try:
            db_df = pd.DataFrame.from_records(db_data.values())
            db_df = db_df.drop('id', axis=1)
            pivoted_db_df = make_pivot_with_date(db_df)

            parsed_db_html = db_df.to_html()
            pivoted_db_html = pivoted_db_df.to_html()

            context = {'parsed_db_html': parsed_db_html,
                       'pivoted_db_html': pivoted_db_html}
            return render(request, 'ursip_parser/db_data_page.html', context)
        except Exception as err:
            return render(request, 'ursip_parser/db_data_page.html', {'error_message': err})
    else:
        context = {'info_message': 'Данные в БД отсутствуют'}
        return render(request, 'ursip_parser/db_data_page.html', context)


def clear_db(request):
    Company.objects.all().delete()
    return HttpResponseRedirect(reverse_lazy('show_db'))
