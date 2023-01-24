# Conway's Game of Life
# Game description available at https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

import numpy as np
import pygame as pg
import time

COLOUR_GRID = (100, 100, 100)  # Grid colour
COLOUR_LIVE = (230, 230, 230)  # Living cell colour
COLOUR_DEAD = (50, 50, 50)  # Dead cell colour


def update(screen, cells, cell_size):  # Function to apply game rules and draw living cells
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))  # Initialise updated cells array as 0s in shape of cells array
    for row, col in np.ndindex(cells.shape):  # For each element in cells array
        if row == 0 and col == 0:  # If first element in cells array
            living_neighbours = np.sum(cells[row:row + 2, col:col + 2]) - cells[row, col]  # Count the number of living neighbour cells
        elif row == 0:  # If first row of cells array
            living_neighbours = np.sum(cells[row:row + 2, col - 1:col + 2]) - cells[row, col]  # Count the number of living neighbour cells
        elif col == 0:  # If first column of cells array
            living_neighbours = np.sum(cells[row - 1:row + 2, col:col + 2]) - cells[row, col]  # Count the number of living neighbour cells
        else:  # If not first element, first row, or first column of cells array
            living_neighbours = np.sum(cells[row - 1:row + 2, col - 1:col + 2]) - cells[row, col]  # Count the number of living neighbour cells

        colour = COLOUR_DEAD if cells[row, col] == 0 else COLOUR_LIVE  # Set cell colour

        if cells[row, col] == 1:  # If cell is alive
            if living_neighbours < 2 or living_neighbours > 3:  # If cell has fewer than 2 or more than 3 living neighbours
                updated_cells[row, col] = 0  # Cell dies
            else:  # If cell has 2 or 3 living neighbours
                updated_cells[row, col] = 1  # Cell stays alive
        else:  # If cell is dead
            if living_neighbours == 3:  # If cell has 3 living neighbours
                updated_cells[row, col] = 1  # Cell becomes alive
            else:  # If cell does not have 3 living neighbours
                updated_cells[row, col] = 0  # Cell stays dead

        pg.draw.rect(screen, colour, (col * cell_size, row * cell_size, cell_size - 1, cell_size - 1))  # Draw rectangle at (col*cell_size, row*cell_size) with size (cell_size-1, cell_size-1)

    return updated_cells  # Return updated cells array


def main():  # Main function to set up game and run game loop
    pg.init()  # Initialise pygame
    screen = pg.display.set_mode((900, 600))  # Set game window to 900x600, of which 800x600 is for the game board and 100x600 is for the menu bar
    pg.display.set_caption("Conway's Game of Life")  # Set game window title

    play_img = pg.image.load("resources/play.png").convert_alpha()  # Load play button image
    restart_img = pg.image.load("resources/restart.png").convert_alpha()  # Load restart button image
    close_img = pg.image.load("resources/close.png").convert_alpha()  # Load close button image

    class Button:  # Class for menu buttons
        def __init__(self, x, y, image):  # Function to initialise button
            self.image = image  # Store button image
            self.rect = self.image.get_rect()  # Set button image border rectangle
            self.rect.topleft = (x, y)  # Set button image top left coordinates

        def draw(self):  # Function to draw button to screen
            action = False  # Execute button action flag initially set as false
            mouse_pos = pg.mouse.get_pos()  # Store mouse coordinates
            if self.rect.collidepoint(mouse_pos) and pg.mouse.get_pressed()[0]:  # If mouse coordinates collide with button image rectangle and left mouse button clicked
                action = True  # Set button action flag to true

            screen.blit(self.image, (self.rect.x, self.rect.y))  # Copy image to screen

            return action  # Return button action flag

    play_button = Button(809, 9, play_img)  # Create button instance for play button
    restart_button = Button(809, 99, restart_img)  # Create button instance for restart button
    close_button = Button(809, 509, close_img)  # Create button instance for close button

    cells = np.zeros((60, 80))  # Initialise cells array as 60 rows and 80 columns of 0s
    screen.fill(COLOUR_GRID)  # Set Screen to grid colour
    update(screen, cells, 10)  # Call update function
    pg.display.update()  # Update full screen display surface

    paused = True  # Game paused flag initially set to true

    while True:  # Game loop constantly awaiting user input
        play = play_button.draw()  # Draw play button to screen and store button action flag
        restart = restart_button.draw()  # Draw restart button to screen and store button action flag
        close = close_button.draw()  # Draw close button to screen and store button action flag
        pg.display.update()  # Update full screen display surface
        for event in pg.event.get():  # For each input event
            if event.type == pg.QUIT or close:  # If quit event triggered
                pg.quit()  # Quit pygame
                return  # Exit main function
            if play:  # If play/pause event triggered
                paused = not paused  # Invert game paused state (play->pause or pause->play)
                update(screen, cells, 10)  # Call update function to sync paused state with current game state
                pg.display.update()  # Update full screen display surface
            if restart:  # If restart event triggered
                paused = True  # Game restarts in paused state
                cells = np.zeros((60, 80))  # Reset cells array as 60 rows and 80 columns of 0s
                screen.fill(COLOUR_GRID)  # Set screen to grid colour
                update(screen, cells, 10)  # Call update function
                pg.display.update()  # Update full screen display surface
            if pg.mouse.get_pressed()[0]:  # If left mouse button is clicked
                pos = pg.mouse.get_pos()  # Store mouse coordinates
                if pos[0] // 10 < 80:  # If mouse x coordinate is above game board
                    cells[pos[1] // 10, pos[0] // 10] = 1  # Set clicked cell to living
                update(screen, cells, 10)  # Call update function
                pg.display.update()  # Update full screen display surface
            elif pg.mouse.get_pressed()[2]:  # If right mouse button is clicked
                pos = pg.mouse.get_pos()  # Store mouse coordinates
                if pos[0] // 10 < 80:  # If mouse x coordinate is above game board
                    cells[pos[1] // 10, pos[0] // 10] = 0  # Set clicked cell to dead
                update(screen, cells, 10)  # Call update function
                pg.display.update()  # Update full screen display surface

        if not paused:  # If game is not paused
            cells = update(screen, cells, 10)  # Update cells array
            pg.display.update()  # Update full screen display surface

        time.sleep(0.01)  # Wait 0.01 seconds


if __name__ == "__main__":  # If file is run as a script
    main()  # Call main function
