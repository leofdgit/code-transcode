#!/bin/bash

IMAGE_NAME="js_eval"

docker build -f Dockerfile.js -t $IMAGE_NAME .

docker run $IMAGE_NAME > output.dat
