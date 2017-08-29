FROM python:3

WORKDIR /usr/src/syco-bench

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./syco-bench.py" ]
