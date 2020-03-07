#!/bin/sh

export DEVICE_ID=freedgePrototype
export CAM_UPDATE_INTERVAL=600
export ENV_UPDATE_INTERVAL=120

export CLOUD_URL='172.30.67.178'
export CLOUD_PORT=8086
export CLOUD_DATABSE='freedgeDB'
export VERBOSE=True

sudo python src/server.py \
--device_id ${DEVICE_ID} \
--camera_update_interval ${CAM_UPDATE_INTERVAL} \
--weather_update_interval ${ENV_UPDATE_INTERVAL} \
--cloudb_host ${CLOUD_URL} \
--cloudb_port ${CLOUD_PORT} \
--cloudb_database ${CLOUD_DATABSE} \
--verbose ${VERBOSE}
