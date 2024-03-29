import sys
import pygame
from ObjectsInSpace import *


class Game:
    def __init__(self, screen: pygame.Surface):

        # screen size for convenience during initialization

        """at some point, the screen should be abstracted away from the Game class
        presently, we're doing the rendering and the handling of each "game" in the class
        itself.  this is fine, but it results in duplicate code here and in either the "menu.py"
        file or in the "main.py" file.  Ultimately, we should try to DRY ourselves with this
        code.


        update 9/7/21  refactoring this code to pass a surface object to this class to do work on it

        """

        # handling the screen
        self.max_screen_x = screen.get_width()
        self.max_screen_y = screen.get_height()
        self.screen = screen

        # sprite Group
        self.space_objects = pygame.sprite.Group()

        # game clock
        self.clock = pygame.time.Clock()

        """score and gameplay stuff here
        obviously we'll adjust this when we add multiplayer
        but for now, it's simple, self.alive controls the main while loop
        and score is the score!"""
        self.score = 0
        self.playing = True
        self.results = "Game Over"  # the main loop will return this variable when the game is complete

        # text default stuff below

        # we need a font for Pygame, change your fonts here
        self.font = pygame.font.Font('freesansbold.ttf', 32)

        # let's set up the text box for the health readout
        self.health_readout = self.font.render('Health: 100%', True, (255, 0, 0), (255, 255, 255))
        self.health_readout_rect = self.health_readout.get_rect()
        self.health_readout_rect.centery = self.max_screen_y - self.health_readout_rect.height
        self.health_readout_rect.centerx = self.health_readout_rect.width

        """
        let's set up a text box for your score
        this is basically duplicate code from above, but the names and colors are slightly different
        not exactly DRY, but writing a function to generate this for only a few things seems like more
        work than just making a score readout"""
        self.score_readout = self.font.render('Score: 0', True, (0, 255, 0), (255, 255, 255))
        self.score_readout_rect = self.score_readout.get_rect()
        self.score_readout_rect.centery = self.max_screen_y - self.score_readout_rect.height
        self.score_readout_rect.centerx = self.max_screen_x - self.score_readout_rect.width

    def main_loop(self):

        while self.playing:

            # get all the events, and process every one
            for event in pygame.event.get():
                self._process_events(event)

            # controls processes here:
            # first process keyboard controls:
            for sprite in [sprite for sprite in self.space_objects if sprite.is_controllable]:
                # go through each key press that a controllable vehicle has and execute the command
                sprite.keys_to_control_inputs(self.space_objects)

            self._process_network_controls()

            # networking to control game state here
            self._send_network_commands()
            self._receive_network_commands()

            # sprite collision, physics stuff, etc can go in this function
            self._process_game_logic()

            # draw the scene on the screen
            self._draw()

            # now tick the clock forward
            self.clock.tick(60)

        # Finally, return the game results from playing.
        return self.results

    def _process_network_controls(self) -> None:
        """
        Network controls will be processed here.
        This should be roughly analogous to the _process_keyboard_controls method

        """
        pass

    def _send_network_commands(self) -> None:
        """
        This is where the network send commands will live.
        """
        pass

    def _receive_network_commands(self) -> None:
        """
        We'll receive the network commands here to update the game state.
        """
        pass


    def _process_events(self, event) -> None:

        # first, let's process the process of properly quitting pygame
        if event.type == pygame.QUIT:
            """
            first let's kill the loop running the variable
            why?  Well - I'd imagine there's some multi threading under the hood
            and God knows what processes will still be running, let's make sure
            there's not a chance to loop through again, as Ripley would say
            nuke it from orbit, it's the only way to be sure
            i'll add that after adding this event handler"""

            pygame.quit()
            sys.exit()  # finally, let's kill everything that's left

    def _process_game_logic(self):
        # start with processing the simple physics
        # delete object list
        delete_list = []  # this list of sprites will be deleted at the end of this method
        add_list = []  # this is list of sprites will be added at the end of this method

        """ 
        rock_group is a sprite group that we can do logic on more conveniently
        we loop through the "space_objects" and add any SpaceBoulder to the
        rock group, we'll use this later to manage collisions
        we also create a laser group here to see measure the
        damage done to rocks"""
        rock_group = pygame.sprite.Group()
        bullet_group = pygame.sprite.Group()
        for obj in self.space_objects:
            if isinstance(obj, SpaceBoulder):
                rock_group.add(obj)
            if isinstance(obj, Bullet):
                bullet_group.add(obj)

        # now iterate through the objects in self.space_objects and perform logic on it
        for obj in self.space_objects:

            """
            let's warp the object back around if it goes outside the screen
            all this logic does is warp stuff to the opposite side of the screen
            if an object goes too far in one direction.  Effectively the geometry of
            this mini universe is toroidal"""
            if obj.rect.centerx > (self.max_screen_x + obj.rect.width):
                obj.rect.centerx = -obj.rect.width
            if obj.rect.centerx < -obj.rect.width:
                obj.rect.centerx = self.max_screen_x + obj.rect.width
            if obj.rect.centery > (self.max_screen_y + obj.rect.height):
                obj.rect.centery = -obj.rect.height
            if obj.rect.centery < -obj.rect.height:
                obj.rect.centery = self.max_screen_y + obj.rect.height

            # process the bullet logic first
            if isinstance(obj, Bullet):
                # let's check for collisions between the rock_group and bullets
                bullet_hit = pygame.sprite.spritecollide(obj, rock_group, False, pygame.sprite.collide_mask)
                if bullet_hit:
                    """
                    if there's a collision between a laser and and rock
                    then make a couple of debris rocks
                    then add the laser beam to the delete list"""
                    for i in range(5):
                        rock_debris = RockDebris(obj.rect)
                        rock_debris.create_rotation_map()
                        add_list.append(rock_debris)  # add this sprites to the list to be added

                    # let's add the score here
                    self.score += 100
                    self.score_readout = self.font.render(f'Score: {self.score}', True, (0, 255, 0), (255, 255, 255))
                    delete_list.append(obj)  # now get rid of the laser

            # now do boulder logic here
            if isinstance(obj, SpaceBoulder):
                # if the boulder's health is zero... add it to the delete list
                if obj.health <= 0:
                    """
                    if the health of a space boulder gets to zero, let's
                    make 4 pieces of debris to fly off"""
                    for i in range(4):
                        rock_debris = RockDebris(obj.rect)
                        rock_debris.create_rotation_map()
                        add_list.append(rock_debris)

                    delete_list.append(obj)

                # if a bullet object collides with a rock object...
                collide = pygame.sprite.spritecollide(obj, bullet_group, True, pygame.sprite.collide_mask)
                if collide:
                    obj.health -= 10  # take away 10 HP if a laser hits a rock

            # now we'll do player logic here
            if isinstance(obj, Player):
                if obj.health <= 0:
                    self.playing = False
                    self.results = (f"You have died.  Game Over.  Final Score: {self.score}", self.score)

                # check to see if the player ship has collided with the rocks
                collision = pygame.sprite.spritecollide(obj, rock_group, False, pygame.sprite.collide_mask)
                if collision:
                    # let's make some sparks if the ship collides with rocks
                    obj.health -= 1

                    for i in range(4):
                        spark = Spark(obj.rect)
                        spark.create_rotation_map()
                        add_list.append(spark)

                    # when the rock hits the ship, let's update the health
                    self.health_readout = self.font.render(f'Health: {obj.health}%', True, (255, 0, 0), (255, 255, 255))

            # Now we'll work with the RockDebris logic and spark logic
            # now we'll clean up sprites if they're out of range
            is_ranged = isinstance(obj, RockDebris) or isinstance(obj, Spark) or isinstance(obj, Bullet)
            if is_ranged:
                # rock debris is short lived, like bullets that don't do any damage
                # they disappear after a little bit, so do sparks, and bullets
                if obj.range <= 0:
                    delete_list.append(obj)

        # finally, we need to process the "winning" logic here
        if len(rock_group) == 0:
            self.playing = False  # end the game loop
            self.results = (f"You have won.  Congratulations!  Final Score: {self.score}", self.score)

        # now delete all the stuff that should be deleted
        for obj in delete_list:
            self.space_objects.remove(obj)

        for obj in add_list:
            self.space_objects.add(obj)

    def _draw(self):
        background_color = (0, 0, 255)
        self.screen.fill(background_color)

        # now let's update and draw all the sprites
        self.space_objects.update()
        self.space_objects.draw(self.screen)

        # now let's draw the player health and score
        self.screen.blit(self.health_readout, self.health_readout_rect)
        self.screen.blit(self.score_readout, self.score_readout_rect)

        pygame.display.flip()
