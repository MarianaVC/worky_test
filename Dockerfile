FROM python:3.4
ENV PYTHONUNBUFFERED 1
RUN mkdir /config
ADD /config/requirements.pip /config/
RUN pip install -r /config/requirements.pip
RUN mkdir /src
CMD python manage.py collectstatic --no-input;python manage.py migrate; gunicorn --timeout 120 worky.wsgi -b 0.0.0.0:8000;

WORKDIR /src



