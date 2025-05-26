resource "aws_security_group" "api_sg" {
  name        = "api-sg"
  description = "Allow inbound traffic on port 5000"

  ingress {
    description = "Allow HTTP API traffic"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
