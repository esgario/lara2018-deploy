# Dockerize and deploy machine learning model as REST API using Flask/Redis/Pytorch

Just install docker and docker-compose (https://docs.docker.com/) and run the following command:
```
docker-compose up
```
The server will be running on port 5000.

---
### Adding a new inference method...
To add a new inference algorithm you have to:
1. Copy your files to the folder */codes*.
2. Modify the worker.py to import and run your script.
