output "instance_ip" {
  description = "IP público da instância EC2 (direto da instância)"
  value       = aws_instance.api_server.public_ip
}

output "elastic_ip" {
  description = "Elastic IP atribuído à instância"
  value       = aws_eip.api_eip.public_ip
}
