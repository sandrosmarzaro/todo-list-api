FROM python:3.13
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app
COPY . .

RUN pip install poetry
RUN poetry config installer.max-workers 10
RUN poetry install --no-interaction --no-ansi --without dev

EXPOSE 8000

CMD ["uvicorn", "todo_list_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
