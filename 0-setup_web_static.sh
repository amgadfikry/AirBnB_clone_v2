#!/usr/bin/env bash
# bash script that sets up webstatic

sudo apt-get -y update
sudo apt-get -y install nginx
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
echo "this is simple content" | sudo tee /data/web_static/releases/test/index.html
if [ -d /data/web_static/current ]; then
	if [ -L /data/web_static/current ]; then
		sudo rm /data/web_static/current
	fi
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/
content=$(cat << 'END HEREDOC'
	server {
		listen 80 default_server;
		listen [::]:80 default_server;
		root /var/www/html;	
		index index.html index.htm index.nginx-debian.html;
		server_name _;
		rewrite ^/redirect_me https://www.youtube.com permanent;
		add_header X-Served-By $hostname;
		error_page 404 /custom_404.html;
		location = /custom_404.html {
			root /usr/share/nginx/html;
			internal;
		}
		location / {
			try_files $uri $uri/ =404;
		}
		location /hbnb_static {
			alias /data/web_static/current/;
		}
	}
END HEREDOC
)
echo -e "$content" >> text.txt
check=$(grep -Fxf text.txt /etc/nginx/nginx.conf)
if [ -z "$check" ]; then
	sudo sed -i '/http {/r text.txt' /etc/nginx/nginx.conf
fi
sudo rm text.txt
sudo service nginx reload
