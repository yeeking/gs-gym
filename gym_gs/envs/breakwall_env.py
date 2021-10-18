import gym
from gym import error, spaces, utils
from gym.utils import seeding

import pygame
import random
from random import randint
import numpy as np
import os

def getFilledRect(w,h,r,g,b):
  img = np.zeros((h,w,3),dtype=np.uint8)
  for x in range(len(img)): # rows
    for y in range(len(img[x])): # cols
      img[x][y][0] = r # R
      img[x][y][1] = g # G
      img[x][y][2] = b # B         
  image = pygame.image.frombuffer(img.tostring(), img.shape[1::-1], "RGB")
  return image

# Derives from the "Sprite" class in Pygame
class Ball(pygame.sprite.Sprite):
  def __init__(self,screen_width, screen_height):
    # Sprite super constructor
    super().__init__()

    # Init ball variables
    self.diameter = 10
    self.velocity = [random.choice([-3,-2,2,3]),1]
    self.maxSpeed = 6
    self.velocity_increment = -1
    
    # Load ball image and scale
    self.image = getFilledRect(self.diameter, self.diameter, 255, 255, 255)
    # Fetch the rectangle object that has the dimensions of the image
    self.rect = self.image.get_rect()
    
    # Position the ball in the middle
    self.rect.x = screen_width/2
    self.rect.y = screen_height/2
    
  # Update ball speed
  def update(self):
    self.rect.x += self.velocity[0]
    self.rect.y += self.velocity[1]
  
  # Collision with paddle
  def bounceOffPaddle(self,paddle):
    # Check collision with paddle
    if pygame.sprite.collide_mask(self, paddle):
      # If left paddle collision
      if (self.rect.x > paddle.rect.x + (paddle.width/2)):
        # Check velocity and bounce appropriately
        if (self.velocity[0]) < 0:
          self.velocity[0] = -self.velocity[0]
        else:
          self.velocity[0] = self.velocity[0]
      # If right paddle collision
      elif (self.rect.x < paddle.rect.x + (paddle.width/2)):
        # Check velocity and bounce appropriately
        if (self.velocity[0]) < 0:
          self.velocity[0] = self.velocity[0]
        else:
          self.velocity[0] = -self.velocity[0]
   
      # Increase speed up to maxSpeed
      if self.velocity[1] < self.maxSpeed:
        self.velocity[1] = -self.velocity[1] + self.velocity_increment
      else:
        self.velocity[1] = -self.velocity[1]

  # Collision with briks
  def bounceOffBriks(self,briks):
    # List of collisions with ball and brik group
    brick_collision_list = pygame.sprite.spritecollide(self,briks,False)
    # Check for collision and remove brik
    for brick in brick_collision_list:
      self.velocity[0] = self.velocity[0]
      self.velocity[1] = -self.velocity[1]
      brick.kill()
      return True

  # Collision with sides and upper wall
  def bounceOffWalls(self,screen_width,screen_height):
    if self.rect.x>=(screen_width-self.diameter):
        self.velocity[0] = -self.velocity[0]
    if self.rect.x<=0:
        self.velocity[0] = -self.velocity[0]
    if self.rect.y<=40:
        self.velocity[1] = -self.velocity[1]
  
  # Collision with ground
  def bounceOffGround(self,screen_height):
    if self.rect.y>(screen_height-self.diameter):
      self.velocity[1] = -self.velocity[1]
      return True
      
# Derives from the "Sprite" class in Pygame
class Brick(pygame.sprite.Sprite):
 
    def __init__(self):
        # Sprite super constructor
        super().__init__()

        # Init brick variables
        self.width = 60
        self.height = 20
        self.image = getFilledRect(self.width, self.height, 255, 0, 0)
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

import pygame

