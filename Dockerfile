FROM python:3.13

WORKDIR /src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

EXPOSE 8000

RUN useradd -m semantic_search_user

USER semantic_search_user

CMD ["uvicorn", "semantic_search.api.base:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]