# AWS Infrastructure as Code with Terraform

This directory provisions the underlying AWS network and managed Kubernetes cluster for TaskBoard:

- **VPC**: 10.20.0.0/16 with 2 public subnets, 2 private subnets, and a NAT Gateway.
- **EKS**: Managed Kubernetes 1.31 cluster with a t3.medium node group.

## Quickstart

```bash
cd terraform
cp terraform.tfvars.example terraform.tfvars
terraform init
terraform plan
terraform apply
```

To configure your `kubectl`:

```bash
aws eks --region ap-south-1 update-kubeconfig --name taskboard-eks
```

To tear down:

```bash
terraform destroy
```
