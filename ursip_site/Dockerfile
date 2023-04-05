FROM python
MAINTAINER Suvorov Timur

# set work directory
WORKDIR /ursip_site/

# set app-environment variables
ENV PYTHONDONTWRITEBYTECODE 1  # Prevents Python from writing pyc files to disc
ENV PYTHONUNBUFFERED 1  #Prevents Python from buffering stdout and stderr.

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /ursip_site/requirements.txt
RUN chmod +x /ursip_site/requirements.txt
RUN pip install -r requirements.txt

EXPOSE 8000

COPY . /ursip_site/

CMD ["python", "./manage.py", "runserver", "0.0.0.0:8000"]