#!/usr/bin/python3
"""fabric svript deploy compress file """
from fabric.api import *
import os


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
    if os.path.exists(archive_path) is False:
        return False
    try:
        put(archive_path, "/tmp")
        file_name = archive_path.split("/")[-1]
        t_path = f"/tmp/{file_name}"
        with cd("/data/web_static/releases/"):
            res = sudo(f"tar -xzvf {t_path}")
        sudo(f"rm {t_path}")
        sudo("rm -rf /data/web_static/current")
        folder_old = "/data/web_static/releases/web_static"
        folder_new = f"/data/web_static/releases/{file_name.split('.')[0]}"
        sudo(f"mv {folder_old} {folder_new}")
        sudo(f"ln -s {folder_new} /data/web_static/current")
        return True
    except Exception:
        return False
