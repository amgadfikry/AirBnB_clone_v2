#!/usr/bin/python3
"""fabric svript deploy compress file """
from fabric.api import *
from datetime import datetime


env.hosts = ["54.237.107.99", "100.25.103.38"]
env.user = "ubuntu"


def do_pack():
    """ function that compress static web folder"""
    n = datetime.now()
    t = f"web_static_{n.year}{n.month}{n.day}{n.hour}{n.minute}{n.second}.tgz"
    local("mkdir -p versions")
    with lcd("./versions"):
        res = local(f"tar -czvf {t} ../web_static")
        if res.succeeded:
            return f"versions/{t}"
    return None


def do_deploy(archive_path):
    """function that deploy the archive file """
    try:
        archive = archive_path.split('/')[-1]
        path = '/data/web_static/releases/' + archive.strip('.tgz')
        current = '/data/web_static/current'
        put(archive_path, '/tmp')
        sudo('mkdir -p {}/'.format(path))
        sudo('tar -xzf /tmp/{} -C {}'.format(archive, path))
        sudo('rm /tmp/{}'.format(archive))
        sudo('mv {}/web_static/* {}'.format(path, path))
        sudo('rm -rf {}/web_static'.format(path))
        sudo('rm -rf {}'.format(current))
        sudo('ln -s {} {}'.format(path, current))
        print('New version deployed!')
        return True
    except Exception:
        return False
