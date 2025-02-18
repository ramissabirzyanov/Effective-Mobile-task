FROM python:3.12

RUN pip install --no-cache-dir poetry

WORKDIR /app

ENV POETRY_VIRTUALENVS_CREATE=false 

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

CMD python manage.py migrate\
    && python manage.py runserver 0.0.0.0:8000
