# -------------------------------------------------------------------------
# Made with LOVE By Gilad Gershon
# Licensed under the MIT License.
# --------------------------------------------------------------------------
from webapp.webapp import app
from pathlib import Path
import os
from decouple import config
local_or_docker  = config("LOCAL_OR_DOCKER")

path_to_file = '6379.conf'
path = Path('./6379.conf')

__all__ = ["app"]

#in case of docker container - start Redis server when the container is start, then delete 6379.conf
if local_or_docker == 'docker':
 if path.is_file():
    print(f'The file {path_to_file} exists')
    print('Starting Redis..')
    os.system('redis-server /usr/local/etc/redis/6379.conf')
    os.remove("./6379.conf")