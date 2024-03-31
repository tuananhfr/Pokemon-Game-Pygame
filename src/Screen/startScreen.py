from Screen import Screen

from gameSettings import gameSettings

import pygame
import sys

class startScreen(Screen):
    """
    Represents the screen displayed at the start of the game.
    
    Attributes:
        bgStartScreen (pygame.Surface): The background image for the start screen.
        start_button_image (pygame.Surface): The image for the start button.
        play_button_rect (pygame.Rect): The rectangle area for the start button.
    """
    def __init__(self, game):
        """
        Initializes the start screen.

        :param self: The GameScreen object that this method is called on.
        :param game (Game): The Game object associated with this screen.
        """
        super().__init__(game)
        # Initialize variables screen
        self.bgStartScreen = pygame.image.load('assets/images/background/background.jpg')
        self.start_button_image = pygame.image.load("assets/images/button/play.png")
        self.play_button_rect = pygame.Rect((self.game.gameWidth - self.start_button_image.get_width()) // 2,
                                            (self.game.gameHeight - self.start_button_image.get_height()) // 2,
        
                                            self.start_button_image.get_width(), self.start_button_image.get_height())
        
        
        

        

        
    def display(self):
        """
        Displays the start screen.
        """
        # setup Music 
        self.game.start_music.play()
      
        # setup background Image
        
        self.bgStartScreen = pygame.transform.scale(self.bgStartScreen, (self.game.gameWidth, self.game.gameHeight))
        self.bgStartScreenRect = self.bgStartScreen.get_rect()

        self.game.screen.blit(self.bgStartScreen, (0, 0))
        # button start game
        self.game.screen.blit(self.start_button_image, self.play_button_rect)
        

        # blit sound on button
        image_width, image_height = self.game.sound_image.get_size()
        self.game.sound_rect = pygame.Rect(gameSettings.GAMEWIDTH - 15 - image_width, gameSettings.GAMEHEIGHT - 15 - image_height, image_width, image_height)             
        if self.game.sound_on:
            self.game.screen.blit(self.game.sound_image, self.game.sound_rect)
        else:
            self.draw_dark_image(self.game.sound_image, self.game.sound_rect, (120, 120, 120)) 
        pygame.display.flip()
    def handle_events(self, event):
        """
        Handles events for the start screen.

        
        :param event (pygame.event.Event): The event to handle.
        """
        if event.type == pygame.QUIT: pygame.quit(), sys.exit()          
        if event.type == pygame.MOUSEMOTION:
            if self.play_button_rect.collidepoint(event.pos):                      
                self.draw_dark_image(self.start_button_image, self.play_button_rect, (60, 60, 60))
            else:
                self.game.screen.blit(self.start_button_image, self.play_button_rect)
            if self.game.sound_on == True:
                if self.game.sound_rect.collidepoint(event.pos):                      
                    self.draw_dark_image(self.game.sound_image, self.game.sound_rect, (60, 60, 60))
                else: 
                    self.game.screen.blit(self.game.sound_image, self.game.sound_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game.sound_rect.collidepoint(event.pos) :
                
                if self.game.sound_on == True:
                    self.game.sound_on = False
                    pygame.mixer.music.set_volume(0)
                    pygame.mixer.music.set_volume(0)
                    self.game.click_sound.setVolume(0)
                    self.game.play_fail_sound.setVolume(0)
                    self.game.clicked_tile_sound.setVolume(0)
                    self.game.play_success_sound.setVolume(0)
                    self.game.game_over_music.setVolume(0)	
                    self.game.victory_music.setVolume(0)

                    self.draw_dark_image(self.game.sound_image, self.game.sound_rect, (120, 120, 120))
                

					
                else:
                    self.game.sound_on = True
                    pygame.mixer.music.set_volume(0.2)
                    self.game.click_sound.setVolume(0.2)
                    self.game.play_fail_sound.setVolume(0.2)
                    self.game.clicked_tile_sound.setVolume(0.2)
                    self.game.play_success_sound.setVolume(0.2)
                    self.game.game_over_music.setVolume(0.2)
                    self.game.victory_music.setVolume(0.2)

                    self.game.screen.blit(self.game.sound_image, self.game.sound_rect)

                

               
            if self.play_button_rect.collidepoint(event.pos):
                # Clicking on the "Play" button plays the intro music and transitions to the welcome screen
                self.game.click_sound.play()
                self.game.set_screen(self.game.play_screen)
                self.game.current_screen.display()
        pygame.display.flip()
            
                       
    def draw_dark_image(self,image, image_rect, color):
        """
        Draws a darkened version of the given image on the screen.

        :param self: The GameScreen object that this method is called on.
        :param image: The image to be darkened.
        :param image_rect: The rectangle that defines the position and size of the image.
        :param color: The color to be used to darken the image.
        """
        dark_image = image.copy()
        dark_image.fill(color, special_flags = pygame.BLEND_RGB_SUB)
        self.game.screen.blit(dark_image, image_rect)

