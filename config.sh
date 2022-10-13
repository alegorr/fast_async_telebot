#!/bin/bash

echo "Configure deployment"
if [ -f "./config/Dockerfile" ]; then
  echo "-> Docker"
  mv requirements.txt config/heroku_requirements.txt
  mv config/docker_requirements.txt requirements.txt
  mv Procfile config/
  mv runtime.txt config/
  mv config/docker-compose.yml .
  mv config/Dockerfile .
else
  echo "-> Heroku"
  mv requirements.txt config/docker_requirements.txt
  mv config/heroku_requirements.txt requirements.txt
  mv config/Procfile .
  mv config/runtime.txt .
  mv docker-compose.yml config/
  mv Dockerfile config/
fi
