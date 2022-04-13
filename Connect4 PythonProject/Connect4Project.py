import pygame


pygame.init()

#colours
white = (255, 255, 255)
red = (255, 0, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
blue = (0, 0, 128)
background = (0, 0, 255)

#sounds
startsound = pygame.mixer.Sound("start.mp3")
piecesound = pygame.mixer.Sound("piece.mp3")
winsound = pygame.mixer.Sound("win.mp3")
errorsound = pygame.mixer.Sound("error.mp3")

pos_x = [50, 150, 250, 350, 450, 550, 650]
pos_y = [50, 150, 250, 350, 450, 550]

#To create game window
def create_screen():
    screen = pygame.display.set_mode((700, 600))
    screen.fill(background)
    x = 50
    for column in range(0,7):
        y = 50
        for row in range(0,6):
            pygame.draw.circle(screen, white, (x,y), 40)
            y += 100
        x += 100
    pygame.display.update()
    return screen


#Checks for vacancy in the column
def col_empty(screen, x):
    if screen.get_at((x, 50)) == white:
        return True
    return False


#Gets vacant row
def get_row(screen, x):
    for y in range(550, 49, -100):
        if screen.get_at((x, y)) == white:
            return y


def get_x_pos(screen, x, y):
    if y <= 590 and y >= 10:
        for pos in pos_x:
            if x <= pos + 40 and x >= pos - 40:
                return pos
    return 420


#Horizontal winning case

def horizontal_4(screen, x_coordinate, y_coordinate, colour):
    coin = 1
    coordinates_list = [[x_coordinate, y_coordinate]]
    prev_x_coordinate = x_coordinate - 100
    while prev_x_coordinate >= 50 and screen.get_at((prev_x_coordinate, y_coordinate)) == colour and coin != 4:
        coin += 1
        coordinates_list.append([prev_x_coordinate, y_coordinate])
        prev_x_coordinate -= 100
    next_x_coordinate = x_coordinate + 100

    while next_x_coordinate <= 650 and screen.get_at((next_x_coordinate, y_coordinate)) == colour and coin != 4:
        coin += 1
        coordinates_list.append([next_x_coordinate, y_coordinate])
        next_x_coordinate += 100
    if coin == 4:
        for pair in coordinates_list:
            add_star(screen, pair[0], pair[1])
        return True
    return False


#Vertical winning case

def vertical_4(screen, x_coordinate, y_coordinate, colour):
    coin = 1
    coordinates_list = [[x_coordinate, y_coordinate]]
    next_y_coordinate = y_coordinate + 100
    while next_y_coordinate <= 550 and screen.get_at((x_coordinate, next_y_coordinate)) == colour and coin != 4:
        coin += 1
        coordinates_list.append([x_coordinate, next_y_coordinate])
        next_y_coordinate += 100
    if coin == 4:
        for pair in coordinates_list:
            add_star(screen, pair[0], pair[1])
        return True
    return False


#diagonal winning case

def diagonal_4(screen, x_coordinate, y_coordinate, colour):
    coin = 1
    coordinates_list = [[x_coordinate, y_coordinate]]
    prev_x_coordinate = x_coordinate - 100
    prev_y_coordinate = y_coordinate - 100
    while prev_x_coordinate >= 50 and prev_y_coordinate >= 50 and screen.get_at((prev_x_coordinate, prev_y_coordinate)) == colour:
        coin += 1
        coordinates_list.append([prev_x_coordinate, prev_y_coordinate])
        prev_x_coordinate -= 100
        prev_y_coordinate -= 100
    next_x_coordinate = x_coordinate + 100
    next_y_coordinate = y_coordinate + 100
    while next_x_coordinate <= 650 and next_y_coordinate <= 550 and screen.get_at((next_x_coordinate, next_y_coordinate)) == colour:
        coin = coin + 1
        coordinates_list.append([next_x_coordinate, next_y_coordinate])
        next_x_coordinate += 100
        next_y_coordinate += 100
    if coin == 4:
        for pair in coordinates_list:
            add_star(screen, pair[0], pair[1])
        return True

    coin = 1
    prev_x_coordinate = x_coordinate - 100
    next_y_coordinate = y_coordinate + 100
    coordinates_list = [[x_coordinate, y_coordinate]]
    while prev_x_coordinate >= 50 and next_y_coordinate <= 550 and screen.get_at((prev_x_coordinate, next_y_coordinate)) == colour:
        coin += 1
        coordinates_list.append([prev_x_coordinate, next_y_coordinate])
        prev_x_coordinate -= 100
        next_y_coordinate += 100
    next_x_coordinate = x_coordinate + 100
    prev_y_coordinate = y_coordinate - 100
    while next_x_coordinate <= 650 and prev_y_coordinate >= 50 and screen.get_at((next_x_coordinate, prev_y_coordinate)) == colour:
        coin += 1
        coordinates_list.append([next_x_coordinate, prev_y_coordinate])
        next_x_coordinate += 100
        prev_y_coordinate -= 100
    if coin == 4:
        for pair in coordinates_list:
            add_star(screen, pair[0], pair[1])
        return True
    return False


#Highlighting the won coins
def add_star(screen, x_coordinate, y_coordinate):
    image = pygame.image.load(r'C:\Users\hp\OneDrive\Desktop\GitRepository\Connect4 PythonProject\FinalStar2.png')
    screen.blit(image, (x_coordinate - 32, y_coordinate - 30))
    pygame.display.update()


#To check for winning case
def winning_move(screen, x_coordinate, y_coordinate, colour):
    return horizontal_4(screen, x_coordinate, y_coordinate, colour) or vertical_4(screen, x_coordinate, y_coordinate, colour) or diagonal_4(screen, x_coordinate, y_coordinate, colour)


def full_board(screen):
    for x in pos_x:
        if col_empty(screen, x):
            return False
    return True

font = pygame.font.Font("freesansbold.ttf", 45)


#To display the winner
def end_message(screen,turn):
     if turn % 2 == 0:
         text = font.render("Congratulations!! Player1 won", True, green, blue)
     else:
         text = font.render("Congratulations!! Player2 won", True, green, blue)

     textRect = text.get_rect()
     textRect.center = (700//2,600//2)
     screen.blit(text,textRect)
     pygame.display.update()


screen = create_screen()
startsound.play()
turn = 0
colour = white
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x , y = event.pos
            x = get_x_pos(screen, x, y)
            if x in pos_x:
                if col_empty(screen, x):
                    y = get_row(screen, x)
                    if turn % 2 == 0:
                        colour = red
                    else:
                        colour = yellow
                    pygame.draw.circle(screen, colour, (x,y), 40)
                    piecesound.play()
                    pygame.display.update()
                    if winning_move(screen, x, y, colour):
                        game_over = True
                        winsound.play()
                        end_message(screen, turn)
                        break
                    elif full_board(screen):
                        text = font.render("Game is draw!!", True, green, blue)
                        textRect = text.get_rect()
                        textRect.center = (700//2,600//2)
                        screen.blit(text,textRect)
                        pygame.display.update()
                    turn += 1
                else:
                    errorsound.play()
