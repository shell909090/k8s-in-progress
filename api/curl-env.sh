#!/bin/bash

export CURL_CA_BUNDLE=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
export TOKEN=$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)

curl -H "Authorization: Bearer $TOKEN" https://kubernetses
