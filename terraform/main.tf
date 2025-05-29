resource "aws_instance" "api_server" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2 - us-east-1
  instance_type = var.instance_type
  key_name      = "key_pem"

  vpc_security_group_ids = [aws_security_group.api_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              yum update -y

              # Instala Docker e Git
              amazon-linux-extras enable docker
              yum install -y docker git

              # Inicia o Docker e adiciona ec2-user ao grupo
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user

              # Instala Docker Compose
              curl -L "https://github.com/docker/compose/releases/download/v2.24.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
              chmod +x /usr/local/bin/docker-compose
              ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

              # Clona o projeto (ajuste se for repositório privado)
              su - ec2-user -c "git clone https://github.com/NovakiDouglas/project-ia.git"

              # Sobe os serviços com docker-compose
              su - ec2-user -c "cd project-ia && docker-compose down -v || true"
              su - ec2-user -c "cd project-ia && docker-compose up -d --build"
              EOF

  tags = {
    Name = "api-server"
  }
}
