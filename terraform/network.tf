# resource "aws_eip" "api_eip" {
#   domain = "vpc"
# }
# resource "aws_eip_association" "api_eip_assoc" {
#   instance_id   = aws_instance.api_server.id
#   allocation_id = aws_eip.api_eip.id
# }
