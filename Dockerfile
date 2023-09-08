FROM python:3.10.9
WORKDIR /EotVRESTful
COPY app /EotVRESTful/app
COPY main.py /EotVRESTful
COPY .env /EotVRESTful
COPY requirements.txt /EotVRESTful
RUN pip install -r requirements.txt
EXPOSE 3001
CMD ["python", "main.py"]
