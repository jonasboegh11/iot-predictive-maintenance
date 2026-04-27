FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["python", "-m", "flask", "--app", "src/app.py", "run", "--host=0.0.0.0", "--port=3000"]