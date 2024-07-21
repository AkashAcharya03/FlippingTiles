import pygame
import os
import random
import sqlite3
import time

pygame.init()

# Variables for Game
gameWidth = 840
gameHeight = 640
picSize = 80
gameColumns = 5
gameRows = 4
padding = 10
leftMargin = (gameWidth - ((picSize + padding) * gameColumns)) // 2
rightMargin = leftMargin
topMargin = (gameHeight - ((picSize + padding) * gameRows)) // 2
bottomMargin = topMargin
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
selection1 = None
selection2 = None

# Function to load and set up game state
def setup_game():
    global memoryPictures, memPics, memPicsRect, hiddenImages
    # Create list of Memory Pictures
    memoryPictures = []
    for item in os.listdir('images/'):
        memoryPictures.append(item.split('.')[0])
    memoryPicturesCopy = memoryPictures.copy()
    memoryPictures.extend(memoryPicturesCopy)
    random.shuffle(memoryPictures)

    # Load each of the images into the python memory
    memPics = []
    memPicsRect = []
    hiddenImages = []
    for item in memoryPictures:
        picture = pygame.image.load(f'images/{item}.png')
        picture = pygame.transform.scale(picture, (picSize, picSize))
        memPics.append(picture)
        pictureRect = picture.get_rect()
        memPicsRect.append(pictureRect)

    for i in range(len(memPicsRect)):
        memPicsRect[i][0] = leftMargin + ((picSize + padding) * (i % gameColumns))
        memPicsRect[i][1] = topMargin + ((picSize + padding) * (i % gameRows))
        hiddenImages.append(False)

# Function to handle game restart
def restart_game():
    global done, selection1, selection2
    done = False
    selection1 = None
    selection2 = None
    setup_game()

# Loading the pygame screen.
screen = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption('Tile Flip-Memory Game')
gameIcon = pygame.image.load('logo.jpg')
pygame.display.set_icon(gameIcon)

# Load the BackGround image into Python
bgImage = pygame.image.load('background.jpg')
bgImage = pygame.transform.scale(bgImage, (gameWidth, gameHeight))
bgImageRect = bgImage.get_rect()

# Load a font for displaying the timer text
font = pygame.font.Font(None, 36)

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('game_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store player information if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS Players (
                    id INTEGER PRIMARY KEY,
                    player_name TEXT
                )''')

# Create a table to store game scores if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS Scores (
                    id INTEGER PRIMARY KEY,
                    player_id INTEGER,
                    time_taken INTEGER,
                    FOREIGN KEY(player_id) REFERENCES Players(id)
                )''')

# Commit the changes to the database
conn.commit()

# Function to fetch top 5 players with their times
def fetch_top_players():
    cursor.execute("SELECT p.player_name, s.time_taken FROM Scores s JOIN Players p ON s.player_id = p.id ORDER BY s.time_taken ASC LIMIT 5")
    rows = cursor.fetchall()
    top_players = [(row[0], row[1]) for row in rows]
    return top_players

# Fetch top 5 players
top_players = fetch_top_players()

# Input box for entering player's name
input_box = pygame.Rect(300, 200, 140, 32)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
done = False

# Setup the game for the first time
setup_game()

