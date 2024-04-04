#!/usr/bin/python3
"""
This Fabric script automates the deployment process in three stages:
1. do_pack: Creates a .tgz archive from the web_static directory.
2. do_deploy: Uploads the archive to the web servers and sets it up.
3. deploy: Executes do_pack and then do_deploy.
Usage:
    fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
"""
from fabric.api import local, env, put, run
from datetime import datetime
from os.path import exists, isdir

# Define the IP addresses of your two web servers
env.hosts = ['100.26.138.154', '100.25.202.2']

def do_pack():
    """
    Packs the 'web_static' directory into a .tgz archive
    under the 'versions' directory.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir versions")
        file_name = f"versions/web_static_{date}.tgz"
        # Creates the archive using tar command
        local(f"tar -cvzf {file_name} web_static")
        return file_name
    except Exception as e:
        print(f"Error: {e}")
        return None

def do_deploy(archive_path):
    """
    Deploys the archive to the web servers:
    - Uploads the archive
    - Unpacks it
    - Sets up the web server directories
    - Updates the symbolic link to the 'current' version
    """
    if not exists(archive_path):
        return False
    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')
        
        # Prepares the directory where the archive will be unpacked
        run(f'mkdir -p {path}{no_ext}/')
        
        # Unpacks the archive
        run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')
        
        # Cleans up the archive from /tmp
        run(f'rm /tmp/{file_n}')
        
        # Moves the unpacked content to the correct location and cleans up
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')
        
        # Updates the symbolic link to point to the new version
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')
        
        return True
    except Exception as e:
        print(f"Deployment error: {e}")
        return False

def deploy():
    """
    Executes the deployment process: packing and then deploying.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)

