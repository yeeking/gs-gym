from gym.envs.registration import register

register(
    id='breakwall-v0',
    entry_point='gym_gs.envs:BreakWall',
)
register(
    id='BreakwallNoFrameskip-v1', 
    entry_point='gym_gs.envs:BreakWall',
)
# register(
#     id='foo-extrahard-v0',
#     entry_point='gym_foo.envs:FooExtraHardEnv',
# )