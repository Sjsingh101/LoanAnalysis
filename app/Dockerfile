FROM python:3.9-slim-buster

COPY . ./app
WORKDIR /app

# Credentials
ENV DB_NAME=
ENV DB_USER=
ENV DB_KEY=
ENV DB_URL=
ENV PORT 3000

# Install Packages
RUN pip3 install -r requirements.txt
EXPOSE 3000

# Entry
#ENTRYPOINT [ "python3" ]
#CMD ["gunicorn"  , "-b", "0.0.0.0:3000", "dash_test:server"]
CMD exec gunicorn --bind 0.0.0.0:$PORT dash_test:server --workers 1 --threads 1 --timeout 60