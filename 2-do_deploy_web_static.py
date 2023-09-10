#!/usr/bin/python3
"""fabric svript deploy compress file """
from fabric.api import *
from datetime import datetime
import os


env.hosts = ["local", "54.237.107.99", "100.25.103.38"]
env.user = "ubuntu"


def do_pack():
    """ function that compress static web folder"""
    n = datetime.now()
    t = "web_static_.tgz".format(n.year, n.month, n.day, n.hour, n.minute, n.second)
    local("mkdir -p versions")
    with lcd("./versions"):
        res = local("tar -czvf {} ../web_static".format(t))
        if res.succeeded:
            return "versions/{}".format(t)
    return None


def change(cmd, archive_path):
    file_name = archive_path.split("/")[-1]
    remote_path = "/tmp/{}".format(file_name)
    folder_old = "/data/web_static/releases/web_static"
    folder_new = "/data/web_static/releases/{}".format(file_name.split('.')[0])

    res = cmd("tar -xzf {} -C /data/web_static/releases/".format(remote_path))
    if res.failed:
        return False

    res = cmd("rm {}".format(remote_path))
    if res.failed:
        return False

    res = cmd("rm /data/web_static/current")
    if res.failed:
        return False

    res = cmd("mv {} {}".format(folder_old, folder_new))
    if res.failed:
        return False

    res = cmd("ln -s {} /data/web_static/current".format(folder_new))
    if res.failed:
        return False

    print("New version deployed!")
    return True

def do_deploy(archive_path):
    """function that deploy the archive file """
    if not os.path.exists(archive_path):
        return False
    if env.host_string != "local":
        res = put(local_path=archive_path, remote_path="/tmp/")
        if res.failed:
            return False
        res = change(sudo, archive_path)
        if res is False:
            return False
    else:
        res = local("cp {} /tmp/".format(archive_path))
        if res.failed:
            return False
        res = change(local, archive_path)
        if res is False:
            return False

    return True
    print("success")
