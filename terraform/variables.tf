variable "aws_region" {
  description = "AWS region for all resources"
  type        = string
  default     = "ca-west-1"
}

variable "image_uri" {
  description = "ECR image URI to deploy to Lambda. Empty string skips Lambda creation."
  type        = string
  default     = ""
}

variable "github_repo" {
  description = "GitHub repository in owner/repo format"
  type        = string
  default     = "bkabyrne/windtrend"
}

variable "state_bucket" {
  description = "S3 bucket name for Terraform state"
  type        = string
  default     = "bkabyrne-windtrend-tfstate"
}