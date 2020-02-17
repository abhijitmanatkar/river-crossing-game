import pygame
import sys
import random
from config import *
from entities import Player, Obstacle, Enemy

# initialization
pygame.init()

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("River Crossing")

clock = pygame.time.Clock()

levels = [-1, 1, 1]
completed = [0, 0, 0]

cont = True

# define land segments
land = [
    (0, 0),
    (0, LAND_DIFF),
    (0, 2*LAND_DIFF),
    (0, 3*LAND_DIFF),
    (0, 4*LAND_DIFF),
    (0, 5*LAND_DIFF),
]

# initial obstacle locations
obs = [
    [WIDTH/4, LAND_DIFF + LAND_HEIGHT/2],
    [3*WIDTH/4, LAND_DIFF + LAND_HEIGHT/2],
    [5*WIDTH/6, 2*LAND_DIFF + LAND_HEIGHT/2],
    [1*WIDTH/6, 2*LAND_DIFF + LAND_HEIGHT/2],
    [WIDTH/4, 3*LAND_DIFF + LAND_HEIGHT/2],
    [3*WIDTH/4, 3*LAND_DIFF + LAND_HEIGHT/2],
    [1*WIDTH/3, 4*LAND_DIFF + LAND_HEIGHT/2],
    [2*WIDTH/3, 4*LAND_DIFF + LAND_HEIGHT/2],
    [WIDTH/2, 2*LAND_DIFF + LAND_HEIGHT/2],
    [WIDTH/2, 4*LAND_DIFF + LAND_HEIGHT/2],
]

# initial enemy start points
ens = [
    [WIDTH/4, (LAND_HEIGHT + WATER_HEIGHT) - WATER_HEIGHT/2],
    [WIDTH/6, 2*(LAND_HEIGHT + WATER_HEIGHT) - WATER_HEIGHT/2],
    [5*WIDTH/7, 3*(LAND_HEIGHT + WATER_HEIGHT) - WATER_HEIGHT/2],
    [5*WIDTH/9, 4*(LAND_HEIGHT + WATER_HEIGHT) - WATER_HEIGHT/2],
    [9*WIDTH/11, 5*(LAND_HEIGHT + WATER_HEIGHT) - WATER_HEIGHT/2],
]

# sprite groups
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# create obstacles
for pos in obs:
    o = Obstacle(pos)
    all_sprites.add(o)
    obstacles.add(o)

# create enemies
for pos in ens:
    e = Enemy(pos, ENEMY_SPEED)
    all_sprites.add(e)
    enemies.add(e)


def play(play_id, level):
    "Function for actual gameplay"

    global cont
    start_time = pygame.time.get_ticks()
    # reset crossed attribute of obstacles and enemies
    for ent in (enemies.sprites() + obstacles.sprites()):
        ent.crossed[play_id] = False
    running = True
    points = 0
    completed[play_id] = 0

    # randomize obstacle locations
    for o in obstacles.sprites():
        o.rect.centerx = WIDTH*random.randrange(20, 90, 5)/100

    # randomize enemy locations
    for e in enemies.sprites():
        e.rect.centerx = WIDTH*random.randrange(300, 700)/1000

    # set enemy speeds
    for e in enemies.sprites():
        spd = ENEMY_SPEED*(0.5 + level/2)
        if spd >= 16:
            spd = 16
        e.speed = spd

    # initiate Player
    if play_id == 1:
        pos = (WIDTH/2, HEIGHT - 20)
    else:
        pos = (WIDTH/2, 20)

    player = Player(pos, play_id)
    all_sprites.add(player)

    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # back to main screen
                if event.key == pygame.K_ESCAPE:
                    running = False
                    cont = False

        # keyboard input for player movement
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            player.rect.x -= player.speed
        elif pygame.key.get_pressed()[pygame.K_RIGHT]:
            player.rect.x += player.speed
        if pygame.key.get_pressed()[pygame.K_UP]:
            player.rect.y -= player.speed
        elif pygame.key.get_pressed()[pygame.K_DOWN]:
            player.rect.y += player.speed

        # UPDATES
        all_sprites.update()

        # update points based on obstacles/enemies crossed
        if play_id == 1:
            for o in obstacles.sprites():
                if player.rect.y < o.rect.y and o.crossed[play_id] is False:
                    points += 5
                    o.crossed[play_id] = True
            for e in enemies.sprites():
                if player.rect.y < e.rect.y and e.crossed[play_id] is False:
                    points += 10
                    e.crossed[play_id] = True
        elif play_id == 2:
            for o in obstacles.sprites():
                if player.rect.y > o.rect.y and o.crossed[play_id] is False:
                    points += 5
                    o.crossed[play_id] = True
            for e in enemies.sprites():
                if player.rect.y > e.rect.y and e.crossed[play_id] is False:
                    points += 10
                    e.crossed[play_id] = True

        # collision detection
        hit = (
            pygame.sprite.spritecollide(player, enemies, False)
            + pygame.sprite.spritecollide(player, obstacles, False)
        )
        if hit:
            exp.play()
            running = False
            pygame.time.delay(1000)

        # win condition
        if play_id == 1:
            if player.rect.y <= 0:
                pygame.time.delay(500)
                completed[play_id] = 1
                running = False
        elif play_id == 2:
            if player.rect.y + player.height >= HEIGHT:
                pygame.time.delay(500)
                completed[play_id] = 1
                running = False

        # update time, score and create other on screen labels
        curr_time = (pygame.time.get_ticks() - start_time)//1000
        score = points - 2*curr_time
        score = font.render("Score: " + str(score), False, WHITE)
        time_ = font.render("Time: " + str(curr_time), False, WHITE)
        player_label = font.render("Player "+str(play_id), False, WHITE)

        # DRAW
        screen.fill(RIVER_BLUE)

        # draw land segments
        for i in range(6):
            pygame.draw.rect(
                screen,
                LAND_COLOR,
                ((0, i*LAND_DIFF), (WIDTH, LAND_HEIGHT))
            )

        all_sprites.draw(screen)

        # display score, time and other labels
        screen.blit(player_label, (WIDTH/2 - player_label.get_width()/2, 0))
        if play_id == 1:
            screen.blit(
                score,
                (WIDTH-score.get_width(), HEIGHT-score.get_height())
            )
        elif play_id == 2:
            screen.blit(score, (0, 0))

        screen.blit(time_, (WIDTH - time_.get_width(), 0))

        # FLIP
        pygame.display.flip()
        clock.tick(60)

    all_sprites.remove(player)  # player 1 can't be drawn in player 2's turn
    return points-2*curr_time, curr_time    # actual score=points-2*curr_time


