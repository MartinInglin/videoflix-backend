FROM python:3

WORKDIR /usr/src/app

COPY templates/ /usr/src/app/templates/
COPY requirements.txt ./

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "videoflix_backend.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]