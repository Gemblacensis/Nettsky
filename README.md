# Nettsky
DAT 515, group 02

# To run Docker
docker-compose up --build -d

# To run Kubernetes:
docker build -t web:latest --network=host .
docker image tag web:latest localhost:5000/web:latest
docker image push localhost:5000/web:latest

kubectl apply -f .