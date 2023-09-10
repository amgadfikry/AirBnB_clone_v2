# puppet manifest configure nginx
package { 'nginx':
  ensure => 'installed'
}
exec { 'run1':
  command => 'sudo mkdir -p /data/web_static/shared/',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'run2':
  command => 'sudo mkdir -p /data/web_static/releases/test/',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'run3':
  command => 'echo "this is simple content" | sudo tee /data/web_static/releases/test/index.html',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'run4':
  command => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'change_permission':
  command => 'sudo chown -R ubuntu:ubuntu /data/',
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
$content = 'location /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}'
exec { 'config':
  command => "sudo sed -i \"/server_name _;/a ${content}\" /etc/nginx/sites-available/default",
  path    => [ '/usr/local/bin/', '/usr/bin/', '/bin/' ]
}
exec { 'restart':
  command => 'sudo service nginx restart',
  path    => [ '/usr/bin/', '/bin/' ]
}
