run:
    python -m flask --app src/app.py run --port 3000

db-up:
    docker-compose up -d

db-down:
    docker-compose down

install:
    pip install -r requirements.txt