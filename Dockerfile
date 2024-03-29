FROM python:3.9


RUN pip install --user --upgrade pip
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
ADD ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
ADD . /app

RUN mkdir -p /tmq
RUN chmod 777 /tmp
RUN mkdir -p /.cache
RUN chmod 777 /.cache

ENV PYTHONPATH "${PYTHONPATH}:/app"

EXPOSE 7860

HEALTHCHECK CMD curl --fail http://localhost:7860/_stcore/health

ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=7860", "--server.address=0.0.0.0"]