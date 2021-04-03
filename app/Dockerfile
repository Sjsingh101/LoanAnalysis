FROM python:3.9-slim-buster

COPY . ./app
WORKDIR /app

# Credentials
ENV DB_NAME=
ENV DB_USER=
ENV DB_KEY=
ENV DB_URL=

# Install Packages
RUN pip3 install -r requirements.txt
EXPOSE 3000

# Entry
ENTRYPOINT [ "python3" ]
CMD [ "dash-test.py" ]