#from os.path import join
import os

def get_cache_name():
	return 'demo_cache'


def get_cache_location():
	return get_cache_name() + '.sqlite' 

def get_token_location():
	return os.path.join(os.environ['HOME'], 'Documents/Tokens/github-private-repositories.txt')

def get_location_of_file_with_ccordinates():
	return  os.path.join(os.environ['HOME'], 'Documents/Tokens/my_real_world_location.json')
