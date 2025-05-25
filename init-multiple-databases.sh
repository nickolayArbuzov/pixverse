#!/bin/bash
set -e

databases=$(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' ')

for db in $databases; do
  psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
    CREATE DATABASE "$db";
EOSQL
done
