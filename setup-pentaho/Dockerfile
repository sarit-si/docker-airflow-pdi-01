# Get Base image
FROM openjdk:8-jre

LABEL maintainer="saritkumarsi@gmail.com" \
      version="1.1" \
      description="Docker file builds container with Pentaho Data Integration & Carte Server"

# Set PDI user with permissions same as the Host machine.
ARG PENTAHO_GID
ARG PENTAHO_UID

# Set required environment vars
ENV PDI_RELEASE=9.1 \
    PDI_VERSION=9.1.0.0-324 \
    PENTAHO_JAVA_HOME=/usr/local/openjdk-8 \
    PENTAHO_HOME=/home/pentaho \
    PENTAHO_UID=${PENTAHO_UID} \
    PENTAHO_GID=${PENTAHO_GID} \
    KETTLE_HOME=/opt/data-integration \
    PATH=${KETTLE_HOME}:${PATH}

# Create Pentaho user home directory and required sub-folders
RUN mkdir -p ${PENTAHO_HOME}/templates ${PENTAHO_HOME}/scripts \
# Create Pentaho group passed as PENTAHO_GID arg
    && groupadd -r ${PENTAHO_GID} \
# Create Pentaho user with PENTAHO_UID same as Host UID, and assign to new group
    && useradd -s /bin/bash -d ${PENTAHO_HOME} -r -g ${PENTAHO_GID} -u ${PENTAHO_UID} pentaho \
# Download PDI and save in PENTAHO_HOME
    && /usr/bin/wget --progress=dot:giga \
    https://sourceforge.net/projects/pentaho/files/Pentaho%20${PDI_RELEASE}/client-tools/pdi-ce-${PDI_VERSION}.zip \
    -P ${PENTAHO_HOME} \
# Unzip PDI to /opt/ directory
    && /usr/bin/unzip -q ${PENTAHO_HOME}/pdi-ce-${PDI_VERSION}.zip -d /opt/ \
# Clean up downloaded files
    && rm -R ${PENTAHO_HOME}/pdi-ce-${PDI_VERSION}.zip \
# Create directory for the kettle.properties file
    && mkdir ${KETTLE_HOME}/.kettle \
# Make pentaho user owner of both PENTAHO_HOME and KETTLE_HOME directories
    && chown -R pentaho ${PENTAHO_HOME} ${KETTLE_HOME}

# Copy carte configs and docker entrypoint file
COPY carte-*-config.xml ${PENTAHO_HOME}/templates/
COPY docker-entrypoint.sh ${PENTAHO_HOME}/scripts/

# Make entrypoint as executable
RUN chmod +x ${PENTAHO_HOME}/scripts/docker-entrypoint.sh

# # Install App dependent packages, if any
# # Download MySQL JDBC Connector to PENTAHO_HOME
# RUN /usr/bin/wget --progress=dot:giga \
#     https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-5.1.49.zip -P ${PENTAHO_HOME} \
# # Unzip MySQL jar file
#     && /usr/bin/unzip -q ${PENTAHO_HOME}/mysql-connector-java-5.1.49.zip -d ${PENTAHO_HOME} \
# # Copy unzipped jar file to /opt/data-integration
#     && cp ${PENTAHO_HOME}/mysql-connector-java-5.1.49/mysql-connector-java-5.1.49-bin.jar /opt/data-integration/lib \
# # Clean up downloaded files
#     && rm -R ${PENTAHO_HOME}/mysql-connector*

USER pentaho

# Expose Carte Server
EXPOSE ${CARTE_PORT}

# Set working directory
WORKDIR ${KETTLE_HOME}

# Set container entrypoint. Sets all required configs for carte server.
ENTRYPOINT ["/home/pentaho/scripts/docker-entrypoint.sh"]

# Start Carte Server - the entry point sets configs in carte.config.xml which is passed to carte.sh
CMD ["carte.sh", "carte.config.xml"]