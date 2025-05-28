resource "aws_instance" "api_server" {
  ami           = "ami-0c2b8ca13fb37a0f1"  # Exemplo: Amazon Linux 2 na us-east-1
  instance_type = var.instance_type       # Tamanho da instância → CPU, RAM
  key_name               = "key_pem"

  # Associando Security Group criado
  vpc_security_group_ids = [aws_security_group.api_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker git
              service docker start
              systemctl enable docker
              curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              git clone https://github.com/NovakiDouglas/project-ia.git
              cd project-ia
              docker-compose up -d
              EOF


  tags = {
    Name = "api-server"
  }
}
