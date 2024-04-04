#!/usr/bin/python3
# Fabfile to distribute an archive to a web server.

import os
from fabric.api import env, put, run

env.user = "ubuntu"
env.hosts = ['100.26.138.154', '100.25.202.2']

def do_deploy(archive_path):
    """Distributes an archive to a web server."""
    print(f"Starting deployment for archive: {archive_path}")

    if not os.path.isfile(archive_path):
        print(f"Archive path {archive_path} does not exist.")
        return False
    
    fullFile = os.path.basename(archive_path)
    folder = fullFile.split(".")[0]
    
    print(f"Uploading archive {fullFile} to /tmp/ on remote server.")
    upload_result = put(archive_path, f"/tmp/{fullFile}")
    if upload_result.failed:
        print(f"Failed to upload archive to /tmp/.")
        return False
    
    print("Deleting existing folder with archive, if it exists.")
    if run(f"rm -rf /data/web_static/releases/{folder}").failed:
        print("Failed to delete existing archive folder.")
        return False

    print("Creating new archive folder.")
    if run(f"mkdir -p /data/web_static/releases/{folder}").failed:
        print("Failed to create new archive folder.")
        return False

    print("Uncompressing archive.")
    if run(f"tar -xzf /tmp/{fullFile} -C /data/web_static/releases/{folder}").failed:
        print("Failed to uncompress archive.")
        return False

    print("Deleting uploaded archive from /tmp/ directory.")
    if run(f"rm /tmp/{fullFile}").failed:
        print("Failed to delete archive from /tmp/ directory.")
        return False

    print("Moving content out of web_static folder.")
    if run(f"mv /data/web_static/releases/{folder}/web_static/* /data/web_static/releases/{folder}/").failed:
        print("Failed to move content out of web_static folder.")
        return False

    print("Deleting now empty web_static folder.")
    if run(f"rm -rf /data/web_static/releases/{folder}/web_static").failed:
        print("Failed to delete empty web_static folder.")
        return False

    print("Deleting current symbolic link, if it exists.")
    if run("rm -rf /data/web_static/current").failed:
        print("Failed to delete current symbolic link.")
        return False

    print("Creating new symbolic link to new version.")
    if run(f"ln -s /data/web_static/releases/{folder}/ /data/web_static/current").failed:
        print("Failed to create symbolic link to new version.")
        return False

    print("New version successfully deployed!")
    return True

