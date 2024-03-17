#!/bin/bash

DOCKERFILE_NAME=$1
OUTPUT_FILE_NAME=$2
FUNC_NAME=$3

IMAGE_NAME=$(date +"%s")


# Build the docker image
docker build -f $DOCKERFILE_NAME -t $IMAGE_NAME .

# Run the docker container and output the result to a file
docker run $IMAGE_NAME /bin/bash -c "./run.sh \"$FUNC_NAME\"" > $OUTPUT_FILE_NAME
