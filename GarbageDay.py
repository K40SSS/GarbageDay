import pygame
import time
from pygame import mixer
import random
from random import randint

pygame.init()
mixer.init()
screen_info = pygame.display.Info()
screenWidth = screen_info.current_w
screenHeight = screen_info.current_h
screen =  pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
pygame.display.set_caption('Garbage Day')
titleScreenButtonFont = pygame.font.Font('GUIFONT.ttf', 63)
titleTextFont = pygame.font.Font('GUIFONT.ttf', 140)
levelSelectorFont = pygame.font.Font('GUIFONT.ttf', 140)
backSymbolFont = pygame.font.SysFont("Arial", 50, bold=True)
pauseSymbolFont = pygame.font.SysFont("Arial", 50, bold = True)
# Constants for falling objects
RECYCLE_SIDE, GARBAGE_SIDE, COMPOST_SIDE = 50, 50, 50
FALL_SPEED = 5
RECYCLE_SPAWN_EVENT = pygame.USEREVENT + 1
GARBAGE_SPAWN_EVENT = pygame.USEREVENT + 2
COMPOST_SPAWN_EVENT = pygame.USEREVENT + 3
RECYCLE_SPAWN_INTERVAL = randint(5000, 7000)
GARBAGE_SPAWN_INTERVAL = randint(5000, 7000)
COMPOST_SPAWN_INTERVAL = randint(5000, 7000)
level1Score = 0
level2Score = 0
level3Score = 0
playerRecycle = False
playerGarbage = False
playerCompost = False
RECYCLE_COLOR = (0, 0, 255)
GARBAGE_COLOR = (255, 0, 0)
COMPOST_COLOR = (0, 255, 0)
throwColour = GARBAGE_COLOR

# Falling objects list
falling_objects = []

RED = (255, 0, 0)
ORANGE = (255, 172, 28)
YELLOW = (255,255,0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
levelSelector = False
gameRunning = False
titleScreen = True
level1Run = False
level2Run = False
level3Run = False
fromLevel1 = False
fromLevel2 = False
pause = False
playMusic = True
song = "Lil Dicky - Earth (Lyrics).mp3"
mx = 0
my = 0
runOnce = True
interactObject = pygame.Rect
buttonObject = pygame.Rect
levelObject = pygame.Rect
recycleObject = pygame.Rect
garbageObject = pygame.Rect
compostObject = pygame.Rect
playerObject = pygame.Rect
npcObject = pygame.Rect
throwObject = pygame.Rect
recycle = 0
garbage = 0
compost = 0
npcX = -100
npcY = 250
throwY = npcY
throwX = npcX
playerX = screenWidth/2 - 50
playerY = screenHeight - 125

recycleBinImg = pygame.image.load("recycleBin-Photoroom.png").convert_alpha()
garbageBinImg = pygame.image.load("garbageBin-Photoroom.png").convert_alpha()
compostBinImg = pygame.image.load("compostBin-Photoroom.png").convert_alpha()
closedBinImg = pygame.image.load("closedBinImg.png").convert_alpha()
levelBackgroundImg = pygame.image.load("levelBackgrounds.jpg").convert_alpha()

buttonImg = pygame.image.load("buttonImage.png").convert_alpha()
recycleItemImg = pygame.image.load("RecycleItem.png").convert_alpha()
compostItemImg = pygame.image.load("CompostItem.png").convert_alpha()
garbageItemImg = pygame.image.load("garbageItem.png").convert_alpha()
binSize = (124,165)
buttonSize = (300, 180)

def pause_menu(screen, screenWidth, screenHeight, fonts, colors, playMusic):
    runOnce = True
    pause = True
    
    while pause:
        if runOnce:
            # Draw semi-transparent overlay
            pauseScreen = pygame.Surface((screenWidth, screenHeight))
            pauseScreen.fill(colors['WHITE'])
            pauseScreen.set_alpha(160)
            screen.blit(pauseScreen, (0, 0))
            runOnce = False
        
        # Draw pause menu buttons
        resumeButton = pygame.Rect(screenWidth / 2 - 80, screenHeight / 2 - 210, 200, 75)
        musicButton = pygame.Rect(screenWidth / 2 - 80, screenHeight / 2 - 85, 200, 75)
        levelButton = pygame.Rect(screenWidth / 2 - 80, screenHeight / 2 + 20, 200, 75)
        quitButton = pygame.Rect(screenWidth / 2 - 80, screenHeight / 2 + 145, 200, 75)

        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth / 2 - 100, screenHeight / 2 - 235))
        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth / 2 - 100, screenHeight / 2 - 110))
        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth / 2 - 100, screenHeight / 2 - 5))
        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth / 2 - 100, screenHeight / 2 + 120))

        screen.blit(fonts['buttonFont'].render("START", True, colors['BLACK']), (screenWidth / 2 - 80, screenHeight / 2 - 190))
        screen.blit(fonts['buttonFont'].render("MUSIC", True, colors['BLACK']), (screenWidth / 2 - 80, screenHeight / 2 - 65))
        screen.blit(fonts['buttonFont'].render("LEVEL", True, colors['BLACK']), (screenWidth / 2 - 67, screenHeight / 2 + 40))
        screen.blit(fonts['buttonFont'].render("QUIT", True, colors['BLACK']), (screenWidth / 2 - 55, screenHeight / 2 + 165))

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                (mx, my) = pygame.mouse.get_pos()
                if resumeButton.collidepoint(mx, my):
                    pause = False
                elif musicButton.collidepoint(mx, my):
                    if playMusic:
                        mixer.music.pause()
                        playMusic = False
                    else:
                        mixer.music.unpause()
                        playMusic = True
                elif levelButton.collidepoint(mx, my):
                    return "levelSelector"
                elif quitButton.collidepoint(mx, my):
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = False
        
        time.sleep(1 / 60)
        pygame.display.update()

    return None

