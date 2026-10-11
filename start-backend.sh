#!/bin/bash
cd "$(dirname "$0")/backend"
if [ -f .env ]; then
  set -a
  . ./.env
  set +a
fi
export SPRING_PROFILES_ACTIVE="${SPRING_PROFILES_ACTIVE:-local}"
mvn spring-boot:run
