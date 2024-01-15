variable "aws_region" {
  description = "Region for the AWS services to run in."
  type        = string
  default     = "us-east-1"
}

variable "bucket_prefix" {
  description = "Bucket prefix for the S3"
  type        = string
  default     = "job-posts-data-"
}

variable "redshift_password" {
  description = "Password for the database in the Redshift cluster"
  type        = string
}

variable "contact_email" {
  description = "Email address to send budget notifications to"
  type        = string
}