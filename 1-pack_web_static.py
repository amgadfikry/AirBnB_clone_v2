#!/usr/bin/python3
""" fabric script """
from datetime import datetime
from fabric.api import local, lcd


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
