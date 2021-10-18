# Goldsmiths openai gym envs

We created some envs for AIs to play in, since we cannot show the original Atari games due to copyright. 

To install:

```
pip install -e .
```

To try it out:
```
import gym
env = gym.make('gym_gs:breakwall-v0')
env.reset()
env.step(1)
```
