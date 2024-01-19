#!/bin/bash

# For pushing a dockerfile to the registry
GCLOUD_PROJECT="mlops-411314"
REPO="app-1"   # Name of artifact registry repo
REGION="europe-west4"
APPNAME="app-4"  # Name of choice
PATH_TO_DOCKERFILE="C:/Users/toell/OneDrive/Documents/GitHub/land-use-classification-mlops/dockerfiles/app.dockerfile"
IMAGE_TAG="${REGION}-docker.pkg.dev/${GCLOUD_PROJECT}/${REPO}/${APPNAME}"

gcloud auth login
gcloud auth configure-docker "${REGION}-docker.pkg.dev"

echo "GCLOUD_PROJECT=${GCLOUD_PROJECT}"
echo "REPO=${REPO}"
echo "REGION=${REGION}"
echo "APPNAME=${APPNAME}"
echo "IMAGE_TAG=${IMAGE_TAG}"

docker build -t "${IMAGE_TAG}" -f "${PATH_TO_DOCKERFILE}" --platform linux/x86_64 .
docker tag "${IMAGE_TAG}" gcr.io/"${GCLOUD_PROJECT}"/"${APPNAME}"
gcloud auth configure-docker
docker push gcr.io/"${GCLOUD_PROJECT}"/"${APPNAME}"

# Does not work due to a much longer name being the real one:
# gcloud run deploy "${APPNAME}" --image "${IMAGE_TAG}" --platform managed --region "${REGION}" --allow-unauthenticated