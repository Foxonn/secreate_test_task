FROM python:latest

EXPOSE 7555

RUN pip install pipenv

RUN python -m pip install --upgrade pip

RUN pip install pipenv

COPY app/ /app/

WORKDIR /app/

RUN pipenv install --deploy --system --ignore-pipfile
