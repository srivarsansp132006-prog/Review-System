FROM python:3.10-alpine
WORKDIR /app
COPY app.py .
EXPOSE 3000
CMD ["python", "app.py"]