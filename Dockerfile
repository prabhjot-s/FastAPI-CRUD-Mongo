FROM python:3.11-slim
WORKDIR /app
 
COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt
 
COPY . /app
 
CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
 