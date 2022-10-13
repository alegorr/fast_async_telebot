# build and run docker
docker-compose build
docker-compose up

# create migration and migrate db
sudo docker-compose run web alembic revision --autogenerate -m "First migration"
sudo docker-compose run web alembic upgrade head

# drop all migrations
sudo docker-compose run web alembic downgrade base
rm -rf alembic/versions

# check service and test api
http://localhost:8000/
http://localhost:8000/docs
