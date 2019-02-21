terraform {
    backend "s3" {
    encrypt = true
    bucket = "maxmilhas-bucket"
    region = "us-east-1"
    key = "folder/statefile"
    }
}

