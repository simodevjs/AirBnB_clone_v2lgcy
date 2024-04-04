#!/usr/bin/env bash
# sets up the web servers for the deployment of web_static

#sudo apt-get -y update
#sudo apt-get -y upgrade
#sudo apt-get -y install nginx
blue='\e[1;34m'
brown='\e[0;33m'
green='\e[1;32m'
reset='\033[0m'

echo -e "${blue}Updating and doing some minor checks...${reset}\n"

function install() {
        command -v "$1" &> /dev/null

        #shellcheck disable=SC2181
        if [ $? -ne 0 ]; then
                echo -e "       Installing: ${brown}$1${reset}\n"
                sudo apt-get update -y -qq && \
                        sudo apt-get install -y "$1" -qq
                echo -e "\n"
        else
                echo -e "       ${green}${1} is already installed.${reset}\n"
        fi
}

install nginx #install nginx

sudo mkdir -p /data/web_static/releases/test /data/web_static/shared
sudo tee /data/web_static/releases/test/index.html <<EOF
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -hR ubuntu:ubuntu /data/
sudo sed -i '/^}$/i \    location /hbnb_static/ {\n        alias /data/web_static/current/;\n    }\n' /etc/nginx/sites-available/default
sudo service nginx restart
