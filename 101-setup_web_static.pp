# puppet manifest configure nginx

package { 'nginx':
  ensure => 'installed'
}

$list = [ '/data/', '/data/web_static/', '/data/web_static/shared/':
  ensure => 'directory'
}
