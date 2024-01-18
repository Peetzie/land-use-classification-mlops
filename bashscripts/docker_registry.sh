#!/bin/bash

# For pushing a dockerfile to the registry
GCLOUD_PROJECT="mlops-411314"
REPO="land-use-1"   # Name of artifact registry repo
REGION="europe-west4"
IMAGE="land-use-1"  # Name of choice
PATH_TO_DOCKERFILE="C:/Users/toell/OneDrive/Documents/GitHub/land-use-classification-mlops/dockerfiles/train_model.dockerfile"

gcloud auth login
gcloud auth configure-docker "${REGION}-docker.pkg.dev"

IMAGE_TAG="${REGION}-docker.pkg.dev/${GCLOUD_PROJECT}/${REPO}/${IMAGE}"

echo "GCLOUD_PROJECT=${GCLOUD_PROJECT}"
echo "REPO=${REPO}"
echo "REGION=${REGION}"
echo "IMAGE=${IMAGE}"
echo "IMAGE_TAG=${IMAGE_TAG}"

docker build -t "${IMAGE_TAG}" -f "${PATH_TO_DOCKERFILE}" --platform linux/x86_64 .
docker push "${IMAGE_TAG}"