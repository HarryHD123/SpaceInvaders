# --- SPACE INVADERS --- #

# Import Modules
import pygame
import random
import time
import shelve

# Initiate Game
pygame.init()
pygame.mixer.init()

# ---CONSTANTS---

# FrameRate
FPS = 60

# Set Screen Resolution (Game will still run if tweaked, too large an adjustment to width will cause issues however)
# Screen width and height in a similar ratio as the original space invaders
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

# Colours
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
SMALL_FONT = pygame.font.SysFont("monospace", 20)
MED_FONT = pygame.font.SysFont("aettenschweiler", 50)
LARGE_FONT = pygame.font.SysFont("aettenschweiler", 100)

# Music
PLACEHOLDER = "Sounds/SOUND PLACEHOLDER.WAV"
FIRSTNOTE = "Sounds/SOUND FirstNote.WAV"
SECONDNOTE = "Sounds/SOUND SecondNote.WAV"
THIRDNOTE = "Sounds/SOUND ThirdNote.WAV"
FOURTHNOTE = "Sounds/SOUND FourthNote.WAV"

# Shield Dimensions
SHIELD_WIDTH = SCREEN_WIDTH / 80
SHIELD_HEIGHT = SCREEN_HEIGHT / 80


# ---CLASSES---

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y, Image, ImageShooting, ImageExplode):
        super().__init__()

        self.image = pygame.image.load(Image).convert()
        self.image_shoot = pygame.image.load(ImageShooting).convert()
        self.image_explode = pygame.image.load(ImageExplode).convert()

        # Passed in Location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def Shoot(self):
        NewBullet = Bullet(self.rect.x + 23, self.rect.y, 12)
        pygame.mixer.music.load("Sounds/SOUND PlayerShoot.WAV")
        pygame.mixer.music.play(1)
        self.image = self.image_shoot
        return NewBullet

    def Explode(self):
        self.image = self.image_explode


class Invader(pygame.sprite.Sprite):
    def __init__(self, x, y, ScoreValue, ShotFreq, Image):
        super().__init__()

        self.image = pygame.image.load(Image).convert()

        # Passed in Location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Speed vector
        self.change_x = 15
        self.change_y = 50

        # Score Value
        self.score = ScoreValue

        # Shot Frequency
        self.shot_freq = ShotFreq

    def InvaderShoot(self):
        NewBullet = Bullet(self.rect.x + 15, self.rect.y + 10, -5)
        return NewBullet

    # Allows invader to shoot at random points. Different shot frequency can be set for a harder invader
    def RandShooting(self):
        EnemyShoot = 1
        RandNum = random.randint(1, self.shot_freq)
        if RandNum == EnemyShoot:
            NewBullet = Invader.InvaderShoot(self)
            return NewBullet

    def UpdateX(self):
        # New x for invader
        self.rect.x += self.change_x

    def UpdateY(self):
        self.rect.y += self.change_y


