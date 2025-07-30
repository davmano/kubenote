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

## 📊 Monitoring Stack

KubeNote includes integrated Prometheus and Grafana monitoring:

### Components
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization dashboards
- **PostgreSQL Exporter**: Database metrics
- **Application Metrics**: Custom Flask application metrics

### Setup Monitoring
```bash
# Deploy monitoring namespace and RBAC
kubectl apply -f k8s/monitoring/namespace.yaml
kubectl apply -f k8s/monitoring/prometheus-rbac.yaml

# Create monitoring secrets
# Before deploying monitoring components, create the required secrets.
# See k8s/monitoring/README.md for detailed secret creation instructions.

# Deploy Prometheus
kubectl apply -f k8s/monitoring/prometheus-configmap.yaml
kubectl apply -f k8s/monitoring/prometheus-deployment.yaml
kubectl apply -f k8s/monitoring/prometheus-service.yaml

# Deploy Grafana
kubectl apply -f k8s/monitoring/grafana-configmap.yaml
kubectl apply -f k8s/monitoring/grafana-deployment.yaml
kubectl apply -f k8s/monitoring/grafana-service.yaml

# Deploy PostgreSQL monitoring
kubectl apply -f k8s/monitoring/postgres-exporter-deployment.yaml

# Deploy ServiceMonitors
kubectl apply -f k8s/monitoring/backend-servicemonitor.yaml
kubectl apply -f k8s/monitoring/frontend-servicemonitor.yaml
kubectl apply -f k8s/monitoring/postgres-servicemonitor.yaml

# Deploy monitoring ingress
kubectl apply -f k8s/monitoring/ingress-monitoring.yaml
```

### Access Monitoring Services
- **Prometheus**: http://kubenote.local/prometheus (via monitoring ingress)
- **Grafana**: http://kubenote.local/grafana (via monitoring ingress)
  - Use the credentials you configured when creating the grafana-secret

### Available Dashboards
- **KubeNote Application Metrics**: HTTP requests, response times, service uptime
- **PostgreSQL Metrics**: Database connections, size, query rates

### Metrics Endpoints
- Backend: http://backend:5000/metrics
- Frontend: http://frontend:5000/metrics
- PostgreSQL: http://postgres-exporter:9187/metrics

## 🤖 CI/CD (GitHub Actions)
See .github/workflows/kubenote-ci.yaml for the CI pipeline.
Action

[![Docker Build & Push](https://github.com/davmano/kubenote/actions/workflows/docker-build-and-push.yaml/badge.svg)](https://github.com/davmano/kubenote/actions/workflows/docker-build-and-push.yaml)
