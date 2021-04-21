#!/bin/bash
# Derived from and modified the logging mechanism discussed in the below article. This mechanism enables Airflow
# container to trigger PDI tasks synchronously:
# https://diethardsteiner.github.io/pdi/2020/04/01/Scheduling-a-PDI-Job-on-Apache-Airflow.html


CARTE_SERVER_URL=$PDI_CONN_STR
PDI_LOG_LEVEL=Basic
SLEEP_INTERVAL_SECONDS=5
PDI_TASK=$1
PDI_TASK_CMD=$2


if [[ $PDI_TASK_CMD == *"rep="* ]] && [[ $PDI_TASK_CMD == *"job="*  || $PDI_TASK_CMD == *"trans="* ]]; then

  set PDI_TASK_ID
  set PDI_TASK_STATUS


  # Execute task and get its Task ID
  if [[ $PDI_TASK_CMD == *"executeJob"* ]]; then
    PDI_TASK_ID=$(curl -s "${CARTE_SERVER_URL}/kettle/${PDI_TASK_CMD}&level=${PDI_LOG_LEVEL}" | xmlstarlet sel -t -m '/webresult/id' -v . -n)
    echo "The PDI Task ID is: " ${PDI_TASK_ID}
  else
    PDI_TASK_ID=$(curl -s "${CARTE_SERVER_URL}/kettle/${PDI_TASK_CMD}&level=${PDI_LOG_LEVEL}")
  fi

  getPDITaskStatus() {
    if [[ $PDI_TASK_CMD == *"executeTrans"* ]]; then
      curl -s "${CARTE_SERVER_URL}/kettle/transStatus/?name=${PDI_TASK}&id=${PDI_TASK_ID}&xml=Y" | xmlstarlet sel -t -m '/transstatus/status_desc' -v . -n
    else
      curl -s "${CARTE_SERVER_URL}/kettle/jobStatus/?name=${PDI_TASK}&id=${PDI_TASK_ID}&xml=Y" | xmlstarlet sel -t -m '/jobstatus/status_desc' -v . -n
    fi
  }

  getPDITaskFullLog() {
    if [[ $PDI_TASK_CMD == *"executeTrans"* ]]; then
      echo "Check carte server for transformation log!!!"
    else
      curl -s "${CARTE_SERVER_URL}/kettle/jobStatus/?name=${PDI_TASK}&id=${PDI_TASK_ID}&xml=Y" | xmlstarlet sel -t -m 'jobstatus/result/log_text' -v . -n
    fi
  }

  PDI_TASK_STATUS=$(getPDITaskStatus)

  # loop as long as the job is running
  while [ ${PDI_TASK_STATUS} == "Running" ]
  do
    PDI_TASK_STATUS=$(getPDITaskStatus)
    echo "The PDI task status is: " ${PDI_TASK_STATUS}
    echo "I'll check in ${SLEEP_INTERVAL_SECONDS} seconds again"
    # check every x seconds
    sleep ${SLEEP_INTERVAL_SECONDS}
  done

  # get and print full pdi task log
  echo "The PDI task status is: " ${PDI_TASK_STATUS}
  echo "Printing full log ..."
  echo $(getPDITaskFullLog)

  # Check if any error. Send exit 1 if so.
  if [[ ${PDI_TASK_STATUS} == "Finished" ]]; then
      exit 0
  else
    exit 1
  fi

else
  echo "Error executing: ${PDI_TASK_CMD}\n File or directory not found."
  exit 1
fi