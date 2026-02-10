#!/bin/sh
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.21.0/serving-crds.yaml
kubectl apply -f https://github.com/knative/serving/releases/download/knative-v1.21.0/serving-core.yaml
kubectl apply -f https://github.com/knative-extensions/net-kourier/releases/download/knative-v1.21.0/kourier.yaml

kubectl patch configmap/config-network \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"ingress-class":"kourier.ingress.networking.knative.dev"}}'

kubectl patch configmap/config-domain \
  --namespace knative-serving \
  --type merge \
  --patch '{"data":{"127.0.0.1.nip.io":""}}'

kubectl patch service/kourier \
  --namespace kourier-system \
  --type merge \
  --patch '{"spec":{"type":"ClusterIP"}}'

kubectl apply -f vllm-omni.yaml

# kubectl -n kourier-system port-forward services/kourier-internal 8080:80
# Go to http://comfyui.default.127.0.0.1.nip.io:8080/
