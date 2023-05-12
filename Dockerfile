FROM python:3.6.12-alpine3.12
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN crontab crontab
CMD ["crond", "-f"]