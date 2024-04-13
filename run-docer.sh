docker build -t my-flask-app .

docker kill my-flask-app
docker rm my-flask-app
docker run -d \
    -p 5000:5000 \
    --name my-flask-app \
    -e FLASK_APP=app.py \
    -e FLASK_ENV=development \
    -e FLASK_DEBUG=1 \
    -e DATABASE_URL=mysql+pymysql://kabbit:kabbit@host.docker.internal:3306/kabbit_db \
    -v $(pwd):/app \
    my-flask-app