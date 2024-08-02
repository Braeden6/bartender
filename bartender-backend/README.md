

docker pull pgvector/pgvector:pg12
docker run --name pgvector -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 pgvector/pgvector:pg12

# inside the docker postgres
psql -U postgres
CREATE DATABASE "main";
\c main
CREATE EXTENSION vector;

