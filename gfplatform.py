#To play this game you need the proper images, so just download the .rar file you can find in this repository; then install the python "acrade" library


import arcade
import os
import random
import math

SPRITE_SCALING = 0.7
SPRITE_NATIVE_SIZE = 128

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000
SCREEN_TITLE = "the gluten free game"

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN = 40
RIGHT_MARGIN = 150

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 20
GRAVITY = 0.5
BOUNCINESS = 0.9
class bounce(arcade.Sprite): #define the physics of first type of enemy, the bouncing one
	def __init__(self, filename, sprite_scaling):

		super().__init__(filename, sprite_scaling)

		self.change_x = 0
		self.change_y = 0
		self.rimbalzi=0
	def update(self):
		self.center_x += self.change_x
		self.center_y += self.change_y
		if self.bottom < 106.65 or self.top > SCREEN_HEIGHT :
			self.change_y *= -1
		if self.rimbalzi < 2 :
			if self.center_x < 0 or self.center_x > SCREEN_WIDTH :
				self.change_x *= -1
				self.rimbalzi += 1

class shoot(arcade.Sprite):#define the physics of first type of enemy, the UFO
	def __init__(self, filename, sprite_scaling):

		super().__init__(filename, sprite_scaling)
		self.count=0
	def update(self):
		self.count +=1
		start_x = self.center_x
		start_y = self.center_y

		# Get the destination location for the bullet
		dest_x = self.aim.center_x
		dest_y = self.aim.center_y

		# Do math to calculate how to get the bullet to the destination.
		# Calculation the angle in radians between the start points
		# and end points. This is the angle the bullet will travel.
		x_diff = dest_x - start_x
		y_diff = dest_y - start_y
		self.angle2 = math.atan2(y_diff, x_diff)

		# Set the enemy to face the player.
		self.angle = math.degrees(self.angle2) -90



