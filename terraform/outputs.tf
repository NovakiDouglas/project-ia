# Exibe o IP público da instância EC2 criada
output "instance_ip" {
  description = "IP público da instância EC2"
  value       = aws_instance.api_server.public_ip
}
# output "elastic_ip" {
#   value = aws_eip.api_eip.public_ip
# }
