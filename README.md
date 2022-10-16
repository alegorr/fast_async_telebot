# Build and run docker
`docker-compose build
docker-compose up -d`

# If adress already in use
`sudo ss -lptn 'sport = :5432'
sudo kill <pid>``

# Create migration and migrate db
`sudo docker-compose run web alembic revision --autogenerate -m "First migration"
sudo docker-compose run web alembic upgrade head`

# Drop all migrations
`sudo docker-compose run web alembic downgrade base`
`rm -rf alembic/versions`

# Check service and test api
https://ztest.online
https://ztest.online/docs

# Environment
TELEBOT_NAME=@DP1Testbot
TELEBOT_WEBHOOK_HOST=ztest.online
TELEBOT_WEBHOOK_PORT=443
TELEBOT_WEBHOOK_CERT=/root/ssl/cert.pem
TELEBOT_WEBHOOK_KEY=/root/ssl/key.pem
TELEBOT_API_TOKEN=5368353864:AAFbR9WPwj9j1Nvq0pnx6HDKwPEH0xjJ5-M
TELEBOT_KNOWN_SERVICES_NAMES=badlisted_words,spacy_nounphrases
TELEBOT_KNOWN_SERVICES_URLS=http://dream.deeppavlov.ai:8018/badlisted_words,http://dream.deeppavlov.ai:8006/respond
DATABASE_URL=postgresql://postgres:postgres@db:5432/postgres

# Test DP services
any fucks in this sentence, good one, fucked one
`curl -X POST -H "Content-Type: application/json" -d '{"sentences": ["any fucks in this sentence", "good one", "fucked one"]}' http://dream.deeppavlov.ai:8018/badlisted_words`
i like michal jordan, hey this is a white bear
`curl -X POST -H "Content-Type: application/json" -d '{"sentences": ["i like michal jordan", "hey this is a white bear"]}' http://dream.deeppavlov.ai:8006/respond`
