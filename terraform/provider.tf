provider "aws" {
  region = var.aws_region
  default_tags {
    tags = {
      owner : "Douglas Novaki"
      managed-by = "terraform"
    }
  }
}
