resource "aws_iam_role" "api_secrets_role" {
  name = "api-secrets-access-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
      Action = "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_policy" "api_secrets_policy" {
  name        = "api-secrets-access-policy"
  description = "Permite acesso ao Secrets Manager para ler API Keys"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "secretsmanager:GetSecretValue"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.api_secrets_role.name
  policy_arn = aws_iam_policy.api_secrets_policy.arn
}

resource "aws_iam_instance_profile" "api_instance_profile" {
  name = "api-instance-profile"
  role = aws_iam_role.api_secrets_role.name
}
