FROM python:3.8
# ENV http_proxy http://proxy-chain.xxx.com:911/
# ENV https_proxy http://proxy-chain.xxx.com:912/ 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# EXPOSE 5000

COPY . .
CMD ["python", "app.py"]


# FROM python:3.9-slim-buster
# ADD hello.py /
# COPY . /app
# WORKDIR /app
# RUN pip3 install Flask
# EXPOSE 5000
# CMD [ "python3", "./hello.py" ]