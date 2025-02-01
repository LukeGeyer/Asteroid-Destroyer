import pygame
import sys
import random

pygame.init()

window_width = 800
window_height = 600

screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Asteroid_Destroyer')
bg = pygame.image.load('Assets/SpaceBG.png').convert() #load back ground
spaceship = pygame.image.load('Assets/SpaceShip200x.png').convert_alpha() #load image for spaceship (convert alpha ensure transparent background of the png)
asteroid = pygame.image.load('Assets/Asteroid200x.png').convert_alpha() 

run = True #Game is running if run is set to true

#Define game variables ================================
asteroid_speed = 0.2
asteroidPos = 600

spaceship_gravity = 0.0005
spaceship_velocity = 0  # Initial velocity (starts from 0, and increases with gravity)
gravity_direction = 1 # 1 for down and -1 for up
collision_time = None
collision_detected = False

spaceship_height = window_height / 2
spaceship_width = window_height / 2 - 200 

game_over_text_font = pygame.font.SysFont('Arial', 50, True, False)
score_text_font = pygame.font.SysFont('Arial', 25, True, False)

score = 0
passed_asteroids = False #Flag to check if player has passed a row of asteroids.
#=======================================================

#Asteroid Class
class Asteroid:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.image = asteroid
        self.rect = self.image.get_rect(topleft=(self.x, self.y))# For collision detection

        # Resize the rect for more accurate collision detection
        self.rect = self.rect.inflate(-50, -50)  # Shrink the rectangle by 50 pixels on each side

    
    def move(self): 
        self.x -= self.speed
        self.rect.x = self.x
        # If the asteroid moves off the left side of the screen, reset it
        if self.x < -200:
            self.x = window_width
            self.y = random.randint(50, window_height - 50)  # Random Y spawn position
            self.rect.y = self.y  # Update the rectangle position
            self.speed = asteroid_speed

            global passed_asteroids
            passed_asteroids = False # Reset flag for next row of asteroids.

    def draw(self, screen):
        screen.blit(asteroid, (self.x, self.y))


# Define game functions=================================
def draw_spaceship(x_pos, y_pos):
    screen.blit(spaceship, (x_pos, y_pos))

def gravity():
    global spaceship_height, spaceship_velocity
    spaceship_velocity += spaceship_gravity * gravity_direction  # Increase velocity due to gravity
    spaceship_height += spaceship_velocity  # Update the spaceship's vertical position

    # Prevent the spaceship from falling below the screen
    if spaceship_height > window_height - spaceship.get_height():
        spaceship_height = window_height - spaceship.get_height()  # Stop at the bottom of screen
        spaceship_velocity = 0  # Stop the velocity when it hits the bottom of screen

    # Prevent the spaceship from going off the top of the screen
    if spaceship_height < 0:
        spaceship_height = 0  # Stop at the top of the screen
        spaceship_velocity = 0  # Stop the velocity when it hits the top of the screen

def check_collision(spaceship_rect, asteroids):
    for asteroid in asteroids:
        if spaceship_rect.colliderect(asteroid.rect):  # Check if the spaceship and asteroid collide
            return True  # Collision detected
    return False  # No collision

def draw_text(text, font, colour, x,y):
    image = font.render(text, True, colour)
    screen.blit(image, (x,y))

def update_score():
    global score, passed_asteroids
    if spaceship_width + spaceship.get_width() > max(asteroid.x for asteroid in asteroids) and not passed_asteroids: #Check if spaceship passed the asteroids
        score += 1  # Increase the score
        print('Score:' + str(score))
        passed_asteroids = True #Flag to prevent multiple increments


##=======================================================

#Create list to store asteroids
asteroids = []

#Generate initial asteroids
for i in range(5):
    x_pos = random.randint(window_width, window_height + 200)
    y_pos = random.randint(50, window_height - 50)
    asteroids.append(Asteroid(x_pos, y_pos, asteroid_speed))

while run:

    screen.blit(bg, (0,0)) # draw background
    
    if not collision_detected:
        #Initialize player
        spaceship_rect = spaceship.get_rect(topleft=(spaceship_width, spaceship_height))  # Get the spaceship's rectangle
        spaceship_rect = spaceship_rect.inflate(-30, -30)  # Reduce the size of the collision rectangle for the spaceship
        draw_spaceship(spaceship_width, spaceship_height)
        gravity()

        #Draw score
        draw_text('Score: ' + str(score), score_text_font, (144, 238, 144), 20, 20)

        #Draw asteroids
        for asteroid_obj in asteroids:
            asteroid_obj.draw(screen)
            asteroid_obj.move() #Move asteroid

            # Check for collision
            if check_collision(spaceship_rect, asteroids):
                print("Collision detected! Game over!") 
                collision_time = pygame.time.get_ticks()
                collision_detected = True 
                break

        update_score()
        
    if collision_detected:
        draw_text('Game Over', game_over_text_font, (255, 0, 0), window_width/2-150, window_height/2-50)
        # Check if 2 seconds have passed
        if pygame.time.get_ticks() - collision_time >= 2000:
            run = False  # End the game after 2 seconds

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Player quits game
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Check for spacebar press
                gravity_direction *= -1  # Reverse gravity direction 

    pygame.display.update()


pygame.quit()