# Description

Step by step approach to easily dockerize Airflow and Pentaho Data Integration **IN SEPARATE CONTAINERS**.
Below is the high level architecture of the setup:
- Airflow:
    - Orchestrator container
    - Sends transformation/job metadata as task to Pentaho container

- Pentaho:
    - Container receives transformation/job details as task to be done
    - Performs (runs) the actual task (transformation/job)


# Pre-requisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

# Versions
- Airflow 2.0
- PDI 9.1

 # Setup
Change directory to the project folder before performing below steps.

### Environment variables, files & folders for containers
- Create a .env file and add the user and group Ids for the respective containers.
This is required for the containers to have same access privileges as that of the host user during docker compose.

        echo -e "PENTAHO_UID=$(id -u)\nPENTAHO_GID=0\nAIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env

- If needed, append the below optional variables to the above .env file.

        echo -e "<variable name>=<value>" >> .env
    - HOST_ENV --> run containers as localhost/dev/qa/prod. This will copy corresponding kettle.properties into the PDI container. Also enables PDI transformations to pick environment specific DB JNDI connections during execution. Can be used by Airflow to connect to corresponding resources.
    - CARTE_USER --> Default: cluster
    - CARTE_PASSWORD --> Default: cluster
    - AIRFLOW_ADMIN_USER --> Create Web UI user. Default: airflow
    - AIRFLOW_ADMIN_PASSWORD --> Default: airflow
    - AIRFLOW_ADMIN_EMAIL --> Required if new user to be created
    - PENTAHO_DI_JAVA_OPTIONS --> Allocate JVM memory to PDI container, based on host machine RAM. Increase if container crashes due to GC Out of memory. Ex: for Min. 1G and Max 4G, set this to "-Xms1g -Xmx4g"
    - CARTE_HOST_PORT --> Default: 8181
    - AIRFLOW_HOST_PORT --> Default: 8080

 - Create below folders for the container volumes to bind

        mkdir ./setup-airflow/logs ./setup-airflow/plugins ./setup-pentaho/logs


- Source Code
Since the DAGs/PDI source code files might undergo frequent updates, they are not copied into the container during image build, instead mounted via docker compose. Any update to these source code files on host will automatically get visible inside the container.

  - Airflow:
    - Default folder for DAGs on host is ./source-code/dags
    - Replace the above default folder in the docker compose file, with the desired folder location on host.
    - Place all the DAG files in the above host dags folder.

  - Pentaho:
    - Default folder for ktr/kjb files on host is ./source-code/ktrs
    - Replace the above default folder in the docker compose file, with the desired folder location on host.
    - Place all the PDI files in the above host ktrs folder.
    - Update repositories.xml file accordingly, to make them visible to Carte.

### Build & Deploy
Below command will build (if first time) and start all the services.

        docker-compose up
To run as daemon, add -d option.

# Web UI
- If not localhost, replace with server endpoint Url
- If not below default ports, replace with the ones used during CARTE_HOST_PORT & AIRFLOW_HOST_PORT setup.

Airflow Webserver
 
        localhost:8080/home

Carte Webserver

        localhost:8181/kettle/status

# Best practices
- ```jdbc.properties``` file, which contains database access credentials, has been included in this repo for reference purpose only. In actual development, this should be avoided and needs to be added to gitignore instead. After first code pull to a server, update it with all JNDI details before docker compose.

- ```.env``` file also may contain sensitive information, like environment dependent access keys. This also should be added to .gitignore file. Instead create this file with necessary parameters during image build.

- ```HOST_ENV``` setting this parameter gives us a flexibility to choose appropriate ```kettle.properties``` file. For example, QA and PROD mailing server SMTP details may differ. This can be included in separate kettle properties file, to be selected dynamically based on the host environment. Not only this, if one uses the ```jdbc.properties``` file, we can enable PDI container dynamically select the correct JNDI from ```jdbc.properties``` file. For ex: if one needs to test a transformation in QA environemnt using Postgres JNDI connection encoded as ```db-${HOST_ENV}```, running PDI service with ```HOST_ENV=qa```, will render ```db-qa``` database JNDI, thus using QA data for testing.

- ```PENTAHO_DI_JAVA_OPTIONS``` Having this option lets the user tweak the amount of memory PDI gets inside the container, to run a task. Depending on the host machine memory and average task complexity, this can be modified to avoid PDI container crash due to "GC Out of Memory" errors. If host machine has ample RAM and PDI container is crashing due to the default memory limits, we can increase it by setting ```PENTAHO_DI_JAVA_OPTIONS=-Xms1g -Xmx4g``` 1GB and 4GB being the lower and upper limits respectively.

# References & Credits
- [What is Carte Server ?](https://wiki.pentaho.com/display/EAI/Carte+User+Documentation)

- [Configure Carte Server](https://help.pentaho.com/Documentation/8.0/Products/Data_Integration/Carte_Clusters/060)

- [Set Repository on the Carte Server](https://help.pentaho.com/Documentation/9.1/Products/Use_Carte_Clusters)

- [Carte APIs to trigger kettle transformation/jobs](https://help.pentaho.com/Documentation/9.1/Developer_center/REST_API_Reference/Carte)

- [Scheduling a PDI job using Dockerized Airflow](https://diethardsteiner.github.io/pdi/2020/04/01/Scheduling-a-PDI-Job-on-Apache-Airflow.html)