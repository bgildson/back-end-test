FROM python:3.7

RUN useradd -ms /bin/bash flask

USER flask

ENV PYTHONUNBUFFERED 1

WORKDIR /home/flask/app

ENV PATH $PATH:/home/flask/.local/bin

COPY poetry.lock pyproject.toml ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root
