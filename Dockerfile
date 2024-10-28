FROM python:3.11

RUN useradd -ms /bin/bash appuser

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

USER appuser

WORKDIR /app/social_api

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
