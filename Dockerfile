FROM python:3.11

RUN pip install "poetry==1.3.2"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn", "--host", "0.0.0.0", "app.main:app"]