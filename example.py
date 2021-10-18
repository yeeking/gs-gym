import gym
env = gym.make('gym_gs:breakwall-v0')
env.reset()
print("running ")
for i in range(1000): 
    if i % 100 == 0: print(i)
    env.step(1)
    #env.render()
