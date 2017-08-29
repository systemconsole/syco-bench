FROM python:3

WORKDIR /usr/src/syco-bench

RUN apt-get update
RUN apt-get upgrade
RUN curl -s https://packagecloud.io/install/repositories/akopytov/sysbench/script.deb.sh | bash
RUN apt -y install sysbench

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./syco-bench.py" ]