# Derives from the "Sprite" class in Pygame
class Paddle(pygame.sprite.Sprite):

  def __init__(self,screen_width,screen_height):
    # Sprite super constructor
    super().__init__()

    # Init paddle variables
    self.width = 100
    self.height = 10

    # Load paddle image and scale
    self.image = getFilledRect(self.width, self.height, 0, 255, 255)

    # Fetch the rectangle object that has the dimensions of the image.
    self.rect = self.image.get_rect()

    # Position the paddle in the middle
    self.rect.x = (screen_width/2) - (self.width/2)
    self.rect.y = screen_height - (self.height * 4)

  # Move paddle left
  def moveLeft(self, speed):
    self.rect.x -= speed
    # Constrain off-screen
    if self.rect.x < 0:
      self.rect.x = 0

  # Move paddle right        
  def moveRight(self, speed,screen_width):
    self.rect.x += speed
    # Constrain off-screen    
    if self.rect.x > (screen_width - self.width):
      self.rect.x = (screen_width - self.width)

# Utility function to initialise the bricks wall
def initBriksEasy(all_sprites_list,bricks_sprites_list):
  # Grid custom layout
  offset_x = 65
  offset_y = 25
  offest_row = 70
  rows = 8
  columns = 10
  # Used to load images for themed modes
  count = 1
  # Create grid of bricks
  for row in range(rows):
    for col in range(columns):
      # Create brick and position
      brick = Brick()
      brick.rect.x = 20 + (offset_x*col)+ brick.width
      brick.rect.y = offest_row + (offset_y*row)+brick.height
      # Add brick to all sprites group and briks group
      all_sprites_list.add(brick)
      bricks_sprites_list.add(brick)
      # Increase counter to load the next image on the brick 
      count+=1

# Utility function to initialise the bricks wall
def initBriks(all_sprites_list,bricks_sprites_list, rows=8,columns=12, col_width=65):
  # Grid custom layout
  offset_x = col_width
  offset_y = 25
  offest_row = 70

  # Used to load images for themed modes
  count = 1
  # Create grid of bricks
  for row in range(rows):
    for col in range(columns):
      # Create brick and position
      brick = Brick()
      brick.rect.x = (offset_x*col)
      brick.rect.y = offest_row + (offset_y*row)+brick.height
      # Add brick to all sprites group and briks group
      all_sprites_list.add(brick)
      bricks_sprites_list.add(brick)
      # Increase counter to load the next image on the brick 
      count+=1 

class BreakWallGame():
  def __init__(self):
    # Choose the game theme (Standard, Coursera, Authors)
    #game_theme = "Standard"

    # Initialise game environment variables
    self.screen_width = 65 * 12
    self.screen_height = 600
    #background_image = pygame.image.load("./images/background.png")
    self.background_image = getFilledRect(self.screen_width, self.screen_height, 0, 0, 0) # b g r
    
    self.reset()
    
    # Initialise game screen and caption
    pygame.init()
    self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))
    pygame.display.set_caption("Breawall")

  def reset(self):
    self.initial_score = 0
    self.game_over = False
    self.lives = 1
    
    # List of all the sprites used in the game
    self.all_sprites_list = pygame.sprite.Group()
    # List of all the bricks sprites
    self.bricks_sprites_list = pygame.sprite.Group()

    # Initialise paddle and ball
    self.paddle = Paddle(self.screen_width,self.screen_height)
    self.ball = Ball(self.screen_width,self.screen_height)

    # Add the paddle and the ball to the list of sprites
    self.all_sprites_list.add(self.paddle)
    self.all_sprites_list.add(self.ball)

    # Initialise wall of bricks
    # Display them in a grid
    initBriks(self.all_sprites_list,
              self.bricks_sprites_list)


  def step(self, action):
    """
    """
    assert action in ["NOOP", "FIRE", "LEFT", "RIGHT"], "Invalid action" + action
    if action == "LEFT":
      self.paddle.moveLeft(5)
    if action == "RIGHT":
      self.paddle.moveRight(5, self.screen_width)

    # Add background image
    #self.screen.blit(self.background_image, (0, 0))
    # faster way to make black background
    self.screen.fill([0, 0, 0])
    # # Update the sprites position
    self.all_sprites_list.update()

    # Check if the ball is bouncing against any of the 3 walls (left, right, top)
    self.ball.bounceOffWalls(self.screen_width,self.screen_height)

    # Check collision with bottom wall (ground)
    if self.ball.bounceOffGround(self.screen_height):
        self.lives -=1 # Remove one life
        if self.lives == 0:
            self.game_over = True

    # Check ball-paddle collision
    self.ball.bounceOffPaddle(self.paddle)

    # Check ball-bricks collision
    if self.ball.bounceOffBriks(self.bricks_sprites_list):
        self.initial_score+=1
   
    # Check win status
    if len(self.bricks_sprites_list) == 0:
        self.game_over=True

    # Draw all the sprites in the game
    self.all_sprites_list.draw(self.screen)

    # # Update full display screen
    pygame.display.flip()


  def getScreenRGB(self):
    # nicked this from Pygame-Learning-Environment
    # pix =  pygame.surfarray.array3d(
    #        pygame.display.get_surface()).astype(np.uint8)
    # pix = np.rot90(pix, 3) # rotate it 90x3 ->270  
    # 100 x faster version :) 
    # get raw framebuffer and convert to numpy
    pix = np.frombuffer(pygame.display.get_surface().get_buffer().raw, dtype=np.int8)
    # reshape to 3D array of RGBA
    pix = np.reshape(pix, [self.screen_height,self.screen_width,4])
    # this tricky bit reverses the order of the RGBA and loses the A
    pix = pix[:,:,2::-1] 
    #pix = np.rot90(pix, 3) # rotate it 90x3 ->270  
    return pix
    
