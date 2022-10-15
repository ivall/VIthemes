
FROM python:3.7-alpine

RUN mkdir -p /opt/services/vithemes/src
WORKDIR /opt/services/vithemes/src

COPY requirements.txt /opt/services/vithemes/src/
RUN pip install -r requirements.txt

COPY /home/ubuntu/vithemes/vithemes /opt/services/vithemes/src
RUN python manage.py migrate

EXPOSE 80

CMD ["gunicorn", "--chdir", ".", "--bind", ":80", "vithemes.wsgi:application"]