class MyGame(arcade.Window):
	""" Main application class. """

	def __init__(self):

		super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

		# Set the working directory (where we expect to find files) to the same
		# directory this .py file is in. You can leave this out of your own
		# code, but it is needed to easily run the examples using "python -m"
		# as mentioned at the top of this program.
		file_path = os.path.dirname(os.path.abspath(__file__))
		os.chdir(file_path)
		self.limiti= None
		self.caso=0
		# Sprite lists
		self.player_list = None
		self.wall_list = None
		self.enemy_list = None
		# Set up the player
		self.player_sprite = None
		self.frame_count=0
		self.physics_engine = None
		self.view_left = 0
		self.view_bottom = 0
		self.game_over = False
		self.score = 0
		self.vel=0
	def setup(self):
		""" Set up the game and initialize the variables. """

		# Sprite lists
		self.player_list = arcade.SpriteList()
		self.wall_list = arcade.SpriteList()
		self.enemy_list = arcade.SpriteList()
		self.nave_list = arcade.SpriteList()
		# Set up the player
		self.player_sprite = arcade.Sprite("images/main2.png",
										SPRITE_SCALING)

		# Starting position of the player
		self.player_sprite.bottom=106.65
		self.player_sprite.center_x = 750
		self.player_sprite.center_y = 270
		self.player_list.append(self.player_sprite)
		self.score = 0
		self.vel=0
		# Draw the walls on the bottom
		for x in range(0, SCREEN_WIDTH, int(SPRITE_NATIVE_SIZE * SPRITE_SCALING)):
			wall = arcade.Sprite("images/wheat_field.png", 0.7)

			wall.bottom = 0
			wall.left = x
			self.wall_list.append(wall)

		self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,self.wall_list,
															gravity_constant=GRAVITY)

		# Set the background color
		arcade.set_background_color(arcade.color.AMAZON)

	def on_draw(self):
		"""
		Render the screen.
		"""

		# This command has to happen before we start drawing
		arcade.start_render()

		# Draw all the sprites.
		self.player_list.draw()
		self.wall_list.draw()
		self.enemy_list.draw()
		output = f"Score: {round(self.score)}"
		arcade.draw_text(output, 10, 75, arcade.color.BLACK, 20)
	def on_key_press(self, key, modifiers):

		if key == arcade.key.UP:
			if self.physics_engine.can_jump():
				self.player_sprite.change_y = JUMP_SPEED
		elif key == arcade.key.LEFT:
			self.limiti= 1 
			self.player_sprite.change_x = -MOVEMENT_SPEED
		elif key == arcade.key.RIGHT:
			self.limiti= 0 
			self.player_sprite.change_x = MOVEMENT_SPEED

	def on_key_release(self, key, modifiers):

		if key == arcade.key.LEFT and self.limiti== 1 or key == arcade.key.RIGHT and self.limiti==0:
			self.player_sprite.change_x = 0
			
			
			#######creating the different enemies
	def bounce(self):
		self.rimb=bounce("images/pane2.png",0.2)
		self.rimb.center_x=random.choice([1,SCREEN_WIDTH])
		self.rimb.center_y=950
		if self.rimb.center_x == 1 :
			self.rimb.change_x = 5 + self.vel
		else:
			self.rimb.change_x = -5 - self.vel
		self.rimb.change_y= -10
		self.enemy_list.append(self.rimb)
		
	def roll(self):
		self.rotolo=arcade.Sprite("images/pane.png",0.2)
		self.rotolo.bottom=106.65
		self.rotolo.center_x=random.choice([1,SCREEN_WIDTH])
		self.rotolo.angle = random.randrange(360)
		if self.rotolo.center_x==1 :
			self.rotolo.change_x = 6 + self.vel
			self.rotolo.change_angle = -6
		else:
			self.rotolo.change_x = -6 - self.vel
			self.rotolo.change_angle = 6
		self.rotolo.angle = random.randrange(360)
		self.enemy_list.append(self.rotolo)
	def astrobarca(self):

		self.nave=shoot("images/ufo.png",0.05)
		self.nave.center_x=random.randrange(SCREEN_WIDTH)
		self.nave.center_y=950
		self.nave.aim=self.player_sprite
		self.nave_list.append(self.nave)
		self.enemy_list.append(self.nave)

	def spara(self,nave):
	
			if self.frame_count % 60 == 0 :
				self.bullet=arcade.Sprite("images/baguette.png",0.2)
				self.bullet.center_x = nave.center_x
				self.bullet.center_y = nave.center_y

				# Angle the bullet sprite
				self.bullet.angle = nave.angle 

				# Taking into account the angle, calculate our change_x
				# and change_y. Velocity is how fast the bullet travels.
				self.bullet.change_x = math.cos(nave.angle2) * (6 + self.vel)
				self.bullet.change_y = math.sin(nave.angle2) * (6 + self.vel)
				self.enemy_list.append(self.bullet)

	def enemy(self): #this chose what type of enemy will pop up
		self.caso=random.randint(1,3)
		if self.caso ==1:
			self.bounce()
		elif self.caso==2:
			self.roll()
		elif self.caso== 3:
			self.astrobarca()


	def update(self, delta_time):
		""" Movement and game logic """
		self.frame_count += 1
		self.score += 0.1
		if self.player_sprite.right > SCREEN_WIDTH and self.limiti == 0 or self.player_sprite.left < 0 and self.limiti ==1  : 
			self.player_sprite.change_x = 0
		if self.score < 100:
			if self.frame_count % 150 == 0:
				self.enemy()
		else:
			if self.frame_count % 100 == 0:
				self.vel=1
				self.enemy()
				
		self.enemy_list.update()
		bad_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.enemy_list)
		if len(bad_hit_list) > 0 :
			arcade.pause(2)
			self.setup()
		self.nave_list.update()
		if self.caso == 3:
			
			for i in self.nave_list :
					self.spara(i)
		else:
			for i in self.nave_list:
				i.kill()
			
		# Update the player based on the physics engine
		if not self.game_over:
			self.physics_engine.update()


def main():
	window = MyGame()
	window.setup()
	arcade.run()


if __name__ == "__main__":
	main()
