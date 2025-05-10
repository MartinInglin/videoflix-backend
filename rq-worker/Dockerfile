FROM python:3

WORKDIR /usr/src/app

# 1) Install ffmpeg first, and verify
RUN apt-get update \
 && apt-get install -y ffmpeg \
 && ffmpeg -version \
 && apt-get clean

# 2) Python deps
COPY requirements.txt ./
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 3) Your code
COPY . .

CMD ["rq", "worker", "default"]
