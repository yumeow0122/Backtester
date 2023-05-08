FROM python:3.10

WORKDIR /app

RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
  tar -xvzf ta-lib-0.4.0-src.tar.gz && \
  cd ta-lib/ && \
  ./configure --prefix=/usr && \
  make && \
  make install

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN rm -R ta-lib ta-lib-0.4.0-src.tar.gz

COPY . .

CMD [ "python", "main.py" ]