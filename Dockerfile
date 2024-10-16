FROM python:3.12.4

WORKDIR /usr/src/app

RUN apt-get update
RUN apt-get install -y cmake build-essential python3-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./percentile.py" ]