mixer.music.load(song)
mixer.music.set_volume(0.1)
mixer.music.play(-1)

while True:
    while titleScreen:
        screen_info = pygame.display.Info()
        screenWidth = screen_info.current_w
        screenHeight = screen_info.current_h
        screen.blit(pygame.transform.scale(levelBackgroundImg, (screenWidth, screenHeight)), (0,0))
        (mx,my) = pygame.mouse.get_pos()
        startText = titleScreenButtonFont.render("START", True, BLACK)
        musicText = titleScreenButtonFont.render("MUSIC", True, BLACK)
        quitText = titleScreenButtonFont.render("QUIT", True, BLACK)
        titleText = titleTextFont.render("GARBAGE DAY", True, BLACK)

        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth/2 - 115, 2*screenHeight/3 - 200))
        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth/2 - 115, 2*screenHeight/3 - 75))
        screen.blit(pygame.transform.scale(buttonImg, buttonSize), (screenWidth/2 - 115, 2*screenHeight/3 + 50))

        screen.blit(titleText, (13*screenWidth/64, screenHeight/5))
        
        startButton = buttonObject(screenWidth/2 - 85, 2*screenHeight/3 - 150, 200, 75)
        screen.blit(startText, startButton)

        musicButton = buttonObject(screenWidth/2 - 85, 2*screenHeight/3 - 25, 200, 75)
        screen.blit(musicText, (screenWidth/2 - 82, 2*screenHeight/3 - 25))

        quitButton = buttonObject(screenWidth/2 - 85, 2*screenHeight/3 + 100, 200, 75)
        screen.blit(quitText, (screenWidth/2 - 62, 2*screenHeight/3 + 95))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0] == True and startButton.collidepoint(mx,my):
                    titleScreen = False
                    levelSelector = True
                elif pygame.mouse.get_pressed()[0] == True and musicButton.collidepoint(mx,my):
                    if playMusic:
                        mixer.music.pause()
                        playMusic = False
                    else:
                        mixer.music.unpause()
                        playMusic = True
                elif pygame.mouse.get_pressed()[0] == True and quitButton.collidepoint(mx,my):
                    pygame.quit()
        time.sleep(1/60)
        pygame.display.update()
    while levelSelector:
        (mx,my) = pygame.mouse.get_pos()
        if not pause:
            pauseButton = pygame.Rect(screenWidth - 75, 25, 50, 50)
            pauseSymbol = pauseSymbolFont.render("II", True, WHITE)
            pygame.draw.rect(screen, BLACK, pauseButton)
            screen.blit(pauseSymbol, (screenWidth - 61, 22))
            screen_info = pygame.display.Info()
            screenWidth = screen_info.current_w
            screenHeight = screen_info.current_h
            screen.blit(pygame.transform.scale(levelBackgroundImg, (screenWidth, screenHeight)), (0,0))
            backSymbol = backSymbolFont.render("<", True, WHITE)
            levelSelectText = titleTextFont.render("LEVEL SELECT", True, BLACK)
            screen.blit(levelSelectText, (19*screenWidth/80, screenHeight/5))
            pauseButton = pygame.Rect(screenWidth - 75, 25, 50, 50)
            pauseSymbol = pauseSymbolFont.render("II", True, WHITE)
            pygame.draw.rect(screen, BLACK, pauseButton)
            screen.blit(pauseSymbol, (screenWidth - 61, 22))
            backButton = interactObject(25, 25, 50, 50)
            pygame.Surface.fill(screen, BLACK, backButton)
            level1 = levelObject(screenWidth/3 + 25, screenHeight/2, 100, 100)
            pygame.Surface.fill(screen, RED, level1)
            screen.blit(backSymbol, (35, 23))
            level2 = levelObject(screenWidth/3 + 250, screenHeight/2, 100, 100)
            pygame.Surface.fill(screen, ORANGE, level2)
            level3 = levelObject(screenWidth/3 + 475, screenHeight/2, 100, 100)
            pygame.Surface.fill(screen, YELLOW, level3)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                            'buttonFont': titleScreenButtonFont,
                        }, {
                            'WHITE': WHITE,
                            'BLACK': BLACK,
                        }, playMusic)
                        if pauseResult == "levelSelector":
                            levelSelector = True
                        break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0] == True and level1.collidepoint(mx,my):
                        level1Run = True
                        pygame.time.set_timer(RECYCLE_SPAWN_EVENT, RECYCLE_SPAWN_INTERVAL)
                        pygame.time.set_timer(GARBAGE_SPAWN_EVENT, GARBAGE_SPAWN_INTERVAL)
                        pygame.time.set_timer(COMPOST_SPAWN_EVENT, COMPOST_SPAWN_INTERVAL)
                        level1Score = 0
                        playerX = screenWidth/2 - 50
                        playerY = screenHeight - 125
                        falling_objects.clear()
                        playerCompost = False
                        playerGarbage = False
                        playerRecycle = False
                        levelSelector = False
                    if pygame.mouse.get_pressed()[0] == True and level2.collidepoint(mx,my):
                        level2Run = True
                        pygame.time.set_timer(RECYCLE_SPAWN_EVENT, RECYCLE_SPAWN_INTERVAL)
                        pygame.time.set_timer(GARBAGE_SPAWN_EVENT, GARBAGE_SPAWN_INTERVAL)
                        pygame.time.set_timer(COMPOST_SPAWN_EVENT, COMPOST_SPAWN_INTERVAL)
                        level2Score = 0
                        npcX = -100
                        npcY = 250
                        throwY = npcY
                        throwX = npcX
                        playerX = screenWidth/2 - 50
                        playerY = screenHeight - 125
                        falling_objects.clear()
                        playerCompost = False
                        playerGarbage = False
                        playerRecycle = False
                        levelSelector = False
                    if pygame.mouse.get_pressed()[0] == True and level3.collidepoint(mx,my):
                        level3Run = True
                        pygame.time.set_timer(RECYCLE_SPAWN_EVENT, RECYCLE_SPAWN_INTERVAL)
                        pygame.time.set_timer(GARBAGE_SPAWN_EVENT, GARBAGE_SPAWN_INTERVAL)
                        pygame.time.set_timer(COMPOST_SPAWN_EVENT, COMPOST_SPAWN_INTERVAL)
                        level3Score = 0
                        playerX = screenWidth/2 - 50
                        playerY = screenHeight - 125
                        falling_objects.clear()
                        playerCompost = False
                        playerGarbage = False
                        playerRecycle = False
                        levelSelector = False
                    if pygame.mouse.get_pressed()[0] == True and backButton.collidepoint(mx,my):
                        titleScreen = True
                        levelSelector = False
                    if pauseButton.collidepoint(mx, my):
                        pauseResult = pause_menu(screen, screenWidth, screenHeight, {'buttonFont': titleScreenButtonFont,
                    }, {
                        'WHITE': WHITE,
                        'BLACK': BLACK,
                    }, playMusic)
                        if pauseResult == "levelSelector":
                            levelSelector = True
                        break
        pygame.event.clear()
        time.sleep(1/60)
        pygame.display.update()
    while level1Run:
        level1GameOver = False
        screen_info = pygame.display.Info()
        screenWidth = screen_info.current_w
        screenHeight = screen_info.current_h
        level1Text = titleScreenButtonFont.render("LEVEL 1", True, BLACK)
        score1Text = titleScreenButtonFont.render("SCORE:", True, BLACK)
        score1Number = titleScreenButtonFont.render(str(level1Score), True, BLACK)
        congratulationsText = titleTextFont.render("CONGRATULATIONS!", True, BLACK)
        player = playerObject(playerX, playerY, 100, 100)
        (mx, my) = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerX = playerX - 20
        if keys[pygame.K_RIGHT]:
            playerX = playerX + 20
        if playerX > screenWidth - 100:
            playerX = screenWidth - 100
        if playerX < 0:
            playerX = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level1Run = False
            if event.type == pygame.MOUSEMOTION:
                playerX,playerY = pygame.mouse.get_pos()
                playerY = screenHeight - 125
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    playerRecycle = True
                    playerGarbage = False
                    playerCompost = False
                elif event.key == pygame.K_2:
                    playerGarbage = True
                    playerRecycle = False
                    playerCompost = False
                elif event.key == pygame.K_3:
                    playerCompost = True
                    playerGarbage = False
                    playerRecycle = False
            # Pause functionality
            if event.type == pygame.MOUSEBUTTONDOWN and pauseButton.collidepoint(mx, my):
                pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                    'buttonFont': titleScreenButtonFont,
                }, {
                    'WHITE': WHITE,
                    'BLACK': BLACK,
                }, playMusic)
                if pauseResult == "levelSelector":
                    levelSelector = True
                    level1Run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                        'buttonFont': titleScreenButtonFont,
                    }, {
                        'WHITE': WHITE,
                        'BLACK': BLACK,
                    }, playMusic)
                    if pauseResult == "levelSelector":
                        levelSelector = True
                        level1Run = False
                    break
            if event.type == RECYCLE_SPAWN_EVENT and not pause:
                x_position = random.randint(0, screenWidth - RECYCLE_SIDE)
                recycle = pygame.Rect(x_position, 0, RECYCLE_SIDE, RECYCLE_SIDE)

                falling_objects.append(recycle)
            elif event.type == GARBAGE_SPAWN_EVENT and not pause:
                x1_position = random.randint(0, screenWidth - GARBAGE_SIDE)
                garbage = pygame.Rect(x1_position, 0, GARBAGE_SIDE, GARBAGE_SIDE)
                falling_objects.append(garbage)
            elif event.type == COMPOST_SPAWN_EVENT and not pause:
                x2_position = random.randint(0, screenWidth - COMPOST_SIDE)
                compost = pygame.Rect(x2_position, 0, COMPOST_SIDE, COMPOST_SIDE)
                falling_objects.append(compost)
            

        # Fill the screen and draw the pause button
        screen.blit(pygame.transform.scale(levelBackgroundImg, (screenWidth, screenHeight)), (0,0))
        pauseButton = pygame.Rect(screenWidth - 75, 25, 50, 50)
        pauseSymbol = pauseSymbolFont.render("II", True, WHITE)
        if playerRecycle:
            screen.blit(pygame.transform.scale(recycleBinImg, binSize),(playerX - 12, playerY - 50))
        elif playerGarbage:
            screen.blit(pygame.transform.scale(garbageBinImg, binSize), (playerX - 12, playerY - 50))
        elif playerCompost:
            screen.blit(pygame.transform.scale(compostBinImg, binSize), (playerX - 12, playerY - 50))
        else:
            screen.blit(pygame.transform.scale(closedBinImg, binSize), (playerX - 12, playerY - 50))
        
        # Draw and optionally update falling objects
        for obj in falling_objects:
            if not pause:
                obj.y += FALL_SPEED  # Only update position if not paused
            if obj == recycle:
                screen.blit(pygame.transform.scale(recycleItemImg, (50,50)), (obj.x, obj.y))
                if (recycle.colliderect(player) and playerRecycle):
                    falling_objects.remove(obj)
                    level1Score += 1
                    playerRecycle = False
            elif obj == garbage:
                screen.blit(pygame.transform.scale(garbageItemImg, (50,50)), (obj.x, obj.y))
                if (garbage.colliderect(player) and playerGarbage):
                    falling_objects.remove(obj)
                    level1Score += 1
                    playerGarbage = False
            elif obj == compost:
                screen.blit(pygame.transform.scale(compostItemImg, (50,50)), (obj.x, obj.y))
                if (compost.colliderect(player) and playerCompost):
                    falling_objects.remove(obj)
                    level1Score += 1
                    playerCompost = False
        screen.blit(level1Text, (screenWidth/2 - 100, 25))
        pygame.draw.rect(screen, BLACK, pauseButton)
        screen.blit(pauseSymbol, (screenWidth - 61, 22))
        screen.blit(score1Text, (25, 25))
        nextLevel = False
        if level1Score >= 10:
            score1Number = titleScreenButtonFont.render(str(level1Score), True, BLACK)
            screen.blit(congratulationsText, (screenWidth/2 - 650, screenHeight/2 - 250))
            nextLevel = True
        # Frame delay and display update
        screen.blit(score1Number, (255, 25))
        time.sleep(1 / 60)
        pygame.display.update()
        if nextLevel:
            pygame.time.delay(3000)
            level1Score = 0
            falling_objects.clear()
            level2Score = 0
            playerX = screenWidth/2 - 50
            playerY = screenHeight - 125
            playerCompost = False
            playerGarbage = False
            playerRecycle = False
            level1Run = False
            level2Run = True
            nextLevel = False
            fromLevel1 = True
    while level2Run:
        if fromLevel1:
            pygame.time.set_timer(RECYCLE_SPAWN_EVENT, RECYCLE_SPAWN_INTERVAL)
            pygame.time.set_timer(GARBAGE_SPAWN_EVENT, GARBAGE_SPAWN_INTERVAL)
            pygame.time.set_timer(COMPOST_SPAWN_EVENT, COMPOST_SPAWN_INTERVAL)
            fromLevel1 = False
        screen_info = pygame.display.Info()
        screenWidth = screen_info.current_w
        screenHeight = screen_info.current_h
        level2Text = titleScreenButtonFont.render("LEVEL 2", True, BLACK)
        score2Text = titleScreenButtonFont.render("SCORE:", True, BLACK)
        score2Number = titleScreenButtonFont.render(str(level2Score), True, BLACK)
        congratulationsText = titleTextFont.render("CONGRATULATIONS!", True, BLACK)
        player = playerObject(playerX, playerY, 100, 100)
        (mx, my) = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerX = playerX - 20
        if keys[pygame.K_RIGHT]:
            playerX = playerX + 20
        if playerX > screenWidth - 100:
            playerX = screenWidth - 100
        if playerX < 0:
            playerX = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level2Run = False
            if event.type == pygame.MOUSEMOTION:
                playerX,playerY = pygame.mouse.get_pos()
                playerY = screenHeight - 125
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    playerRecycle = True
                    playerGarbage = False
                    playerCompost = False
                elif event.key == pygame.K_2:
                    playerGarbage = True
                    playerRecycle = False
                    playerCompost = False
                elif event.key == pygame.K_3:
                    playerCompost = True
                    playerGarbage = False
                    playerRecycle = False
            # Pause functionality
            if event.type == pygame.MOUSEBUTTONDOWN and pauseButton.collidepoint(mx, my):
                pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                    'buttonFont': titleScreenButtonFont,
                }, {
                    'WHITE': WHITE,
                    'BLACK': BLACK,
                }, playMusic)
                if pauseResult == "levelSelector":
                    levelSelector = True
                    level2Run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                        'buttonFont': titleScreenButtonFont,
                    }, {
                        'WHITE': WHITE,
                        'BLACK': BLACK,
                    }, playMusic)
                    if pauseResult == "levelSelector":
                        levelSelector = True
                        level2Run = False
                    break
            # Object height reset
            if event.type == RECYCLE_SPAWN_EVENT and not pause:
                x_position = random.randint(0, screenWidth - RECYCLE_SIDE)
                recycle = pygame.Rect(x_position, 0, RECYCLE_SIDE, RECYCLE_SIDE)
                falling_objects.append(recycle)
            elif event.type == GARBAGE_SPAWN_EVENT and not pause:
                x1_position = random.randint(0, screenWidth - GARBAGE_SIDE)
                garbage = pygame.Rect(x1_position, 0, GARBAGE_SIDE, GARBAGE_SIDE)
                falling_objects.append(garbage)
            elif event.type == COMPOST_SPAWN_EVENT and not pause:
                x2_position = random.randint(0, screenWidth - COMPOST_SIDE)
                compost = pygame.Rect(x2_position, 0, COMPOST_SIDE, COMPOST_SIDE)
                falling_objects.append(compost)
            
        # Fill the screen and draw the pause button
        screen.blit(pygame.transform.scale(levelBackgroundImg, (screenWidth, screenHeight)), (0,0))
        pauseButton = pygame.Rect(screenWidth - 75, 25, 50, 50)
        pauseSymbol = pauseSymbolFont.render("II", True, WHITE)
        if playerRecycle:
            screen.blit(pygame.transform.scale(recycleBinImg, binSize),(playerX - 12, playerY - 50))
        elif playerGarbage:
            screen.blit(pygame.transform.scale(garbageBinImg, binSize), (playerX - 12, playerY - 50))
        elif playerCompost:
            screen.blit(pygame.transform.scale(compostBinImg, binSize), (playerX - 12, playerY - 50))
        else:
            screen.blit(pygame.transform.scale(closedBinImg, binSize), (playerX - 12, playerY - 50))
        
        

        #Oscar's safe space
        npcSpeed = 5
        throwSpeed = 5
        throw = throwObject(throwX, throwY, 25, 25)
        
        randomColour = 0
        
        if(throw.colliderect(player)):
            if((throwColour == RECYCLE_COLOR and playerRecycle) or (throwColour == COMPOST_COLOR and playerCompost) or (throwColour == GARBAGE_COLOR and playerGarbage)):
                level2Score += 1
                playerRecycle = False
                throwY = npcY
                throwX = npcX
                randomColour = random.randint(0, 3)
                if randomColour == 1:
                    screen.blit(pygame.transform.scale(recycleItemImg, (50,50)), (throw.x, throw.y))
                elif randomColour == 2:
                    screen.blit(pygame.transform.scale(garbageItemImg, (50,50)), (throw.x, throw.y))
                elif randomColour == 3:
                    screen.blit(pygame.transform.scale(compostItemImg, (50,50)), (throw.x, throw.y))
        if throwY > screenHeight or throwY < npcY:
            throwY = npcY
            throwX = npcX
            randomColour = random.randint(0, 3)
            if randomColour == 1:
                screen.blit(pygame.transform.scale(recycleItemImg, (50,50)), (throw.x, throw.y))
            elif randomColour == 2:
                screen.blit(pygame.transform.scale(garbageItemImg, (50,50)), (throw.x, throw.y))
            elif randomColour == 3:
                screen.blit(pygame.transform.scale(compostItemImg, (50,50)), (throw.x, throw.y))
        

        npc = npcObject(npcX, npcY, 100, 100)
        if npcX > screenWidth:
            npcX = -100
        
        npcX += npcSpeed
        pygame.draw.rect(screen, BLACK, npc)

        throwY += throwSpeed
        screen.blit(pygame.transform.scale(recycleItemImg, (50,50)), (throw.x, throw.y))
                
        # Draw and optionally update falling objects
        for obj in falling_objects:
            if not pause:
                obj.y += FALL_SPEED  # Only update position if not paused
            if obj == recycle:
                screen.blit(pygame.transform.scale(recycleItemImg, (50,50)), (obj.x, obj.y))
                if (recycle.colliderect(player) and playerRecycle):
                    falling_objects.remove(obj)
                    level2Score += 1
                    playerRecycle = False
            elif obj == garbage:
                screen.blit(pygame.transform.scale(garbageItemImg, (50,50)), (obj.x, obj.y))
                if (garbage.colliderect(player) and playerGarbage):
                    falling_objects.remove(obj)
                    level2Score += 1
                    playerGarbage = False
            elif obj == compost:
                screen.blit(pygame.transform.scale(compostItemImg, (50,50)), (obj.x, obj.y))
                if (compost.colliderect(player) and playerCompost):
                    falling_objects.remove(obj)
                    level2Score += 1
                    playerCompost = False
        screen.blit(level2Text, (screenWidth/2 - 100, 25))
        pygame.draw.rect(screen, BLACK, pauseButton)
        screen.blit(pauseSymbol, (screenWidth - 61, 22))
        screen.blit(score2Text, (25, 25))
        nextLevel = False
        if level2Score >= 30:
            score2Number = titleScreenButtonFont.render(str(level2Score), True, BLACK)
            screen.blit(congratulationsText, (screenWidth/2 - 650, screenHeight/2 - 250))
            nextLevel = True
        # Frame delay and display update
        screen.blit(score2Number, (255, 25))
        time.sleep(1 / 60)
        pygame.display.update()
        if nextLevel:
            pygame.time.delay(3000)
            level2Score = 0
            falling_objects.clear()
            level3Score = 0
            playerX = screenWidth/2 - 50
            playerY = screenHeight - 125
            playerCompost = False
            playerGarbage = False
            playerRecycle = False
            level2Run = False
            level3Run = True
            nextLevel = False
            fromLevel2 = True
    while level3Run:
        if fromLevel2:
            pygame.time.set_timer(RECYCLE_SPAWN_EVENT, RECYCLE_SPAWN_INTERVAL)
            pygame.time.set_timer(GARBAGE_SPAWN_EVENT, GARBAGE_SPAWN_INTERVAL)
            pygame.time.set_timer(COMPOST_SPAWN_EVENT, COMPOST_SPAWN_INTERVAL)
            fromLevel2 = False
        screen_info = pygame.display.Info()
        screenWidth = screen_info.current_w
        screenHeight = screen_info.current_h
        level3Text = titleScreenButtonFont.render("LEVEL 3", True, BLACK)
        score3Text = titleScreenButtonFont.render("SCORE:", True, BLACK)
        score3Number = titleScreenButtonFont.render(str(level3Score), True, BLACK)
        congratulationsText = titleTextFont.render("CONGRATULATIONS!", True, BLACK)
        player = playerObject(playerX, playerY, 100, 100)
        (mx, my) = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            playerX = playerX - 20
        if keys[pygame.K_RIGHT]:
            playerX = playerX + 20
        if playerX > screenWidth - 100:
            playerX = screenWidth - 100
        if playerX < 0:
            playerX = 0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                level3Run = False
            if event.type == pygame.MOUSEMOTION:
                playerX,playerY = pygame.mouse.get_pos()
                playerY = screenHeight - 125
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    playerRecycle = True
                    playerGarbage = False
                    playerCompost = False
                elif event.key == pygame.K_2:
                    playerGarbage = True
                    playerRecycle = False
                    playerCompost = False
                elif event.key == pygame.K_3:
                    playerCompost = True
                    playerGarbage = False
                    playerRecycle = False
            # Pause functionality
            if event.type == pygame.MOUSEBUTTONDOWN and pauseButton.collidepoint(mx, my):
                pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                    'buttonFont': titleScreenButtonFont,
                }, {
                    'WHITE': WHITE,
                    'BLACK': BLACK,
                }, playMusic)
                if pauseResult == "levelSelector":
                    levelSelector = True
                    level3Run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pauseResult = pause_menu(screen, screenWidth, screenHeight, {
                        'buttonFont': titleScreenButtonFont,
                    }, {
                        'WHITE': WHITE,
                        'BLACK': BLACK,
                    }, playMusic)
                    if pauseResult == "levelSelector":
                        levelSelector = True
                        level3Run = False
                    break
            # Object height reset
            if event.type == RECYCLE_SPAWN_EVENT and not pause:
                x_position = random.randint(0, screenWidth - RECYCLE_SIDE)
                recycle = pygame.Rect(x_position, 0, RECYCLE_SIDE, RECYCLE_SIDE)
                falling_objects.append(recycle)
            elif event.type == GARBAGE_SPAWN_EVENT and not pause:
                x1_position = random.randint(0, screenWidth - GARBAGE_SIDE)
                garbage = pygame.Rect(x1_position, 0, GARBAGE_SIDE, GARBAGE_SIDE)
                falling_objects.append(garbage)
            elif event.type == COMPOST_SPAWN_EVENT and not pause:
                x2_position = random.randint(0, screenWidth - COMPOST_SIDE)
                compost = pygame.Rect(x2_position, 0, COMPOST_SIDE, COMPOST_SIDE)
                falling_objects.append(compost)
            
        # Fill the screen and draw the pause button
        screen.blit(pygame.transform.scale(levelBackgroundImg, (screenWidth, screenHeight)), (0,0))
        pauseButton = pygame.Rect(screenWidth - 75, 25, 50, 50)
        pauseSymbol = pauseSymbolFont.render("II", True, WHITE)
        if playerRecycle:
            pygame.Surface.fill(screen, BLUE, player)
        elif playerGarbage:
            pygame.Surface.fill(screen, RED, player)
        elif playerCompost:
            pygame.Surface.fill(screen, GREEN, player)
        else:
            pygame.Surface.fill(screen, ORANGE, player)
        




        # Draw and optionally update falling objects
        for obj in falling_objects:
            if not pause:
                obj.y += FALL_SPEED  # Only update position if not paused
            if obj == recycle:
                pygame.draw.rect(screen, RECYCLE_COLOR, obj)
                if (recycle.colliderect(player) and playerRecycle):
                    falling_objects.remove(obj)
                    level3Score += 1
                    playerRecycle = False
            elif obj == garbage:
                pygame.draw.rect(screen, GARBAGE_COLOR, obj)
                if (garbage.colliderect(player) and playerGarbage):
                    falling_objects.remove(obj)
                    level3Score += 1
                    playerGarbage = False
            elif obj == compost:
                pygame.draw.rect(screen, COMPOST_COLOR, obj)
                if (compost.colliderect(player) and playerCompost):
                    falling_objects.remove(obj)
                    level3Score += 1
                    playerCompost = False
        screen.blit(level3Text, (screenWidth/2 - 100, 25))
        pygame.draw.rect(screen, BLACK, pauseButton)
        screen.blit(pauseSymbol, (screenWidth - 61, 22))
        screen.blit(score3Text, (25, 25))
        # Frame delay and display update
        screen.blit(score3Number, (255, 25))
        time.sleep(1 / 60)
        pygame.display.update()