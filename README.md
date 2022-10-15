# Build and run docker
docker-compose build
docker-compose up -d

# If adress already in use
sudo ss -lptn 'sport = :5432'
sudo kill <pid>

# Create migration and migrate db
sudo docker-compose run web alembic revision --autogenerate -m "First migration"
sudo docker-compose run web alembic upgrade head

# Drop all migrations
sudo docker-compose run web alembic downgrade base
rm -rf alembic/versions

# Check service and test api
http://localhost:8000/
http://localhost:8000/docs

# Environment
TELEBOT_ALLOWED_HOSTS is allowed hosts URLs or IPs for deployment
TELEBOT_WEBHOOK_HOST is domain of deploy server url
TELEBOT_API_TOKEN is Telegram API Token from the @BotFather
TELEBOT_KNOWN_SERVICES are urls of deeppavlov.ai services
TELEBOT_KNOWN_SERVICES_NAMES are services names
DATABASE_URL is remote or local postres database url

# Example
TELEBOT_ALLOWED_HOSTS=0.0.0.0,127.0.0.1,localhost
TELEBOT_WEBHOOK_HOST=deeppavlov2.herokuapp.com
TELEBOT_API_TOKEN=5781893081:AAHfbx1v2m-v4cA_6XLh4IbbJox6cVqzExM
TELEBOT_KNOWN_SERVICES=http://dream.deeppavlov.ai:8018/badlisted_words,http://dream.deeppavlov.ai:8006/respond
TELEBOT_KNOWN_SERVICES_NAMES=badlisted_words,spacy_nounphrases
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres
