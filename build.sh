#!/bin/bash

# usage: build.sh <version>
# e.g. ./build.sh 1.0.12

export VERSION=$1

docker build -t transport-dashboard .
BUILD_SUCCESS=$?

if [ $BUILD_SUCCESS -eq 0 ]; then
  docker tag transport-dashboard nexus-altdev.services.aquilaheywood.co.uk/transport-dashboard:$VERSION
  docker push nexus-altdev.services.aquilaheywood.co.uk/transport-dashboard:$VERSION
fi