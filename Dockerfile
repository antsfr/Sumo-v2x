FROM python:3.9

RUN mkdir -p /usr/src/app/

WORKDIR /usr/src/app

COPY . /usr/src/app/
# ADD sumoRetriever.py .
# ADD requirements.txt .
# RUN pip freeze > requirements.txt
RUN pip install -r requirements.txt
# COPY . .
CMD ["python", "sumoRetriever.py"]