# Game loop
while True:
    # Player Name Input
    while not done:
        grey = (34, 40, 49)
        # Load background image
        screen.blit(bgImage, bgImageRect)

        # Display top 5 players
        top_players_text = font.render("TOP 5 PLAYERS:", True, grey)
        screen.blit(top_players_text, (620, 20))
        
        lImage = pygame.image.load('logo.jpg')
        lImage = pygame.transform.scale(lImage, (250, 250))
        lImageRect = lImage.get_rect()
        screen.blit(lImage,((gameWidth/2)-250/2, 250))

        #title
      
        for idx, (name, time_taken) in enumerate(top_players):
            player_text = font.render(f"{idx+1}. {name}: {time_taken} sec", True, grey)
            screen.blit(player_text, (600, 50 + idx * 30))

        # Input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    active = not active
                else:
                    active = False
                # Change the current color of the input box.
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        player_name = text
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode

        # Define brown color
        BROWN = (139, 69, 19)  # Brown color RGB value

        # Render the input_box and text.
        pygame.draw.rect(screen, BROWN, input_box, 2)  # Change color to brown
        font = pygame.font.Font(None, 24)
        text_surface = font.render(text, True, BROWN)
        width = max(240, text_surface.get_width() + 10)
        input_box.w = width
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        # Render "Enter Your Name" text with brown color
        enter_name_font = pygame.font.Font(None, 24)
        enter_name_text = enter_name_font.render("ENTER YOUR NAME :", True, BROWN)  # Render with brown color
        screen.blit(enter_name_text, (input_box.x, input_box.y - 30))

        pygame.display.flip()

    # Start game loop after player enters name
    # Start timer
    start_time = time.time()

    while True:
        # Load background image
        screen.blit(bgImage, bgImageRect)
        

        # Input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for item in memPicsRect:
                    if item.collidepoint(event.pos):
                        if hiddenImages[memPicsRect.index(item)] != True:
                            if selection1 is not None:
                                selection2 = memPicsRect.index(item)
                                hiddenImages[selection2] = True
                            else:
                                selection1 = memPicsRect.index(item)
                                hiddenImages[selection1] = True
        lImage = pygame.image.load('logo.jpg')
        lImage = pygame.transform.scale(lImage, (picSize, picSize))
        lImageRect = lImage.get_rect()

        for i in range(len(memoryPictures)):
            if hiddenImages[i] == True:
                screen.blit(memPics[i], memPicsRect[i])
            else:
                pygame.draw.rect(screen, WHITE, (memPicsRect[i][0], memPicsRect[i][1], picSize, picSize))
                screen.blit(lImage,(memPicsRect[i][0], memPicsRect[i][1], picSize, picSize))


        # Calculate total time taken and render timer text
        end_time = time.time()
        total_time = int(end_time - start_time)
        timer_text = font.render("Time: " + str(total_time) + " sec", True, WHITE)
        screen.blit(timer_text, (20, 20))

        pygame.display.update()

        if selection1 is not None and selection2 is not None:
            if memoryPictures[selection1] == memoryPictures[selection2]:
                selection1, selection2 = None, None
            else:
                pygame.time.wait(1000)
                hiddenImages[selection1] = False
                hiddenImages[selection2] = False
                selection1, selection2 = None, None

        win = 1
        for number in range(len(hiddenImages)):
            win *= hiddenImages[number]

        if win == 1:
            pygame.time.wait(5000)
            break

    if not done:  # If the game was not completed (player quit), don't store the time in the database
        continue

    # Insert the player's name into the Players table if it doesn't exist
    cursor.execute("INSERT OR IGNORE INTO Players (player_name) VALUES (?)", (player_name,))

    # Fetch the player's ID from the Players table
    cursor.execute("SELECT id FROM Players WHERE player_name = ?", (player_name,))
    player_id = cursor.fetchone()[0]

    # Insert the player's score into the Scores table
    cursor.execute("INSERT INTO Scores (player_id, time_taken) VALUES (?, ?)", (player_id, total_time))

    # Commit the changes to the database
    conn.commit()

    # Print player's name and time taken
    print_text = font.render(f"Player: {player_name}, Time taken: {total_time} sec", True, WHITE)

    # Prompt for restart or quit
    restart_game = False
    while True:
        # Load background image
        screen.blit(bgImage, bgImageRect)

        # Display the print text
        screen.blit(print_text, (gameWidth // 2 - 150, gameHeight // 2 - print_text.get_height() // 2))

        # Prompt for restart or quit
        restart_text = font.render("Press 'R' to restart or 'Q' to quit", True, WHITE)
        screen.blit(restart_text, (gameWidth // 2 - 150, gameHeight // 2 + 50))

        pygame.display.flip()

        # Input events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game = True
                    break
                elif event.key == pygame.K_q:
                    pygame.quit()
                    break

        # If the player wants to restart, reset necessary variables and restart the game loop
        if restart_game:
            # Reset necessary variables here (e.g., hiddenImages, selection1, selection2)
            setup_game()
            break

# Close the database connection
conn.close()
