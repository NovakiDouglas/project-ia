resource "aws_instance" "api_server" {
  ami           = "ami-0c02fb55956c7d316" // imagem padrão do Ubuntu 20.04 LTS na AWS região us-east-1
  instance_type = var.instance_type // tamanho da instância → CPU, RAM

  // Associando Security Group criado
  vpc_security_group_ids = [aws_security_group.api_sg.id]

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y docker.io docker-compose git
              sudo systemctl start docker
              sudo systemctl enable docker
              git clone https://github.com/NovakiDouglas/project-ia.git
              cd project-ia
              docker-compose up -d
              EOF

  tags = {
    Name = "api-server"
  }
}
