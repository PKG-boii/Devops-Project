output "cluster_name" {
  description = "EKS cluster name"
  value       = module.eks.cluster_name
}

output "cluster_endpoint" {
  description = "EKS control plane public endpoint"
  value       = module.eks.cluster_endpoint
}

output "vpc_id" {
  description = "TaskBoard VPC ID"
  value       = module.vpc.vpc_id
}

output "configure_kubectl_command" {
  description = "AWS CLI command to configure local kubeconfig"
  value       = "aws eks --region ${var.aws_region} update-kubeconfig --name ${module.eks.cluster_name}"
}
