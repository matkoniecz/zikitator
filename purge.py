import os
import config

if os.path.isdir(config.get_cache_location()):
    raise Exception("expected file")

if os.path.isfile(config.get_cache_location()):
    os.remove(config.get_cache_location())