def start():
    "Start Screen loop"

    running = True

    while running:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
        # DRAW

        # render text to be drawn on the screen
        title_ = title_font.render("River Crossing", True, BLUE)
        sub1 = font.render('An "original" game by Abhijit', True, GREEN)
        sub2 = font.render('Press ENTER to Play', True, GREEN)

        # draw objects on the screen
        screen.fill(BLACK)
        screen.blit(title_, (WIDTH/2 - title_.get_width()/2, HEIGHT/3))
        screen.blit(sub1, (WIDTH/2 - sub1.get_width()/2, 2*HEIGHT/3))
        screen.blit(sub2, (WIDTH/2 - sub2.get_width()/2, 5*HEIGHT/6))

        # FLIP
        pygame.display.flip()
        clock.tick(60)


def round_start():
    "Screen displayed before start of a round"

    running = True

    while running:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # DRAW

        # display levels of each of the players
        l1 = font.render("Player 1 on level " + str(levels[1]), True, YELLOW)
        l2 = font.render("Player 2 on level " + str(levels[2]), True, YELLOW)
        screen.fill(BLACK)
        screen.blit(l1, (WIDTH/2 - l1.get_width()/2, 2*HEIGHT/5))
        screen.blit(l2, (WIDTH/2 - l2.get_width()/2, 3*HEIGHT/5))

        # FLIP
        pygame.display.flip()
        clock.tick(60)


def round_end(time1, time2, points1, points2, winner):
    "Screen displayed at the end of a round. Displays points and winner."

    global cont
    running = True

    while running:
        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                if event.key == pygame.K_ESCAPE:
                    running = False
                    cont = False

        # DRAW
        t1 = mid_font.render("Player 1:", True, GREEN)
        t1_t = font.render("Time: " + str(time1), True, BLUE)
        t1_p = font.render("Points: " + str(points1), True, BLUE)
        t2 = mid_font.render("Player 2:", True, GREEN)
        t2_t = font.render("Time: " + str(time2), True, BLUE)
        t2_p = font.render("Points: " + str(points2), True, BLUE)
        tb = font.render(
            "Press ENTER to continue or ESC to go back to main screen",
            True,
            WHITE
        )
        if winner == 0:
            win_str = "No Winners this round!"
        else:
            win_str = "Winner is Player " + str(winner)
        tw = mid_font.render(win_str, True, YELLOW)
        screen.fill(BLACK)
        screen.blit(t1, (WIDTH/2 - t1.get_width()/2, HEIGHT/9))
        screen.blit(t1_t, (WIDTH/2 - t1_t.get_width()/2, 2*HEIGHT/9))
        screen.blit(t1_p, (WIDTH/2 - t1_p.get_width()/2, 3*HEIGHT/9))
        screen.blit(t2, (WIDTH/2 - t2.get_width()/2, 4*HEIGHT/9))
        screen.blit(t2_t, (WIDTH/2 - t2_t.get_width()/2, 5*HEIGHT/9))
        screen.blit(t2_p, (WIDTH/2 - t2_p.get_width()/2, 6*HEIGHT/9))
        screen.blit(tw, (WIDTH/2 - tw.get_width()/2, 7*HEIGHT/9))
        screen.blit(tb, (WIDTH/2 - tb.get_width()/2, 8*HEIGHT/9))

        # FLIP
        pygame.display.flip()
        clock.tick(60)


def round():
    """Function to run start and end screens of a round, play the actual round
     and calculate the winner of the round.
    """

    global cont

    # ROUND START
    round_start()

    # PLAY

    # player 1 plays
    points1, time1 = play(1, levels[1])
    if cont is False:   # check to see if jump to main screen or not
        return None

    # player 2 plays
    points2, time2 = play(2, levels[2])
    if cont is False:
        return None

    # DECIDE WINNER
    winner = 0
    if completed[1] == completed[2] == 1:
        if points1 == points2:
                winner = 0
        elif points1 < points2:
            winner = 2
        elif points1 > points2:
            winner = 1
    elif completed[1] == 1 and completed[2] == 0:
        winner = 1
    elif completed[2] == 1 and completed[1] == 0:
        winner = 2
    levels[winner] += 1

    # ROUND END
    round_end(time1, time2, points1, points2, winner)


def main():
    "Main function that displays start screen and plays rounds in a loop"

    global cont

    # music starts
    pygame.mixer.music.load("bg.mp3")
    pygame.mixer.music.play(-1)

    # loop for the application
    while True:
        start()
        levels[1] = levels[2] = 1   # initialize both players' levels to 1
        cont = True
        # loop for continuing rounds
        while cont:
            round()

if __name__ == "__main__":
    main()

# quit
pygame.quit()
