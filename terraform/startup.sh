#!/bin/bash

# Atualiza pacotes
yum update -y

# Instala Docker e Git
amazon-linux-extras enable docker
yum install -y docker git

# Inicia o Docker e adiciona o usuário padrão ao grupo
systemctl start docker
systemctl enable docker
usermod -aG docker ec2-user

# Instala Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.24.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Clona o repositório
su - ec2-user -c "git clone https://github.com/NovakiDouglas/project-ia.git"

# Injeta ENV como variável para docker-compose
cat <<EOF > /home/ec2-user/project-ia/.env
ENV=${env}
EOF

# Sobe os serviços
su - ec2-user -c "cd project-ia && docker-compose down -v || true"
su - ec2-user -c "cd project-ia && docker-compose up -d --build"
