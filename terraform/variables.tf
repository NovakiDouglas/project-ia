# Define a região da AWS onde os recursos serão criados
variable "aws_region" {
  description = "Região da AWS"
  default     = "us-east-1"
}

# Define o tipo de instância EC2
variable "instance_type" {
  description = "Tipo da instância EC2"
  default     = "t2.micro"
}

variable "env" {
  description = "Ambiente da aplicação (dev ou prod)"
  type        = string
}
