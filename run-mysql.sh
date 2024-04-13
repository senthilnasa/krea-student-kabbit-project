docker kill kabbit-db
docker rm kabbit-db
docker run -d \
  -p 3306:3306 \
  --name kabbit-db \
  -e MYSQL_ROOT_PASSWORD=    \
  -e MYSQL_DATABASE=kabbit_db \
  -e MYSQL_USER=kabbit \
  -e MYSQL_PASSWORD=kabbit \
  -v /docker/mysql-data/:/var/lib/mysql \
  mariadb:latest
