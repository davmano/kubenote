# Monitoring Stack Setup

This directory contains the monitoring stack configuration for KubeNote.

## Required Secrets

Before deploying the monitoring stack, create the following secrets:

### PostgreSQL Exporter Secret
```bash
kubectl create secret generic postgres-exporter-secret \
  --from-literal=DATA_SOURCE_NAME="postgresql://USERNAME:PASSWORD@postgres:5432/notesdb?sslmode=disable" \
  --namespace=default
```

Replace `USERNAME` and `PASSWORD` with your PostgreSQL credentials from the existing secret.

### Grafana Admin Secret
```bash
kubectl create secret generic grafana-secret \
  --from-literal=admin-user="YOUR_ADMIN_USERNAME" \
  --from-literal=admin-password="YOUR_SECURE_PASSWORD" \
  --namespace=monitoring
```

Replace the placeholders with your desired Grafana admin credentials.

## Deployment Order

1. Create secrets (as shown above)
2. Deploy monitoring namespace: `kubectl apply -f namespace.yaml`
3. Deploy RBAC: `kubectl apply -f prometheus-rbac.yaml`
4. Deploy Prometheus components
5. Deploy Grafana components
6. Deploy ServiceMonitors

## Security Notes

- Never commit secrets to version control
- Use strong, unique passwords for all services
- Consider using external secret management solutions for production deployments
