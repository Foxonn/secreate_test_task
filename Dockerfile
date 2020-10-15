FROM python:latest

VOLUME /app /app

WORKDIR app

EXPOSE 7550

RUN pip install pipenv

RUN python -m pip install --upgrade pip

RUN pip install pipenv

RUN pipenv install --deploy --system --ignore-pipfile

CMD bash