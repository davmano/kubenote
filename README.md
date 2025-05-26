# 📒 KubeNote

KubeNote is a simple full-stack note-taking application built with Flask (backend & frontend) and PostgreSQL, deployed on Kubernetes using a local Kind cluster. This project is designed for DevOps hands-on learning with CI/CD, containerization, and Kubernetes.

## 🧱 Project Structure
```
kubenote/
├── kind-cluster.yaml # Kind cluster config
├── app/ # Flask applications
│ ├── backend/
│ └── frontend/
├── docker/ # Dockerfiles
│ ├── backend.Dockerfile
│ └── frontend.Dockerfile
├── k8s/
│ ├── manifests/
│ │ ├── backend.yaml
│ │ ├── frontend.yaml
│ │ ├── postgres.yaml
│ ├── configs/
│ │ ├── secret.yaml
│ │ └── configmap.yaml
│ └── ingress/
│ └── ingress.yaml
└── README.md
```

## 🚀 Tech Stack

- Frontend: Flask
- Backend: Flask (REST API)
- Database: PostgreSQL
- Containerization: Docker
- Orchestration: Kubernetes (Kind)
- CI/CD: GitHub Actions

## 🛠️ Setup (Local Dev)

### 1. Create and start the Kind cluster

```bash
kind create cluster --name kubenote --config kind-cluster.yaml
```
### 2. Build and load Docker images into Kind
```
docker build -t kubenote-backend:latest -f docker/backend.Dockerfile app/backend
docker build -t kubenote-frontend:latest -f docker/frontend.Dockerfile app/frontend

kind load docker-image kubenote-backend:latest --name kubenote
kind load docker-image kubenote-frontend:latest --name kubenote
``` 
### 3. Apply Kubernetes manifests
```
kubectl apply -f k8s/configs/
kubectl apply -f k8s/manifests/
kubectl apply -f k8s/ingress/
```
### 4. Access the App
Use the Kind node port or configure Ingress and access via localhost (requires Ingress controller like NGINX).

## 🧪 Testing the App
To verify:
```
kubectl get pods
kubectl get svc
```
Frontend should be accessible (e.g. http://localhost or NodePort IP).

## 🤖 CI/CD (GitHub Actions)
See .github/workflows/kubenote-ci.yaml for the CI pipeline.


![Docker CI](https://github.com/davmano/kubenote/actions/workflows/docker-build-and-push.yaml/badge.svg)

## ScreenShot
![Screenshot 2025-05-26 165905](https://github.com/user-attachments/assets/2e603672-0a5b-431d-895d-531ddd4220ae)


