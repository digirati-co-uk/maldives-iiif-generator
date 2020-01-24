variable "region" {
  description = "AWS region for deployment"
  default     = "eu-west-1"
}

variable "prefix" {
  description = "Prefix for AWS resources"
  default     = "mhs"
}

variable "project" {
  description = "Project name for tags"
  default     = "maldives-heritage"
}