FROM python:3.11.8
LABEL authors="Vlad Tsaryk"
ENV PYTHONPATH "${PYTHONPATH}:/home/app/test_task"

WORKDIR $PYTHONPATH

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/usr/local/poetry python -
ENV PATH="${PATH}:/usr/local/poetry/bin"

WORKDIR /home/app/test_task
COPY . /home/app/test_task

RUN poetry config virtualenvs.create false
RUN poetry install
