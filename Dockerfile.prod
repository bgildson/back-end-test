FROM python:3.7-slim-stretch

RUN useradd -ms /bin/bash flask

ENV PYTHONUNBUFFERED 1
ENV WORKERS 5
ENV PORT 5000
ENV FLASK_ENV production

WORKDIR /home/flask/app

ENV PATH $PATH:/home/flask/.local/bin

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

COPY . .

EXPOSE 5000

CMD gunicorn -w $WORKERS -b 0.0.0.0:$PORT 'app:create_app()'
