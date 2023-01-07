FROM python

WORKDIR /proxy_onem2m
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python", "./onem2mproxy.py" ]