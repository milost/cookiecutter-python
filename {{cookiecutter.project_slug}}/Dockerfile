# syntax = docker/dockerfile:1.0-experimental

# Use an official Python runtime as a parent image
FROM python:{{cookiecutter.python_version}}-slim-buster

ARG package_name

# Define environment variables
ENV package_name=$package_name \
    ANOTHERVAR="another value"

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY {{cookiecutter.project_slug}}/  /app/{{cookiecutter.project_slug}}
{% if cookiecutter.use_jupyterlab == "yes" -%}
COPY notebooks/  /app/notebooks
{% endif %}
COPY resources/ /app/resources 
COPY README.rst LICENSE.rst Pipfile Pipfile.lock setup.py /app/

## Install any needed packages specified in requirements.txt
# RUN printf $NEXUS_CONFIG | base64 -d > /etc/pip.conf
# RUN pip install --upgrade pip
RUN pip install pipenv
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

# TODO This should be more like an entrypoint
# Run app.py when the container launches
{% if cookiecutter.use_jupyterlab == "no" -%}
CMD python ./{{cookiecutter.project_slug}}/main.py
{% else %}
CMD jupyter lab --ip=0.0.0.0 --notebook-dir=./notebooks --allow-root --no-browser --NotebookApp.token='' --NotebookApp.password=''
{% endif %}
