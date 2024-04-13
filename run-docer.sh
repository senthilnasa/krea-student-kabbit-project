docker build -t my-flask-app .

docker kill my-flask-app
docker rm my-flask-app
docker run -d \
    -p 5000:5000 \
    --name my-flask-app \
    -e FLASK_APP=app.py \
    -e FLASK_ENV=development \
    -e FLASK_DEBUG=1 \
    -e MYSQL_HOST=host.docker.internal \
    -e MYSQL_USER=kabbit \
    -e MYSQL_PASSWORD=kabbit \
    -e MYSQL_DATABASE=kabbit_db \
    -v $(pwd):/app \
    my-flask-app