FROM python:3.9.2-slim-buster
RUN mkdir /app && chmod 777 /app
WORKDIR /app
ENV DEBIAN_FRONTEND=noninteractive
RUN apt -qq update && apt -qq install -y git python3 ffmpeg libsndfile1-dev python3-pip 
COPY . . 
RUN pip3 install -r requirements.txt
CMD ["bash","start.sh"]
