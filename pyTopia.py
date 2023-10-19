import pygame
import random

#game settings
grid_width = 180
grid_height = 90
TILE_SIZE = 10
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600 

background_colour = (100,100,100)
stationaryFoodColour = (66, 235, 14)
slowFoodColour = (230, 230, 23)
mediumFoodColour = (235, 128, 14)
fastFoodColour = (235, 40, 14)
playerColour = (16, 66, 204)
stationaryFoodCount = 50
slowfoodCount = 50
mediumFoodCount = 25
fastFoodCount = 10

#spawn slow food function
def foodSpawn():
    spawnCords_x = random.randint(0, grid_width)
    spawnCords_y = random.randint(0, grid_height)
    cords = [spawnCords_x, spawnCords_y]
    return cords

#move slow food function, screen wrap integrated
def moveFood(movement, foodList):
  for i in range(len(foodList)):
    if foodList[i][0] < grid_width and foodList[i][0] > 0:
        foodList[i][0] += random.randint(-movement, movement)
    elif foodList[i][0] >= grid_width:
        foodList[i][0] = 1
    elif foodList[i][0] == 0:
        foodList[i][0] = (grid_width - 1)

    if foodList[i][1] < grid_height and foodList[i][1] > 0:                   
        foodList[i][1] += random.randint(-movement, movement)
    elif foodList[i][1] >= grid_height:
        foodList[i][1] = 1
    elif foodList[i][1] == 0:
        foodList[i][1] = (grid_height - 1)


#consume a food when the player walks over it
def eatFood(foodType):
    for i in range(len(foodType)):
        if foodType[i][0] == player_x and foodType[i][1] == player_y:        
            del foodType[i]
            break   


#draw all food in the screen
def drawFood(foodColour, foodList):
    for j in range(len(foodList)):
        pygame.draw.circle(screen, foodColour, (foodList[j][0]*TILE_SIZE+TILE_SIZE/2, foodList[j][1]*TILE_SIZE+TILE_SIZE/2), TILE_SIZE/3) 


# Initialize pygame 
pygame.init()


# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Calculate window size based on number of tiles 
WINDOW_WIDTH = TILE_SIZE * grid_width
WINDOW_HEIGHT = TILE_SIZE * grid_height


# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) 


#setup player
player_x = 90 
player_y = 45


#setup food
stationaryFoodList = []
slowFoodList = []
mediumFoodList = []
fastFoodList = []

for i in range(slowfoodCount):
  slowFoodList.append([foodSpawn()[0], foodSpawn()[1]])

for j in range(mediumFoodCount):
   mediumFoodList.append([foodSpawn()[0], foodSpawn()[1]])

for k in range(stationaryFoodCount):
   stationaryFoodList.append([foodSpawn()[0], foodSpawn()[1]])

for l in range(fastFoodCount):
   fastFoodList.append([foodSpawn()[0], foodSpawn()[1]])


# Generate the tile field 
tile_field = [[background_colour for i in range(300)] for j in range(300)] 

# we will need to generate food
# stationary food, movement = 0 tile per player move (herbivore) +5 hunger
# slow moving food, movement = 1 tile per player move (scavenger) +20 hunger
# medium moving food, movement = 2 tile per player move ( ) + 35 hunger
# fast moving food , movement = 3 tiles per player move (predetor) +50 hunger
# Set the player's position

# our little dot needs some rules
#hunger
    #hunger 0-100, if hunger at 0 player dies
    #reward each hour player does not starve to death
#energy
    #energy 0-100, energy is needed to move, 1 energy = 1 tile
    #energy is slowly gained by reducing hunger
#age
    #age 0-100
    #age 0-20 can move 1 tile and consume 1 hunger
    #age 20-40 can move 2 tiles and consume 1 hunger, 20 energy to reproduce
    #age 40-60 can move 2 tiles and consume 2 hunger, 30 energy to reproduce
    #age 60-80 can move 1 tile and consume 2 hunger, 40 energy to reproduce
    #age 80-100 can move 1 tile and consume 3 hunger, 50 energy to reproduce
#reproduce
    #if age >= 20 and energy >= 20: reproduce and give birth to random number between floor energy/cost to reproduce
#grow
    #if consumed > 10, move + 1 tiles
    #if consumed > 25, move + 2 tiles
    #if consumed > 50, move + 3 tiles
    #if consumed > 100, move + 4 tiles
#vision range

################################################# Game loop #################################################

running = True
while running:
  

  # Handle events
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

      
    # Player movement  
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_w or event.key == pygame.K_UP:
        player_y -= 1
        moveFood(1, slowFoodList)
        moveFood(2, mediumFoodList)
        moveFood(3, fastFoodList)
      elif event.key == pygame.K_s or event.key == pygame.K_DOWN: 
        player_y += 1
        moveFood(1, slowFoodList)
        moveFood(2, mediumFoodList)
        moveFood(3, fastFoodList)
      elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
        player_x -= 1
        moveFood(1, slowFoodList)
        moveFood(2, mediumFoodList)
        moveFood(3, fastFoodList)
      elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
        player_x += 1
        moveFood(1, slowFoodList)
        moveFood(2, mediumFoodList)
        moveFood(3, fastFoodList)


  # Draw the tile field
  for y in range(300):
    for x in range(300):
      pygame.draw.rect(screen, tile_field[y][x], (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
      pygame.draw.rect(screen, background_colour, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


  # Draw player    
  pygame.draw.circle(screen, playerColour, (player_x*TILE_SIZE+TILE_SIZE/2, player_y*TILE_SIZE+TILE_SIZE/2), TILE_SIZE/3)

  # move player auto

  
  #eat food
  eatFood(slowFoodList)
  eatFood(mediumFoodList)
  eatFood(fastFoodList)
  eatFood(stationaryFoodList)    


  # Draw all food
  drawFood(slowFoodColour, slowFoodList)
  drawFood(mediumFoodColour, mediumFoodList)
  drawFood(fastFoodColour, fastFoodList)
  drawFood(stationaryFoodColour, stationaryFoodList)
  
  pygame.display.update()
  
pygame.quit()