resource "aws_instance" "api_server" {
  ami                    = "ami-0c02fb55956c7d316" # Amazon Linux 2 - us-east-1
  instance_type          = var.instance_type
  key_name               = "key_pem"
  vpc_security_group_ids = [aws_security_group.api_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.api_instance_profile.name

  # Usa script externo com variável de ambiente
  user_data = templatefile("${path.module}/startup.sh", {
    env = var.env
  })

  tags = {
    Name = "api-server"
  }
}
