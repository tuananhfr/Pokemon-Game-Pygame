from Board.boardPlay import boardPlay
from Screen import Screen
from gameSettings import gameSettings
from algorithme.bfsAlgorithme import bfsAlgorithme
import random,time,sys
import pygame


class playScreen(Screen):
    """
    Class representing the gameplay screen of the Pikachu game.

    Attributes:
        game: The game object associated with the screen.
        backgroundList: List of background images for the gameplay screen.
        boardPlay: Instance of boardPlay for managing the game board.
        time_icon: Pygame surface representing the time icon.
        Time: Pygame clock for managing time.
        live_image: Pygame surface representing the life icon.
        list_level: List of level images.
        font_pikachu: Font object for rendering text.
        game_over_background: Pygame surface for the game over background.
        victory_background: Pygame surface for the victory background.
        pause_btn: Pygame surface for the pause button.
        pause_panel_image: Pygame surface for the pause panel.
        continue_btn: Pygame surface for the continue button.
        replay_btn: Pygame surface for the replay button.
        home_btn: Pygame surface for the home button.
    """
    def __init__(self, game):
        """
        Initialize the playScreen object.

        :param self: The GameScreen object that this method is called on.
        :param game: The game object associated with the screen.
        """
        super().__init__(game)
        # Variables for Game
        
        self.backgroundList = [pygame.transform.scale(pygame.image.load("assets/images/background/background-game/" + str(i) + ".jpg"), (gameSettings.GAMEWIDTH, gameSettings.GAMEHEIGHT)) for i in range(10)]

        self.boardPlay = boardPlay(self.game)
        #time
        self.time_icon = pygame.transform.scale(pygame.image.load("assets/images/tiles/section1.png"), (gameSettings.TILE_WIDTH, gameSettings.TILE_HEIGHT))
        self.Time = pygame.time.Clock()
        # lives
        self.live_image = pygame.transform.scale(pygame.image.load("assets/images/heart.png"), (50, 50))
        # level
        self.list_level = [pygame.transform.scale(pygame.image.load("assets/images/level/" + str(i) + ".png"), (50, 50)) for i in range(1, 10)]

        self.font_pikachu = pygame.font.Font("assets/font/pikachu.otf", 50)
        # button
        self.game_over_background = pygame.image.load("assets/images/background/gameover.png").convert_alpha()
        self.victory_background = pygame.image.load("assets/images/background/win.png").convert_alpha()

        self.pause_btn = pygame.transform.scale(pygame.image.load("assets/images/button/pause.png").convert_alpha(), (50, 50))
        self.pause_panel_image = pygame.transform.scale(pygame.image.load("assets/images/button/panel_pause.png"), (300, 200))
        self.continue_btn = pygame.image.load("assets/images/button/continue.png").convert_alpha()
        self.replay_btn = pygame.image.load("assets/images/button/replay.png")
        self.home_btn = pygame.image.load("assets/images/button/exit.png").convert_alpha()


    def display(self):  
        """
        Display the gameplay screen.
        """
        self.level = 1
        self.lives = 3         
        while self.level <= gameSettings.MAX_LEVEL:
            print("Current level:", self.level)
            random.shuffle(self.backgroundList)
            self.playing()
            self.level += 1
            pygame.time.wait(300)
                
            


    
    def playing(self):
        """
        Main gameplay loop.
        """
        # Pause
        self.paused = False
        # time
        self.time_start_paused = 0
        self.time_paused = 0

        # get random background
        self.game.bgPlayScreen = self.backgroundList[0]

        self.boardPlay = boardPlay(self.game)
        self.board = self.boardPlay.get_random_board()

        # mouse
        self.mouse_x,self.mouse_y = 0,0
        # store index cards clicked
        self.clicked_tiles = []

        self.hint = self.boardPlay.get_hint(self.board)

        # time
        self.start_time = time.time()
        self.bonus_time = 0

        self.last_time_get_point = time.time()
        while True:
            self.Time.tick(gameSettings.FPS)

            self.game.screen.blit(self.game.bgPlayScreen, (0, 0)) # set background
            width_dim_screen, height_dim_screen = self.game.screen.get_size()
            self.dim_screen = pygame.Surface((width_dim_screen, height_dim_screen), pygame.SRCALPHA)
            pygame.draw.rect(self.dim_screen, (0, 0, 0, 150), self.dim_screen.get_rect())
            self.game.screen.blit(self.dim_screen, (0, 0))
            self.boardPlay.draw_board(self.board)
            self.draw_lives(self.lives, self.level)
            self.draw_time_bar(self.start_time, self.bonus_time)
            self.boardPlay.draw_clicked_tiles(self.board, self.clicked_tiles)


            if self.game.sound_on:
                self.game.screen.blit(self.game.sound_image, self.game.sound_rect)
            else:
                self.draw_dark_image(self.game.sound_image, self.game.sound_rect, (120, 120, 120)) 
            
            self.mouse_clicked = False
            
            if self.lives == 0:
                self.show_dim_screen()
                self.level = gameSettings.MAX_LEVEL + 1
                
                
                self.game.game_over_music.play()            
                
                self.start_end = time.time()
                while time.time() - self.start_end <= gameSettings.TIME_END:
                    self.game_over_background = pygame.transform.scale(self.game_over_background, (gameSettings.GAMEWIDTH//2, gameSettings.GAMEHEIGHT//2))
                    self.game.screen.blit(self.game_over_background, (gameSettings.GAMEWIDTH//4, gameSettings.GAMEHEIGHT//6))
                    pygame.display.flip()

                    pygame.time.wait(6000)  # Wait for 6 seconds
                    self.game.set_screen(self.game.start_screen)
                    self.game.current_screen.__init__(self.game)
                    self.game.current_screen.display()
                return
            # check event
            for event in pygame.event.get():
                self.handle_events(event)

            self.sound_button(self.mouse_x, self.mouse_y, self.mouse_clicked)
            
            self.draw_pause_button(self.mouse_x, self.mouse_y, self.mouse_clicked)

            is_time_up = self.check_time(self.start_time, self.bonus_time) # 0 if game over, 1 if lives -= 1, 2 if nothing
            if self.paused:
                self.show_dim_screen()
                if is_time_up == 0: #game over
                    self.lives -= 1
                elif is_time_up == 1:
                    self.lives -= 1                    
                    return

                select = self.panel_pause(self.mouse_x, self.mouse_y, self.mouse_clicked) # 0 if click replay, 1 if click home, 2 if continue, 3 if nothing
                if select == 0: 
                    self.lives -= 1
                    if self.lives > 0:					    
                        return
                    
                elif select == 1:
                    self.level = gameSettings.MAX_LEVEL + 1
                    return 
                elif select == 2:                   
                    self.mouse_clicked = False


            # check time get hint
            if time.time() - self.last_time_get_point - self.time_paused > gameSettings.HINT_TIME and not self.paused: self.boardPlay.draw_hint(self.hint)			
            #update
            try:
                tile_i, tile_j = self.get_index_at_mouse(self.mouse_x, self.mouse_y)
                if self.board[tile_i][tile_j] != 0 and not self.paused:                   
                    self.boardPlay.draw_border_tile(self.board,tile_i, tile_j)
                    if self.mouse_clicked:
                        self.mouse_clicked = False
                        self.clicked_tiles.append((tile_i, tile_j))
                        self.boardPlay.draw_clicked_tiles(self.board, self.clicked_tiles)
                        if len(self.clicked_tiles) == 1:
                            self.game.clicked_tile_sound.play()

                        if len(self.clicked_tiles) > 1: # 2 cards was clicked 
                            path = bfsAlgorithme.algo(self.board, self.clicked_tiles[0][0], self.clicked_tiles[0][1], tile_i, tile_j)
                            if path:
				    			# delete the same card
                                self.board[self.clicked_tiles[0][0]][self.clicked_tiles[0][1]] = 0
                                self.board[tile_i][tile_j] = 0
                                self.game.play_success_sound.play() 
                                self.boardPlay.draw_path(path)

                                self.bonus_time += 1
                                self.last_time_get_point = time.time() # count time hint
				    			# if level > 1, upgrade difficulty by moving cards 
                                self.update_difficulty(self.board, self.level, self.clicked_tiles[0][0], self.clicked_tiles[0][1], tile_i, tile_j)
                                if self.is_level_complete(self.board):
                                    if self.level == 5:
                                        self.show_dim_screen()
                                        self.level = gameSettings.MAX_LEVEL + 1

                                        pygame.mixer.music.pause()
                                        self.game.victory_music.play()
                                        self.victory_background = pygame.transform.scale(self.victory_background, (gameSettings.GAMEWIDTH, gameSettings.GAMEHEIGHT))
                                        self.game.screen.blit(self.victory_background, (0,0))
                                        pygame.display.flip()

                                        pygame.time.wait(8000)  # Wait for 6 seconds
                                        self.game.set_screen(self.game.start_screen)
                                        
                                        self.game.current_screen.display()     
                                    return
 
				    			# if hint got by player
                                if not(self.board[self.hint[0][0]][self.hint[0][1]] != 0 and bfsAlgorithme.algo(self.board, self.hint[0][0], self.hint[0][1], self.hint[1][0], self.hint[1][1])):
                                    self.hint = self.boardPlay.get_hint(self.board)
                                    while not self.hint:
                                        pygame.time.wait(100)
                                        self.boardPlay.reset_board(self.board)
                                        self.hint = self.boardPlay.get_hint(self.board)
                            else:
                                if not (self.clicked_tiles[0][0] == self.clicked_tiles[1][0] and self.clicked_tiles[0][1] == self.clicked_tiles[1][1]):
                                    self.game.play_fail_sound.play()
                            #reset
                            self.clicked_tiles = []
            except: pass
            pygame.display.flip()
            

    def check_time(self,start_time,bonus_time):
        """
        Check if the time is up and update game status accordingly.

        :param self: The GameScreen object that this method is called on.
        :param start_time: The start time of the game.
        :param bonus_time: Bonus time earned during the game.

        :return:
            int: 0 if game over, 1 if lives -= 1, 2 if nothing.
        """
        if self.paused: return 2	
	    # check game lost
        if time.time() - start_time - self.time_paused > gameSettings.GAME_TIME + bonus_time: # time up
            self.paused = True
            if self.lives <= 1: return 0
            return 1
        return 2

    def draw_time_bar(self,start_time, bonus_time):
        """
        Draw the time bar on the game screen to represent the remaining time.

        Args:
        :param self: The GameScreen object that this method is called on.
        :param start_time (int): The starting time of the game.
        :param bonus_time (int): Bonus time earned during the game.

        
        """
        pygame.draw.rect(self.game.screen, (255,255,255,5), (gameSettings.TIME_BAR_POS[0], gameSettings.TIME_BAR_POS[1], gameSettings.TIME_BAR_WIDTH, gameSettings.TIME_BAR_HEIGHT), 2, border_radius = 20)
        timeOut = 1 - (time.time() - start_time - bonus_time - self.time_paused) / gameSettings.GAME_TIME # ratio between remaining time and total time
        if self.paused:
            if not self.time_start_paused: self.time_start_paused = time.time()
            timeOut = 1 - (self.time_start_paused - start_time - bonus_time - self.time_paused) / gameSettings.GAME_TIME
        else:
            if self.time_start_paused:
                self.time_paused += time.time() - self.time_start_paused
                timeOut = 1 - (time.time() - start_time - bonus_time - self.time_paused) / gameSettings.GAME_TIME
            self.time_start_paused = 0

        # Calculate the width of the inner bar based on the time ratio
        inner_width = max(0, min(gameSettings.TIME_BAR_WIDTH * timeOut - 4, gameSettings.TIME_BAR_WIDTH - 4))
        innerPos = (gameSettings.TIME_BAR_POS[0] + 2, gameSettings.TIME_BAR_POS[1] + 2)
        innerSize = (inner_width, gameSettings.TIME_BAR_HEIGHT - 4)
        pygame.draw.rect(self.game.screen, "green", (innerPos, innerSize), border_radius=20)


    def draw_lives(self,lives, level):
        """
        Draw the lives bar on the game screen.

        Args:
        :param self: The GameScreen object that this method is called on.
        :param lives (int): The lives of the game.
        :param level (int): The level of the game.

        
        """
        self.game.screen.blit(self.live_image, (10, 12))
        lives_count = self.font_pikachu.render(str(lives), True, 'white')
        self.game.screen.blit(lives_count, (60, 13))

        self.game.screen.blit(self.list_level[level - 1], (gameSettings.GAMEWIDTH - 70, 12))

    def panel_pause(self,mouse_x, mouse_y, mouse_clicked):
        """
        Display the pause panel and handle button interactions when the game is paused.

        :param self: The GameScreen object that this method is called on.
        :param mouse_x (int): The x-coordinate of the mouse pointer.
        :param mouse_y (int): The y-coordinate of the mouse pointer.
        :param mouse_clicked (bool): A boolean indicating whether the mouse button is clicked.

        :return:
            int: An integer representing the action chosen:
                 - 0: Replay button clicked.
                 - 1: Home button clicked.
                 - 2: Continue button clicked.
                 - 3: No button clicked.
        """
        width_panel_rect, height_panel_rect = self.pause_panel_image.get_size()
        panel_rect = pygame.Rect(0, 0, width_panel_rect, height_panel_rect)
        panel_rect.center = (gameSettings.GAMEWIDTH / 2, gameSettings.GAMEHEIGHT / 2)
        self.game.screen.blit(self.pause_panel_image, panel_rect)


        width_continue_rect, height_continue_rect = self.continue_btn.get_size()
    
        continue_rect = pygame.Rect(0, 0, width_continue_rect, height_continue_rect)
        continue_rect.center = (panel_rect.centerx, panel_rect.centery)
        self.game.screen.blit(self.continue_btn, continue_rect)
        if continue_rect.collidepoint(mouse_x, mouse_y):
            self.draw_dark_image(self.continue_btn, continue_rect, (60, 60, 60))
            if mouse_clicked:
                self.draw_dark_image(self.continue_btn, continue_rect, (120, 120, 120))
                self.paused = False
                self.game.click_sound.play()
                return 2
        width_replay_rect, height_replay_rect = self.replay_btn.get_size()
        replay_rect = pygame.Rect(0, 0, width_replay_rect, height_replay_rect)
        replay_rect.center = (panel_rect.centerx - 80, panel_rect.centery)
        self.game.screen.blit(self.replay_btn, replay_rect)
        if replay_rect.collidepoint(mouse_x, mouse_y):
            self.draw_dark_image(self.replay_btn, replay_rect, (60, 60, 60))
            if mouse_clicked:
                self.paused = False
                self.draw_dark_image(self.replay_btn, replay_rect, (120, 120, 120))
                self.game.click_sound.play()
                return 0
            
        width_home_rect, height_home_rect = self.home_btn.get_size()
        home_rect = pygame.Rect(0, 0, width_home_rect, height_home_rect)
        home_rect.center = (panel_rect.centerx + 80, panel_rect.centery)
        self.game.screen.blit(self.home_btn, home_rect)
        if home_rect.collidepoint(mouse_x, mouse_y):
            self.draw_dark_image(self.home_btn, home_rect, (60, 60, 60))
            if mouse_clicked:
    
                self.draw_dark_image(self.home_btn, home_rect, (120, 120, 120))
                self.game.click_sound.play()
                self.game.set_screen(self.game.start_screen)
                self.game.current_screen.display()
                return 1

        return 3


    def draw_pause_button(self,mouse_x, mouse_y, mouse_clicked):
        """
        Display the pause button and handle interactions.

        :param self: The GameScreen object that this method is called on.
        :param mouse_x (int): The x-coordinate of the mouse pointer.
        :param mouse_y (int): The y-coordinate of the mouse pointer.
        :param mouse_clicked (bool): A boolean indicating whether the mouse button is clicked.
        """ 
        width, height = self.pause_btn.get_size()
        pause_rect = pygame.Rect(0, 0, width, height)      
        pause_rect.center = (gameSettings.GAMEWIDTH - 220, 35)
        self.game.screen.blit(self.pause_btn, pause_rect)
        if pause_rect.collidepoint(mouse_x, mouse_y):
            if not self.paused: self.draw_dark_image(self.pause_btn, pause_rect, (60, 60, 60))
            if mouse_clicked:
                mouse_clicked = False
                self.paused = True
                self.game.click_sound.play()

    def sound_button(self,mouse_x, mouse_y, mouse_clicked):
        """
        Handles the sound button behavior and drawing.

        :param self: The GameScreen object that this method is called on.
        :param mouse_x: The x coordinate of the mouse position.
        :param mouse_y: The y coordinate of the mouse position.
        :param mouse_clicked: A boolean indicating whether the mouse button is clicked.
        """
        if self.game.sound_on:
            if self.game.sound_rect.collidepoint(mouse_x, mouse_y):                      
                self.draw_dark_image(self.game.sound_image, self.game.sound_rect, (60, 60, 60))
                if mouse_clicked:
                    self.game.sound_on = False
                    pygame.mixer.music.set_volume(0)
                    self.game.click_sound.setVolume(0)
                    self.game.play_fail_sound.setVolume(0)
                    self.game.clicked_tile_sound.setVolume(0)
                    self.game.play_success_sound.setVolume(0)
                    self.game.game_over_music.setVolume(0)
                    self.game.victory_music.setVolume(0)

                    		       

                    self.draw_dark_image(self.game.sound_image, self.game.sound_rect, (120, 120, 120))   
            else: 
                self.game.screen.blit(self.game.sound_image, self.game.sound_rect)
           
                    
        else:
            if self.game.sound_rect.collidepoint(mouse_x, mouse_y):          
                if mouse_clicked:
                    self.game.sound_on = True
                    pygame.mixer.music.set_volume(0.2)
                    self.game.click_sound.setVolume(0.2)
                    self.game.play_fail_sound.setVolume(0.2)
                    self.game.clicked_tile_sound.setVolume(0.2)
                    self.game.play_success_sound.setVolume(0.2)
                    self.game.game_over_music.setVolume(0.2)
                    self.game.victory_music.setVolume(0.2)


                    self.game.screen.blit(self.game.sound_image, self.game.sound_rect)
    def show_dim_screen(self):
        """
        Displays a dimmed screen to give a "dimmed" effect to the screen.
        """
        self.dim_screen = pygame.Surface(self.game.screen.get_size(), pygame.SRCALPHA)
        pygame.draw.rect(self.dim_screen, (0, 0, 0, 220), self.dim_screen.get_rect())
        self.game.screen.blit(self.dim_screen, (0, 0))

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
    

    def get_index_at_mouse(self,x, y): # get index of card at mouse clicked from coords x, y
        """
        Returns the index of the card at the given mouse coordinates.

        :param self: The GameScreen object that this method is called on.
        :param x: The x coordinate of the mouse position.
        :param y: The y coordinate of the mouse position.
        :return: A tuple containing the row and column index of the card at the given mouse coordinates, or `None` if the mouse is not over a card.
        """
        if x < gameSettings.MARGIN_X or y < gameSettings.MARGIN_Y: return None, None
        return (y - gameSettings.MARGIN_Y) // gameSettings.TILE_HEIGHT, (x - gameSettings.MARGIN_X) // gameSettings.TILE_WIDTH

    def handle_events(self, event):
        """
        Handles the game events.

        :param self: The GameScreen object that this method is called on.
        :param event: A pygame event.
        """       
        if event.type == pygame.QUIT: pygame.quit(), sys.exit()
        if event.type == pygame.MOUSEMOTION:
            self.mouse_x, self.mouse_y = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_x, self.mouse_y = event.pos
            self.mouse_clicked = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_k: # use key k to hack game
                tile1_i, tile1_j = self.hint[0][0], self.hint[0][1]
                tile2_i, tile2_j = self.hint[1][0], self.hint[1][1]
                self.board[tile1_i][tile1_j] = 0
                self.board[tile2_i][tile2_j] = 0
                self.bonus_time += 1
                self.update_difficulty(self.board, self.level, tile1_i, tile1_j, tile2_i, tile2_j)
                if self.is_level_complete(self.board): return
                    
                if not(self.board[tile1_i][tile1_j] != 0 and bfsAlgorithme.algo(self.board, tile1_i, tile1_j, tile2_i, tile2_j)):
                    self.hint = self.boardPlay.get_hint(self.board)
                    while not self.hint:
                        pygame.time.wait(100)
                        self.boardPlay.reset_board(self.board)
                        self.hint = self.boardPlay.get_hint(self.board)
        
       
    
    def update_difficulty(self,board, level, tile1_i, tile1_j, tile2_i, tile2_j):
        """
        Updates the difficulty of the game based on the level.

        :param self: The GameScreen object that this method is called on.
        :param board: The current state of the game board.
        :param level: The current level of the game.
        :param tile1_i: The row index of the first tile.
        :param tile1_j: The column index of the first tile.
        :param tile2_i: The row index of the second tile.
        :param tile2_j: The column index of the second tile.
        """
        if level == 2: #all card move up
            for j in (tile1_j, tile2_j):
                new_column = [0]
                for i in range(gameSettings.BOARD_ROWS):
                    if board[i][j] != 0:
                        new_column.append(board[i][j])
                while(len(new_column) < gameSettings.BOARD_ROWS): new_column.append(0)
                for k in range(gameSettings.BOARD_ROWS):
                    board[k][j] = new_column[k]
        if level == 3: #all card move down
            for j in (tile1_j, tile2_j):
                new_column = []
                for i in range(gameSettings.BOARD_ROWS):
                    if board[i][j] != 0:
                        new_column.append(board[i][j])
                while(len(new_column) < gameSettings.BOARD_ROWS - 1): new_column = [0] + new_column
                new_column.append(0)
                for k in range(gameSettings.BOARD_ROWS):
                    board[k][j] = new_column[k]
        if level == 4: #all card move left
            for i in (tile1_i, tile2_i):
                new_row = [0]
                for j in range(gameSettings.BOARD_COLUMNS):
                    if board[i][j] != 0:
                        new_row.append(board[i][j])
                while(len(new_row) < gameSettings.BOARD_COLUMNS): new_row.append(0)
                for k in range(gameSettings.BOARD_COLUMNS):
                    board[i][k] = new_row[k]
        if level == 5: #all card move right
            for i in (tile1_i, tile2_i):
                new_row = []
                for j in range(gameSettings.BOARD_COLUMNS):
                    if board[i][j] != 0:
                        new_row.append(board[i][j])
                while len(new_row) < gameSettings.BOARD_COLUMNS - 1: new_row = [0] + new_row
                new_row.append(0)
                for k in range(gameSettings.BOARD_COLUMNS):
                    board[i][k] = new_row[k]   

    def is_level_complete(self,board):
        """
        Checks if the level is complete.

        :param self: The GameScreen object that this method is called on.
        :param board: The current state of the game board.
        :return: A boolean indicating if the level is complete.
        """
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] != 0: return False
        return True

                    
    
