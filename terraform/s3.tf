resource "aws_s3_bucket" "jsf-bucket" {
  bucket_prefix = var.bucket_prefix
  force_destroy = true
}

resource "aws_s3_bucket_versioning" "jsf-bucket-versioning" {
  bucket = aws_s3_bucket.jsf-bucket.id
  versioning_configuration {
    status = "Enabled"
  }
}