#!/bin/bash
name=${PWD##*/}
name=${name//[-._]/}

printf 'Setting up %s\n' $name

printf "...Creating databases\n"
dropdb ${name}
dropdb ${name}_test

createdb ${name}
createdb ${name}_test

psql -d ${name} -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"
psql -d ${name}_test -c "CREATE EXTENSION IF NOT EXISTS pgcrypto;"

psql -d ${name} -c "CREATE USER dev WITH PASSWORD 'development';"

psql -d ${name} -c "GRANT ALL PRIVILEGES ON DATABASE ${name} to dev;"
psql -d ${name}_test -c "GRANT ALL PRIVILEGES ON DATABASE ${name}_test to dev;"
