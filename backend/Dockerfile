# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /backend

# Install dependencies
RUN pip install --upgrade pip
RUN pip install django
RUN pip install mysqlclient
RUN pip install django-autoreload
RUN pip install python-dotenv
RUN pip install django-cors-headers
RUN pip install djangorestframework
RUN curl -sSL https://github.com/vishnubob/wait-for-it/raw/master/wait-for-it.sh -o /wait-for-it.sh && \
    chmod +x /wait-for-it.sh

# Copy the backend code into the container at /backend
COPY /backend/ /backend

# Expose port 7012 to allow external access
EXPOSE 7004

CMD ["sh", "-c", "python manage.py migrate && python manage.py migrate backend && python manage.py runserver 0.0.0.0:7004"]