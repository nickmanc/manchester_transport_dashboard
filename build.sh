#!/bin/bash

# usage: build.sh <version>
# e.g. ./build.sh 1.0.12

export VERSION=$1

docker build --build-arg DASHBOARD_BUILD_VERSION=$VERSION -t manchester-transport-dashboard .
BUILD_SUCCESS=$?

if [ $BUILD_SUCCESS -eq 0 ]; then
  docker tag manchester-transport-dashboard nickmanc/manchester-transport-dashboard:$VERSION
  docker push nickmanc/manchester-transport-dashboard:$VERSION
fi