#   def _get_image(self):
#   image_rotated = np.fliplr(np.rot90(self.game_state.getScreenRGB(),3)) #
# Hack to fix the rotated image returned by ple
#   return image_rotated



class BreakWall(gym.Env):
  """
  This is a simple, high level wrapper class for the breakwall game which presents it with an openai gym compatible interface as per:
  https://github.com/openai/gym/blob/master/docs/creating_environments.md
  """
  metadata = {'render.modes': ['human']}

  def __init__(self):
    # offscreen mode
    os.environ['SDL_VIDEODRIVER'] = 'dummy'
    self.game = BreakWallGame()
    self.viewer = None
    # these variables allow atari wrapper to work
    self._action_set = [0,1,3,4] # NOOP, FIRE, LEFT, RIGHT
    self.action_space = spaces.Discrete(len(self._action_set))
    self.observation_space = spaces.Box(low=0, high=255, shape=(self.game.screen_height, self.game.screen_width, 3), dtype=np.uint8)
    self.seed()

  
  
    # need this to provide a self.ale object with a lives function
    class ale:
      def __init__(self, game):
        self.game = game 
      def lives(self):
        return self.game.lives
    self.ale = ale(self.game)

  
    self.ACTION_MEANING = {
    0: "NOOP",
    1: "FIRE",
    2: "UP",
    3: "RIGHT",
    4: "LEFT",
    5: "DOWN",
    6: "UPRIGHT",
    7: "UPLEFT",
    8: "DOWNRIGHT",
    9: "DOWNLEFT",
    10: "UPFIRE",
    11: "RIGHTFIRE",
    12: "LEFTFIRE",
    13: "DOWNFIRE",
    14: "UPRIGHTFIRE",
    15: "UPLEFTFIRE",
    16: "DOWNRIGHTFIRE",
    17: "DOWNLEFTFIRE",
  }
  
  def step(self, action):
    """
    """
    start_score = self.game.initial_score
    action = self._action_set[action]
    self.game.step(self.ACTION_MEANING[action])
    state = self.game.getScreenRGB()
    end_score = self.game.initial_score
    reward = end_score - start_score
    terminal = self.game.game_over
    return state, reward, terminal, {}


  def seed(self, seed=None):
    self.np_random, seed1 = seeding.np_random(seed)

  def reset(self):
    self.game.reset()
    state = self.game.getScreenRGB()
    return state
    
  def render(self, mode='human'):
    """
    show the current screen
    """
    img = self.game.getScreenRGB()
    if mode == 'rgb_array':
        return img
    elif mode == 'human':
        from gym.envs.classic_control import rendering
        if self.viewer is None:
            self.viewer = rendering.SimpleImageViewer()
        self.viewer.imshow(img)

  def close(self):
    pass
  
  def get_action_meanings(self):
    """
    copied from atari_env.py
    """
    return [self.ACTION_MEANING[i] for i in self._action_set]



