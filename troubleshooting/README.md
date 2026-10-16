# Kubernetes Troubleshooting Exercises

This module contains deliberately broken manifests used for diagnosing and resolving real-world Kubernetes failure scenarios.

## Exercise 1: ImagePullBackOff Investigation

1. Apply the manifest:
   ```bash
   kubectl apply -f troubleshooting/broken-image.yaml
   ```
2. Diagnose:
   ```bash
   kubectl get pods -n taskboard
   kubectl describe pod taskboard-broken-image-<hash> -n taskboard
   ```
3. Root Cause:
   The container references `ghcr.io/example/taskboard-backend:does-not-exist`.
4. Fix:
   Update the image tag to a valid image repository or rollback the deployment.

---

## Exercise 2: Broken Service Selector (No Endpoints)

1. Apply the manifest:
   ```bash
   kubectl apply -f troubleshooting/broken-service.yaml
   ```
2. Diagnose:
   ```bash
   kubectl get svc -n taskboard
   kubectl get endpoints taskboard-broken-service -n taskboard
   kubectl get pods -n taskboard --show-labels
   ```
3. Root Cause:
   The Service selector `app: label-that-does-not-exist` does not match any running pods, resulting in an empty Endpoints list.
4. Fix:
   Align `spec.selector` in the Service with the labels defined on the target Pods.
