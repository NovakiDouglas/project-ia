resource "aws_instance" "api_server" {
  ami           = "ami-0c02fb55956c7d316" // imagem padrão do Ubuntu 20.04 LTS na AWS região us-east-1
  instance_type = var.instance_type //  tamanho da instância → CPU, RAM

  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y docker.io git
              sudo systemctl start docker
              sudo systemctl enable docker
              git clone https://github.com/SEU_USUARIO/meu-projeto-ia.git
              cd meu-projeto-ia
              docker-compose up -d
              EOF

  tags = {
    Name = "api-server"
  }
}