class Shield(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        # Image created
        self.image = pygame.Surface([SHIELD_WIDTH, SHIELD_HEIGHT])
        self.image.fill(GREEN)

        # Passed in Location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, Speed):
        super().__init__()

        self.image = pygame.Surface([3, 10])
        self.image.fill(WHITE)

        # Passed in Location
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # Speed vector
        self.change_y = Speed

    def Update(self):
        # New position for bullet
        self.rect.y -= self.change_y


# ---FUNCTIONS---

def TextObjects(Text, Font, Colour, Centre):
    TextSurface = Font.render(Text, True, Colour)
    TextSurface_rect = TextSurface.get_rect()
    TextSurface_rect.center = Centre
    return TextSurface, TextSurface_rect


def DisplayMessage(Text, Font, Colour, Screen, Centre):
    Text, Text_rect = TextObjects(Text, Font, Colour, Centre)
    Screen.blit(Text, Text_rect)


def DisplayImage(Image, Screen, x, y):
    Image = pygame.image.load(Image).convert()
    Screen.blit(Image, (x, y))


def UpdateHighScore(Score, HighScoreFile):
    if "HighScore" in HighScoreFile:
        HighScore = HighScoreFile["HighScore"]
        if Score > HighScore:
            HighScoreFile["HighScore"] = Score
            HighScoreFile.close()
        else:
            HighScoreFile.close()


def SpawnInvaders(RowNumber, InvadersPerRow, ScoreValue, ShotFreq, Image):
    InvaderList = []
    for Index in range(InvadersPerRow):
        x = (SCREEN_WIDTH - SCREEN_WIDTH / 3) / (InvadersPerRow + 1) * (Index + 1) - SCREEN_WIDTH / 40
        y = SCREEN_HEIGHT / 6 + SCREEN_HEIGHT / 18 * RowNumber
        Inv = Invader(x, y, ScoreValue, ShotFreq, Image)
        InvaderList.append(Inv)
    return InvaderList


def SpawnShields(ShieldsPerBlock, NumBlocks, NumRows):
    ShieldList = []
    for IndexShieldsPerBlock in range(int(-ShieldsPerBlock / 2), int(ShieldsPerBlock / 2)):
        for IndexRowNumber in range(NumRows):
            y = SCREEN_HEIGHT - (100 + ((SHIELD_HEIGHT - 1) * (IndexRowNumber - 1)))
            for IndexBlockNumber in range(NumBlocks):
                x = (SCREEN_WIDTH / NumBlocks) * IndexBlockNumber + (
                        (SCREEN_WIDTH / NumBlocks) / 2) + IndexShieldsPerBlock * (SHIELD_WIDTH - 1)
                Shi = Shield(x, y)
                ShieldList.append(Shi)
    return ShieldList


def Levels(Level):
    InvaderList = []
    if Level == 1:
        InvaderList = [Level1()]
    if Level == 2:
        InvaderList = [Level2()]
    if Level == 3:
        InvaderList = [Level3()]
    if Level == 4:
        InvaderList = [Level4()]
    if Level == 5:
        InvaderList = [Level5()]
    return InvaderList


# Levels here can be changed easily
def Level1():
    InvaderList = [SpawnInvaders(1, 11, 50, 3000, "Images/IMG Invader3.png"),
                   SpawnInvaders(2, 11, 20, 5000, "Images/IMG Invader2.png"),
                   SpawnInvaders(3, 11, 20, 5000, "Images/IMG Invader2.png"),
                   SpawnInvaders(4, 11, 10, 7500, "Images/IMG Invader1.png"),
                   SpawnInvaders(5, 11, 10, 7500, "Images/IMG Invader1.png")]
    # SpawnInvaders(RowNumber (From top to Bottom), InvadersPerRow, ScoreValue, ShotFreq (Lower = Higher Freq), Image)
    return InvaderList


def Level2():
    InvaderList = [SpawnInvaders(2, 11, 70, 2500, "Images/IMG Invader3.png"),
                   SpawnInvaders(3, 11, 50, 3000, "Images/IMG Invader2.png"),
                   SpawnInvaders(4, 11, 50, 3000, "Images/IMG Invader2.png"),
                   SpawnInvaders(5, 11, 20, 5000, "Images/IMG Invader1.png"),
                   SpawnInvaders(6, 11, 20, 5000, "Images/IMG Invader1.png")]
    # SpawnInvaders(RowNumber (From top to Bottom), InvadersPerRow, ScoreValue, ShotFreq (Lower = Higher Freq), Image)
    return InvaderList


def Level3():
    InvaderList = [SpawnInvaders(3, 10, 200, 1000, "Images/IMG Invader3.png"),
                   SpawnInvaders(4, 10, 100, 2000, "Images/IMG Invader2.png"),
                   SpawnInvaders(5, 10, 100, 2000, "Images/IMG Invader2.png"),
                   SpawnInvaders(6, 10, 50, 3000, "Images/IMG Invader1.png"),
                   SpawnInvaders(7, 10, 50, 3000, "Images/IMG Invader1.png")]
    # SpawnInvaders(RowNumber (From top to Bottom), InvadersPerRow, ScoreValue, ShotFreq (Lower = Higher Freq), Image)
    return InvaderList


def Level4():
    InvaderList = [SpawnInvaders(4, 8, 300, 500, "Images/IMG Invader3.png"),
                   SpawnInvaders(5, 8, 200, 1000, "Images/IMG Invader2.png"),
                   SpawnInvaders(6, 8, 200, 1000, "Images/IMG Invader2.png"),
                   SpawnInvaders(7, 8, 100, 2000, "Images/IMG Invader1.png"),
                   SpawnInvaders(8, 8, 100, 2000, "Images/IMG Invader1.png")]
    # SpawnInvaders(RowNumber (From top to Bottom), InvadersPerRow, ScoreValue, ShotFreq (Lower = Higher Freq), Image)
    return InvaderList


def Level5():
    InvaderList = [SpawnInvaders(5, 7, 500, 250, "Images/IMG Invader3.png"),
                   SpawnInvaders(6, 7, 300, 500, "Images/IMG Invader2.png"),
                   SpawnInvaders(7, 7, 300, 500, "Images/IMG Invader2.png"),
                   SpawnInvaders(8, 7, 200, 1000, "Images/IMG Invader1.png"),
                   SpawnInvaders(9, 7, 200, 1000, "Images/IMG Invader1.png")]
    # SpawnInvaders(RowNumber (From top to Bottom), InvadersPerRow, ScoreValue, ShotFreq (Lower = Higher Freq), Image)
    return InvaderList


# Main Loop
def SettingsLoop():
    # --Setting Variables--

    # Create a screen and set a clock
    SettingsScreen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    Clock = pygame.time.Clock()

    # Starting Variables (Adjustable)
    TwoPlayer = False
    Lives = 3  # Starting lives
    Score = 0  # Starting score
    ReloadTime = 0.75  # Player shooting delay (lower is faster) (Not less than 0.3!)
    MovementSensitivity = 3.5  # Player movement sensitivity
    TimeForInvaderUpdateX = 1.05  # The time per invader movement (lower is faster)
    InvaderSpeedUpIncrease = 0.7  # Adjusts the delay for invaders to move for every change in y (lower is faster)
    InvaderSpeedUpIncreaseReductionPerY = 1.05  # The reduction in invader speed up amount per change in y (higher is
    # more)
    InvaderShotFreqIncrease = 1.2  # How much more frequently the invaders shoot for every change in y (higher is more)
    InvaderUpdateXSpeedUpPerLevel = 0.05  # How much faster the invaders will start per level (higher is faster)

    Level = 1  # Starting Level
    ExtraLifePerLevel = True  # Whether or not player gains a life for each level completed

    # Working Variables (Do Not Adjust)
    Done = False

    # --Settings Loop--
    while not Done:

        SettingsScreen.fill(BLACK)
        DisplayMessage("SPACE INVADERS", LARGE_FONT, GREEN, SettingsScreen,
                       (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 8))
        DisplayMessage("5 Waves of Survival", MED_FONT, GREEN, SettingsScreen,
                       (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5))
        DisplayMessage("Press Enter to Start", MED_FONT, GREEN, SettingsScreen,
                       (SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 4))

        DisplayImage("Images/IMG Invader3.png", SettingsScreen, SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 5)
        DisplayImage("Images/IMG Invader2.png", SettingsScreen, SCREEN_WIDTH / 2 - SCREEN_WIDTH / 20,
                     SCREEN_HEIGHT - SCREEN_HEIGHT / 5)
        DisplayImage("Images/IMG Invader1.png", SettingsScreen, SCREEN_WIDTH / 2 + SCREEN_WIDTH / 20,
                     SCREEN_HEIGHT - SCREEN_HEIGHT / 5)

        # Displays Instructions and HighScore
        if not TwoPlayer:
            DisplayMessage("Use <- and -> to move. Click the space bar to shoot", SMALL_FONT, WHITE, SettingsScreen,
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            HighScoreFile = shelve.open("HighScores/HighScore.txt")
            if "HighScore" in HighScoreFile:
                DisplayMessage("HIGHSCORE:" + str(HighScoreFile["HighScore"]), MED_FONT, GREEN, SettingsScreen,
                               (SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 3))
            else:
                HighScoreFile["HighScore"] = 0
        if TwoPlayer:
            DisplayMessage("PLAYER 1: Use <- and -> to move and the UP key to shoot", SMALL_FONT, WHITE, SettingsScreen,
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            DisplayMessage("PLAYER 2: Use A and D to move and W to shoot", SMALL_FONT, WHITE,
                           SettingsScreen,
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3 + SCREEN_HEIGHT / 20))
            HighScoreFile = shelve.open("HighScores/MultiplayerHighScore.txt")
            if "HighScore" in HighScoreFile:
                DisplayMessage("HIGHSCORE:" + str(HighScoreFile["HighScore"]), MED_FONT, GREEN, SettingsScreen,
                               (SCREEN_WIDTH / 2, SCREEN_HEIGHT - SCREEN_HEIGHT / 3))
            else:
                HighScoreFile["HighScore"] = 0

        MultiplayerClickBox = pygame.Rect(0, 0, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 20)
        MultiplayerClickBox.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        if TwoPlayer:
            Multiplayer = "Activated"
        else:
            Multiplayer = "Deactivated"
        DisplayMessage("Multiplayer Mode:" + Multiplayer, SMALL_FONT, WHITE, SettingsScreen,
                       (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

        for event in pygame.event.get():
            # quits game if X clicked in top corner
            if event.type == pygame.QUIT:
                Done = True
            if event.type == pygame.KEYDOWN:
                if event.key == 13:  # 13 is the number of the enter key
                    Done = True
            if event.type == pygame.MOUSEBUTTONDOWN:

                if MultiplayerClickBox.collidepoint(event.pos):
                    TwoPlayer = not TwoPlayer

        pygame.display.flip()

        Clock.tick(FPS)

    return TwoPlayer, Lives, Score, ReloadTime, MovementSensitivity, TimeForInvaderUpdateX, InvaderSpeedUpIncrease, \
           InvaderShotFreqIncrease, Level, ExtraLifePerLevel, InvaderUpdateXSpeedUpPerLevel, \
           InvaderSpeedUpIncreaseReductionPerY


def GameLoop(TwoPlayer, Lives, Score, ReloadTime, MovementSensitivity, TimeForInvaderUpdateX, InvaderSpeedUpIncrease,
             InvaderShotFreqIncrease, Level, InvaderUpdateXSpeedUpPerLevel, InvaderSpeedUpIncreaseReductionPerY):
    # --Setting Variables--

    # Create a screen and set a clock
    GameScreen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
    Clock = pygame.time.Clock()

    # Working Variables (Do Not Adjust)
    LastShotTime = 0
    Reloading = False
    PressedKeys = {"left": False, "right": False}
    LastInvaderUpdateX = 0
    Move = False
    ChangeDirectionYSpeedShotFreq = False
    InvaderLanded = False
    ThemeNote = FIRSTNOTE
    RUNNING, PAUSED, GAMEOVER, VICTORY = 0, 1, 2, 3
    State = RUNNING
    Done = False
    Restart = False
    LevelUp = False

    # Player1 Created
    Player1 = Player((SCREEN_WIDTH - 50) / 2, SCREEN_HEIGHT - 70, 'Images/IMG Player1.png',
                     'Images/IMG Player1Shoot.png', 'Images/IMG Player1Explosion.png')
    PlayerList = [Player1]

    # Player2 Created if Multiplayer Selected
    if TwoPlayer:
        Player2 = Player((SCREEN_WIDTH - 50) / 2, SCREEN_HEIGHT - 70, 'Images/IMG Player2.png',
                         'Images/IMG Player2Shoot.png', 'Images/IMG Player2Explosion.png')
        PlayerList.append(Player2)
        LastShotTimeP2 = 0
        ReloadingP2 = False
        PressedKeysP2 = {"left": False, "right": False}

    PlayerList = pygame.sprite.Group(PlayerList)

    # Invaders Created
    InvaderList = [Levels(Level)]
    InvaderList = pygame.sprite.Group(InvaderList)
    InvaderKillList = []

    # Shields Created
    ShieldList = [SpawnShields(10, 4, 5)]
    # SpawnShields(ShieldsPerBlock, NumBlocks, NumRows)
    ShieldList = pygame.sprite.Group(ShieldList)

    # Bullet Lists Created
    Bullets = []
    InvaderBullets = []

    # Sprites Added
    all_sprites_list = pygame.sprite.Group()
    all_sprites_list.add(PlayerList, InvaderList, ShieldList)

    # --GameLoop--
    while not Done:
        if State == RUNNING:

            # Player Controls
            for event in pygame.event.get():
                # quits game if X clicked in top corner
                if event.type == pygame.QUIT:
                    Done = True

                elif event.type == pygame.KEYDOWN:
                    # shoots when space clicked
                    if event.key == pygame.K_SPACE and not TwoPlayer:
                        # If reload time has elapsed allows a shot to be fired
                        if time.perf_counter() - LastShotTime > ReloadTime:
                            Reloading = False
                        if not Reloading:
                            NewBullet = Player.Shoot(Player1)
                            all_sprites_list.add(NewBullet)
                            Bullets.append(NewBullet)
                            LastShotTime = time.perf_counter()
                            Reloading = True
                    # Pressing keys and letting go adjust a variable so the player can hold keys to move smoothly
                    if event.key == pygame.K_LEFT:
                        PressedKeys["left"] = True
                    if event.key == pygame.K_RIGHT:
                        PressedKeys["right"] = True
                    if event.key == pygame.K_p:
                        State = PAUSED

                    if TwoPlayer:
                        if event.key == pygame.K_w:
                            # If reload time has elapsed allows a shot to be fired
                            if time.perf_counter() - LastShotTimeP2 > ReloadTime:
                                ReloadingP2 = False
                            if not ReloadingP2:
                                NewBullet = Player.Shoot(Player2)
                                all_sprites_list.add(NewBullet)
                                Bullets.append(NewBullet)
                                LastShotTimeP2 = time.perf_counter()
                                ReloadingP2 = True
                        # Swaps player 1 shoot to up if two player so players hands don't get in each others way
                        if event.key == pygame.K_UP:
                            # If reload time has elapsed allows a shot to be fired
                            if time.perf_counter() - LastShotTime > ReloadTime:
                                Reloading = False
                            if not Reloading:
                                NewBullet = Player.Shoot(Player1)
                                all_sprites_list.add(NewBullet)
                                Bullets.append(NewBullet)
                                LastShotTime = time.perf_counter()
                                Reloading = True
                        # Pressing keys and letting go adjust a variable so the player can hold keys to move smoothly
                        if event.key == pygame.K_a:
                            PressedKeysP2["left"] = True
                        if event.key == pygame.K_d:
                            PressedKeysP2["right"] = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        PressedKeys["left"] = False
                    if event.key == pygame.K_RIGHT:
                        PressedKeys["right"] = False

                    if TwoPlayer:
                        if event.key == pygame.K_a:
                            PressedKeysP2["left"] = False
                        elif event.key == pygame.K_d:
                            PressedKeysP2["right"] = False

            # Moves player and sets boundaries
            if PressedKeys["right"]:
                if Player1.rect.x < SCREEN_WIDTH - 70 * SCREEN_WIDTH / 896:
                    Player1.rect.x += MovementSensitivity
            if PressedKeys["left"]:
                if Player1.rect.x > 10 * SCREEN_WIDTH / 784:
                    Player1.rect.x -= MovementSensitivity

            if TwoPlayer:
                if PressedKeysP2["right"]:
                    if Player2.rect.x < SCREEN_WIDTH - 70 * SCREEN_WIDTH / 896:
                        Player2.rect.x += MovementSensitivity
                if PressedKeysP2["left"]:
                    if Player2.rect.x > 10 * SCREEN_WIDTH / 784:
                        Player2.rect.x -= MovementSensitivity

            # Invaders will move per unit time and a note will play every time they move
            if time.perf_counter() - LastInvaderUpdateX > TimeForInvaderUpdateX - \
                    (InvaderUpdateXSpeedUpPerLevel * Level):
                Move = True
            if Move:
                for Enemy in InvaderList:
                    Invader.UpdateX(Enemy)
                    LastInvaderUpdateX = time.perf_counter()
                pygame.mixer.music.load(ThemeNote)
                pygame.mixer.music.play(1)
                Move = False
                # Changes Note
                if ThemeNote == FOURTHNOTE:
                    ThemeNote = PLACEHOLDER
                if ThemeNote == THIRDNOTE:
                    ThemeNote = FOURTHNOTE
                if ThemeNote == SECONDNOTE:
                    ThemeNote = THIRDNOTE
                if ThemeNote == FIRSTNOTE:
                    ThemeNote = SECONDNOTE
                if ThemeNote == PLACEHOLDER:
                    ThemeNote = FIRSTNOTE

            # Y movement, shooting for invaders and checks if colliding with shields
            for Enemy in InvaderList:

                # Checks if an invader collides with a shield or has passed it and removes the shield if it does
                pygame.sprite.spritecollide(Enemy, ShieldList, True)
                for Barrier in ShieldList:
                    if Enemy.rect.y > Barrier.rect.y and Enemy.rect.x >= Barrier.rect.x:
                        Barrier.kill()
                        ShieldList.remove(Barrier)

                # All invaders remaining will shoot at randomly intervals
                NewBullet = Invader.RandShooting(Enemy)
                if NewBullet is not None:
                    all_sprites_list.add(NewBullet)
                    InvaderBullets.append(NewBullet)
                # If any invader hits the side of the screen all invaders will change their direction,
                # move down and speed up
                if Enemy.rect.x > SCREEN_WIDTH - 50 or Enemy.rect.x < 0:
                    ChangeDirectionYSpeedShotFreq = True

            if ChangeDirectionYSpeedShotFreq:
                for Enemy in InvaderList:
                    Invader.UpdateY(Enemy)
                    Enemy.rect.x -= Enemy.change_x
                    Enemy.change_x = - Enemy.change_x
                    Enemy.shot_freq = int(Enemy.shot_freq / InvaderShotFreqIncrease)
                    # If an invader lands the player loses
                    if Enemy.rect.y >= Player1.rect.y:
                        InvaderLanded = True
                # Invaders are sped up
                TimeForInvaderUpdateX *= InvaderSpeedUpIncrease
                if InvaderSpeedUpIncrease < 1:
                    InvaderSpeedUpIncrease *= InvaderSpeedUpIncreaseReductionPerY
                # Resets variable
                ChangeDirectionYSpeedShotFreq = False

            # Checks player bullets
            for Ammo in Bullets:
                Ammo.Update()
                # Checks if a player bullet collides with an invader and removes the bullet if it does
                InvaderKillList = pygame.sprite.spritecollide(Ammo, InvaderList, False)
                if len(InvaderKillList) > 0:
                    Ammo.kill()
                    Bullets.remove(Ammo)
                # Plays invader killed sound, shows explosion and adds to overall score
                for Enemy in InvaderKillList:
                    pygame.mixer.music.load("Sounds/SOUND InvaderKilled.WAV")
                    pygame.mixer.music.play(1)
                    Enemy.image = pygame.image.load('Images/IMG InvaderKilled.png').convert()
                    Score += Enemy.score
                # Checks if a player bullet collides with a shield, removes the shield and bullet if it does
                ShieldDamageFriendly = pygame.sprite.spritecollide(Ammo, ShieldList, True)
                if len(ShieldDamageFriendly) != 0:
                    Ammo.kill()
                    Bullets.remove(Ammo)
                # Any bullet off the screen is removed
                if Ammo.rect.y < -10:
                    Ammo.kill()
                    Bullets.remove(Ammo)

            # Checks invader bullets
            for Ammo in InvaderBullets:
                Ammo.Update()
                # Checks if an invader bullet collides with the player, removes a life and bullet if it does
                LivesLost = pygame.sprite.spritecollide(Ammo, PlayerList, False)
                if len(LivesLost) != 0:
                    Ammo.kill()
                    InvaderBullets.remove(Ammo)
                    Lives -= 1
                    # Players Flash Red when a life is lost
                    for P in PlayerList:
                        P.image = pygame.image.load('Images/IMG PlayerLifeLost.png').convert()
                # Checks if an invader bullet collides with a shield, removes the shield and bullet if it does
                ShieldDamage = pygame.sprite.spritecollide(Ammo, ShieldList, True)
                if len(ShieldDamage) != 0:
                    Ammo.kill()
                    InvaderBullets.remove(Ammo)
                # Any invader bullet off the screen is removed
                if Ammo.rect.y > SCREEN_HEIGHT:
                    Ammo.kill()
                    InvaderBullets.remove(Ammo)

            # Game Over Protocol
            if Lives <= 0 or InvaderLanded:
                pygame.mixer.music.load("Sounds/SOUND PlayerKilled.WAV")
                pygame.mixer.music.play(1)
                for P in PlayerList:
                    P.Explode()
                State = GAMEOVER

            # Victory Protocol
            if len(InvaderList) == 0:
                State = VICTORY

            # Redraws screen
            GameScreen.fill(BLACK)
            all_sprites_list.draw(GameScreen)

            # Adds lives at top
            DisplayMessage("Lives: " + str(Lives), SMALL_FONT, WHITE, GameScreen,
                           (SCREEN_WIDTH - SCREEN_WIDTH * 0.1, SCREEN_HEIGHT * 0.03))
            # Adds score at top
            DisplayMessage("Score: " + str(Score), SMALL_FONT, WHITE, GameScreen,
                           (SCREEN_WIDTH * 0.12, SCREEN_HEIGHT * 0.03))

            # Adds level at top
            DisplayMessage("Level " + str(Level), SMALL_FONT, WHITE, GameScreen,
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.03))

            # Resets Player Image after shooting
            Player1.image = pygame.image.load('Images/IMG Player1.png').convert()
            if TwoPlayer:
                Player2.image = pygame.image.load('Images/IMG Player2.png').convert()

            # Removes Invader after it explodes
            for Enemy in InvaderKillList:
                Enemy.kill()
                InvaderList.remove(Enemy)
                InvaderKillList.remove(Enemy)

        # GameOver Protocol
        elif State == GAMEOVER:
            DisplayMessage("GAME OVER!", LARGE_FONT, RED, GameScreen,
                           (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2 - (SCREEN_HEIGHT / 12))))
            DisplayMessage("Press R to Restart the level with 3 lives", MED_FONT, RED, GameScreen,
                           (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2 - (SCREEN_HEIGHT / 3))))
            DisplayMessage("or Q to Quit", MED_FONT, RED, GameScreen,
                           (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2 - (SCREEN_HEIGHT / 3) + SCREEN_HEIGHT / 20)))

            if not TwoPlayer:
                HighScoreFile = shelve.open("HighScores/HighScore.txt")
                HighScore = HighScoreFile["HighScore"]
                if Score > HighScore:
                    DisplayMessage("NEW HIGHSCORE SET!", MED_FONT, RED, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, RED, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 15))
                if Score <= HighScore:
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, RED, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            if TwoPlayer:
                HighScoreFile = shelve.open("HighScores/MultiplayerHighScore.txt")
                HighScore = HighScoreFile["HighScore"]
                if Score > HighScore:
                    DisplayMessage("NEW HIGHSCORE SET!", MED_FONT, RED, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, RED, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 15))
                if Score <= HighScore:
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, RED, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        Lives = 3
                        Restart = True
                        Done = True
                    if event.key == pygame.K_q:
                        Done = True

        # Victory Protocol
        elif State == VICTORY:
            DisplayMessage("YOU WIN!", LARGE_FONT, WHITE, GameScreen,
                           (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2 - (SCREEN_HEIGHT / 12))))
            if Level != 5:
                DisplayMessage("Press N for the Next Level or Q to Quit", MED_FONT, WHITE, GameScreen,
                               (SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2 - (SCREEN_HEIGHT / 3))))

            if not TwoPlayer:
                HighScoreFile = shelve.open("HighScores/HighScore.txt")
                HighScore = HighScoreFile["HighScore"]
                if Score > HighScore:
                    DisplayMessage("NEW HIGHSCORE SET!", MED_FONT, WHITE, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, WHITE, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 15))
                if Score <= HighScore:
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, WHITE, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            if TwoPlayer:
                HighScoreFile = shelve.open("HighScores/MultiplayerHighScore.txt")
                HighScore = HighScoreFile["HighScore"]
                if Score > HighScore:
                    DisplayMessage("NEW HIGHSCORE SET!", MED_FONT, WHITE, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, WHITE, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 15))
                if Score <= HighScore:
                    DisplayMessage("SCORE:" + str(Score), LARGE_FONT, WHITE, GameScreen,
                                   (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Done = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_n:
                        LevelUp = True
                        Restart = True
                        Done = True
                    if event.key == pygame.K_q:
                        Done = True

        # Pause Protocol
        elif State == PAUSED:
            DisplayMessage("PAUSED", LARGE_FONT, GREEN, GameScreen,
                           (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    Done = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        State = RUNNING

        # Makes the game appear in the window
        pygame.display.flip()

        Clock.tick(FPS)

    return Restart, LevelUp, Lives, Score, GameScreen


def MainLoop():
    Play = True
    # Saves settings into a variable
    ChosenSettings = SettingsLoop()
    Level = ChosenSettings[8]
    Lives = ChosenSettings[1]
    Score = ChosenSettings[2]
    # Main Loop
    while Play:
        ContinueOptions = GameLoop(ChosenSettings[0], Lives, Score, ChosenSettings[3], ChosenSettings[4],
                                   ChosenSettings[5], ChosenSettings[6], ChosenSettings[7], Level, ChosenSettings[10],
                                   ChosenSettings[11])
        Play = ContinueOptions[0]
        LevelUp = ContinueOptions[1]
        Lives = ContinueOptions[2]

        # Saves HighScore if a new one has been set
        Score = ContinueOptions[3]
        if not ChosenSettings[0]:
            HighScoreFile = shelve.open("HighScores/HighScore.txt")
            UpdateHighScore(Score, HighScoreFile)

        if ChosenSettings[0]:
            HighScoreFile = shelve.open("HighScores/MultiplayerHighScore.txt")
            UpdateHighScore(Score, HighScoreFile)

        # Moves to the next level if the previous one has been completed has been completed
        if LevelUp:
            Score = ContinueOptions[3]
            Level += 1
            if ChosenSettings[9]:
                Lives += 1

    # Ends programme
    pygame.quit()


# ---MAIN---

if __name__ == "__main__":
    MainLoop()