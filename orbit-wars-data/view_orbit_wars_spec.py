from kaggle_environments import make

env = make("orbit_wars")
print("Configuration schema:")
import pprint
pprint.pprint(env.configuration)
