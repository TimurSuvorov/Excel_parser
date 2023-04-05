import os.path

from django.core.exceptions import ValidationError
from django.shortcuts import render
from .utils import excel_parser, write_to_db, make_pivot_with_date


def upload_parse(request):
    context: dict = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['uploaded_file']
        # Проверка расширения файла
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension not in ['.xls', '.xlsx']:
            return render(request, 'ursip_parser/upload_page.html', {'error_message': 'Формат файла должен быть .xls, .xlsx'})

        try:
            parsed_df = excel_parser(uploaded_file)  # Парсим данные и оперируем далее с df
            write_to_db(parsed_df)  # Записываем df в БД
        except (ValueError, ValidationError) as err:
            return render(request, 'ursip_parser/upload_page.html', {'error_message': err})

        pivoted_df = make_pivot_with_date(parsed_df)  # Добавляем случайные даты к исходному и делаем агрегации

        parsed_html = parsed_df.to_html()  # Форматирование распарсенного df с датами в html для рендеринга
        pivoted_html = pivoted_df.to_html()  # Форматирование агрегированого df в html для рендеринга

        context = {'parsed_html': parsed_html,
                   'pivoted_html': pivoted_html}
    return render(request, 'ursip_parser/upload_page.html', context)
