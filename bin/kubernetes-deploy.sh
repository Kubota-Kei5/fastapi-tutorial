# !/bin/bash
set -e
# kubectl create secret generic --save-config env-local --from-env-file ./env/.env.local
kubectl apply -f ../k8s/deployment.yaml
echo "Deployment applied successfully."

docker build --no-cache -f .devcontainer/Dockerfile -t asia-northeast1-docker.pkg.dev/k8s-tutorial-454510/my-repo/fastapi-tutorial:latest .

docker push asia-northeast1-docker.pkg.dev/k8s-tutorial-454510/my-repo/fastapi-tutorial:latest

kubectl set image deployment/fastapi-tutorial fastapi-tutorial=asia-northeast1-docker.pkg.dev/k8s-tutorial-454510/my-repo/fastapi-tutorial:latest