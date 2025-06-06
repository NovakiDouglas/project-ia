resource "aws_instance" "api_server" {
  ami                    = "ami-0c02fb55956c7d316"
  instance_type          = var.instance_type
  key_name               = "key_pem"
  subnet_id              = aws_subnet.public_subnet.id
  vpc_security_group_ids = [aws_security_group.api_sg.id]
  iam_instance_profile   = aws_iam_instance_profile.api_instance_profile.name

  user_data = templatefile("${path.module}/startup.sh", {
    env = var.env
  })

  tags = {
    Name = "api-server"
  }
}

resource "aws_eip" "api_eip" {
  instance = aws_instance.api_server.id
  domain   = "vpc"

  tags = {
    Name = "api-eip"
  }
}
