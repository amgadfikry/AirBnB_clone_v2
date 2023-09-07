# puppet manifest configure nginx
package { 'nginx':
  ensure => 'installed'
}
$list = [ '/data/', '/data/web_static/', '/data/web_static/shared/',
          '/data/web_static/releases/', '/data/web_static/releases/test/'
        ]
file { $list:
  ensure => 'directory'
}
file { '/data/web_static/releases/test/index.html':
  ensure  => 'present',
  content => 'this is simple content'
}
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test/'
}
exec { 'change_permission':
  command => 'sudo chown -R ubuntu:ubuntu /data/',
  path    => [ '/usr/bin/', '/bin/' ]
}
file_line { 'add_location':
  ensure => 'present',
  path   => '/etc/nginx/sites-available/default',
  after  => 'server_name _;',
  line   => 'location /hbnb_static {\n\talias /data/web_static/current/;\n}'
}
exec { 'restart':
  command => 'sudo service nginx restart',
  path    => [ '/usr/bin/', '/bin/' ]
}
