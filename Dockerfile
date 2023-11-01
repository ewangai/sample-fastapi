#pull version of python required
FROM python:3.11.4

# set work directory
WORKDIR /usr/src/app

# pull the required libs from requirements.txt from working directory.
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

#copy everything in current directory into working directory.
COPY . .

#give command to run when starting the container. Split each comand 
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
