# Download ubuntu from docker hub
FROM ubuntu:latest

# Download updates and install python3, pip and vim
RUN apt-get update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y
RUN apt-get install vim -y
#ENTRYPOINT ["python3"]
CMD [ "python3 --version"]
# Declaring working directory in our container
WORKDIR /opt/apps
CMD ["mkdir", "logs"]
# Copy all relevant files to our working dir /opt/apps/flaskap
COPY requirements.txt .

# Install all requrements for our app
RUN pip3 install -r requirements.txt

# Copy source files to $WORKDIR
COPY ./src .
RUN chmod +x bincryptsell.py
# Expose container port to outside host
EXPOSE 8000

# Run the application
CMD [ "python3", "/opt/apps/bincryptsell.py" ]
