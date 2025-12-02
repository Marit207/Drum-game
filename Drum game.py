import pygame
from sys import exit
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()

SCREEN_WIDTH = 950
SCREEN_HEIGTH = 800

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGTH))
pygame.display.set_caption("Drum game")
clock = pygame.time.Clock()
game_active = False
running = True
sticks_neutral_visible = True
stick_hihat_visible = False
stick_snare_visible = False
stick_crash_l_visible = False
stick_hightom_visible = False
stick_midtom_visible = False
stick_floortom_visible = False
stick_ride_visible = False
stick_crash_r_visible = False
kickdrum_visible = False
sticks_visible_list = []

# Timer 
HIHAT_TIMER = pygame.USEREVENT + 1
CRASH_L_TIMER = pygame.USEREVENT + 2
SNARE_TIMER = pygame.USEREVENT + 3
HIGHTOM_TIMER = pygame.USEREVENT + 4
MIDTOM_TIMER = pygame.USEREVENT + 5
FLOORTOM_TIMER = pygame.USEREVENT + 6
RIDE_TIMER = pygame.USEREVENT + 7
CRASH_R_TIMER = pygame.USEREVENT + 8
KICKDRUM_TIMER = pygame.USEREVENT + 9

STICK_NEUTRAL_TIMER = pygame.USEREVENT + 10

# Max 2 sticks visible
def sticks_visible(stick_type):
  global sticks_visible_list
  global stick_hihat_visible, stick_crash_l_visible, stick_snare_visible, stick_hightom_visible, stick_midtom_visible, stick_floortom_visible, stick_ride_visible, stick_crash_r_visible, kickdrum_visible
  
  sticks_visible_list.append(stick_type)
  
  if len(sticks_visible_list) > 2:
    oldest = sticks_visible_list.pop(0)
    if oldest == 'hihat':
      stick_hihat_visible = False
    elif oldest == 'crash l':
      stick_crash_l_visible = False
    elif oldest == 'snare':
      stick_snare_visible = False
    elif oldest == 'hightom':
      stick_hightom_visible = False
    elif oldest == 'midtom':
      stick_midtom_visible = False
    elif oldest == 'floortom':
      stick_floortom_visible = False
    elif oldest == 'ride':
      stick_ride_visible = False
    elif oldest == 'crash r':
      stick_crash_r_visible = False
    elif oldest == 'kickdrum':
      kickdrum_visible = False

  if stick_type == 'hihat':
    stick_hihat_visible = True
  elif stick_type == 'crash l':
    stick_crash_l_visible = True
  elif stick_type == 'snare':
    stick_snare_visible = True
  elif stick_type == 'hightom':
    stick_hightom_visible = True
  elif stick_type == 'midtom':
    stick_midtom_visible = True
  elif stick_type == 'floortom':
    stick_floortom_visible = True
  elif stick_type == 'ride':
    stick_ride_visible = True
  elif stick_type == 'crash r':
    stick_crash_r_visible = True
  elif stick_type == 'kick drum':
    kickdrum_visible = True
 
# Drum sounds
pygame.mixer.set_num_channels(9)

hihat_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\LSD Hat 035 (P).wav')
channel1 = pygame.mixer.Channel(0)

crash_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\Crash_15.wav')
crash_sound.set_volume(0.3)
channel2 = pygame.mixer.Channel(1)

snaredrum_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\LSD Percussion 217 (P).wav')
snaredrum_sound.set_volume(0.7)
channel3 = pygame.mixer.Channel(2)

hightom_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\high-tom-single-hit-c-sharp-key-52-Ih0.wav')
hightom_sound.set_volume(0.6)
channel4 = pygame.mixer.Channel(3)

midtom_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\low-mid-tom-drum-sound-b-key-03-nwl.wav')
midtom_sound.set_volume(0.9)
channel5 = pygame.mixer.Channel(4)

ride_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\Ride_09.wav')
channel6 = pygame.mixer.Channel(5)

floortom_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\low-floor-tom-drum-single-hit-f-sharp-key-34-4H0.wav')
channel7 = pygame.mixer.Channel(6)
channel8 = pygame.mixer.Channel(7)

kick_sound = pygame.mixer.Sound(r'C:\Users\marit\OneDrive\Documenten\Python\Pygame\Drum game\Sounds\Kick_28.wav')
channel9 = pygame.mixer.Channel(8)

# Background
background_drums = pygame.image.load('Background drums.png').convert_alpha()

# Stick image
sticks_neutral = pygame.image.load('Sticks neutral.png').convert_alpha()

# Hit 
hit_hihat = pygame.image.load('hit hi-hat.png').convert_alpha()
hit_crash_l = pygame.image.load('hit crash l.png').convert_alpha()
hit_snare = pygame.image.load('hit snare.png').convert_alpha()
hit_hightom = pygame.image.load('hit hightom.png').convert_alpha()
hit_midtom = pygame.image.load('hit midtom.png').convert_alpha()
hit_floortom = pygame.image.load('hit floortom.png').convert_alpha()
hit_ride = pygame.image.load('hit ride.png').convert_alpha()
hit_crash_r = pygame.image.load('hit crash r.png').convert_alpha()
hit_kickdrum = pygame.image.load('hit kickdrum.png').convert_alpha()

# Text
font = pygame.font.Font(None, 24)
font_title = pygame.font.Font(None, 35)

# Text begin screen
game_title = font_title.render("Drum Game", False, (0, 0, 0))
instruction1 = font.render("How to play:", False, (0, 0, 0))
instruction2 = font.render("Place your fingers on the keyboard as usual, and your thumb on the spacebar.", False, (0, 0, 0))
instruction3 = font.render("Each key corresponds to a component of the drumkit.", False, (0, 0, 0))
instruction4 = font.render("There are 9 components. Use your 8 fingers for the components, plus the thumb for the kick drum.", False, (0, 0, 0))
instruction5 = font.render("The leftmost key corresponds to the leftmost component, and the rightmost key corresponds to the rightmost component.", False, (0, 0, 0))
instruction6 = font.render("For example: A = Hihat. ; = Crash cymbal (right).", False, (0 , 0, 0))
instruction7 = font.render("To start: Press space.", False, (0 , 0, 0))

while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      exit()
    elif event.type == pygame.KEYDOWN:
      if event.key == pygame.K_ESCAPE:
        pygame.quit()
        exit()

    if game_active:
      # Begin screen with neutral sticks
      if sticks_neutral_visible:
        screen.blit(sticks_neutral, (0, 0))
      else:
        screen.blit(background_drums, (0, 0))

      if stick_hihat_visible:
        screen.blit(hit_hihat, (0, 0))
      if stick_snare_visible:
        screen.blit(hit_snare, (0, 0))
      if stick_crash_l_visible:
        screen.blit(hit_crash_l, (0, 0))
      if stick_hightom_visible:
        screen.blit(hit_hightom, (0, 0))
      if stick_midtom_visible:
        screen.blit(hit_midtom, (0, 0))
      if stick_floortom_visible:
        screen.blit(hit_floortom, (0, 0))
      if stick_ride_visible:
        screen.blit(hit_ride, (0, 0))
      if stick_crash_r_visible:
        screen.blit(hit_crash_r, (0, 0))
      if kickdrum_visible:
        screen.blit(hit_kickdrum, (0, 0))
      
      if event.type == pygame.KEYDOWN:
        sticks_neutral_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(STICK_NEUTRAL_TIMER, 3000)

        if event.key == pygame.K_a:
          channel1.play(hihat_sound)
          stick_hihat_visible = True  
          sticks_visible('hihat')
          pygame.time.set_timer(HIHAT_TIMER, 100)
          
        elif event.key == pygame.K_s: 
          channel2.play(crash_sound)
          stick_crash_l_visible = True
          sticks_visible('crash l')
          pygame.time.set_timer(CRASH_L_TIMER, 100)

        elif event.key == pygame.K_d:
          channel3.play(snaredrum_sound)
          stick_snare_visible = True
          sticks_visible('snare')
          pygame.time.set_timer(SNARE_TIMER, 100)

        elif event.key == pygame.K_f:
          channel4.play(hightom_sound)
          stick_hightom_visible = True
          sticks_visible('hightom')
          pygame.time.set_timer(HIGHTOM_TIMER, 100)      

        elif event.key == pygame.K_j:
          channel5.play(midtom_sound)
          stick_midtom_visible = True
          sticks_visible('midtom')
          pygame.time.set_timer(MIDTOM_TIMER, 100)

        elif event.key == pygame.K_k:
          channel6.play(floortom_sound)
          stick_floortom_visible = True
          sticks_visible('floortom')
          pygame.time.set_timer(FLOORTOM_TIMER, 100)

        elif event.key == pygame.K_l:
          channel7.play(ride_sound)
          stick_ride_visible = True
          sticks_visible('ride')
          pygame.time.set_timer(RIDE_TIMER, 100)

        elif event.key == pygame.K_SEMICOLON:
          channel8.play(crash_sound) 
          stick_crash_r_visible = True
          sticks_visible('crash r')
          pygame.time.set_timer(CRASH_R_TIMER, 100)

        elif event.key == pygame.K_SPACE:
          channel9.play(kick_sound)   
          kickdrum_visible = True
          sticks_visible('kick drum')
          pygame.time.set_timer(KICKDRUM_TIMER, 100)
      
      # Set timers to 0
      if event.type == HIHAT_TIMER:
        stick_hihat_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(HIHAT_TIMER, 0)

      elif event.type == CRASH_L_TIMER:
        stick_crash_l_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(CRASH_L_TIMER, 0)

      elif event.type == SNARE_TIMER:
        stick_snare_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(SNARE_TIMER, 0)

      elif event.type == HIGHTOM_TIMER:
        stick_hightom_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(HIGHTOM_TIMER, 0)

      elif event.type == MIDTOM_TIMER:
        stick_midtom_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(MIDTOM_TIMER, 0)

      elif event.type == FLOORTOM_TIMER:
        stick_floortom_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(FLOORTOM_TIMER, 0)

      elif event.type == RIDE_TIMER:
        stick_ride_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(RIDE_TIMER, 0)

      elif event.type == CRASH_R_TIMER:
        stick_crash_r_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(CRASH_R_TIMER, 0)

      elif event.type == KICKDRUM_TIMER:
        kickdrum_visible = False
        screen.blit(background_drums, (0, 0))
        pygame.time.set_timer(KICKDRUM_TIMER, 0)

      if event.type == STICK_NEUTRAL_TIMER:
        sticks_neutral_visible = True
        screen.blit(sticks_neutral, (0, 0))
        pygame.time.set_timer(STICK_NEUTRAL_TIMER, 0)
      
    if not game_active:
      # Blit background + blur
      screen.blit(background_drums, (0, 0))
      overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGTH))
      overlay.set_alpha(100)
      overlay.fill((255, 255, 255))
      screen.blit(overlay, (0, 0))

      # Blit instructions
      game_title_rect = game_title.get_rect(center= (SCREEN_WIDTH / 2, 40))
      screen.blit(game_title, game_title_rect)
      
      instr1_rect = instruction1.get_rect(center= (SCREEN_WIDTH / 2, 70))
      screen.blit(instruction1, instr1_rect)
      instr2_rect = instruction2.get_rect(center= (SCREEN_WIDTH / 2, 90))
      screen.blit(instruction2, instr2_rect)
      instr3_rect = instruction3.get_rect(center= (SCREEN_WIDTH / 2, 110))
      screen.blit(instruction3, instr3_rect)
      instr4_rect = instruction4.get_rect(center= (SCREEN_WIDTH / 2, 130))
      screen.blit(instruction4, instr4_rect)
      instr5_rect = instruction5.get_rect(center= (SCREEN_WIDTH / 2, 150))
      screen.blit(instruction5, instr5_rect)
      instr6_rect = instruction6.get_rect(center= (SCREEN_WIDTH / 2, 170))
      screen.blit(instruction6, instr6_rect)
      instr7_rect = instruction7.get_rect(center= (SCREEN_WIDTH / 2, 190))
      screen.blit(instruction7, instr7_rect)
     
      if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        game_active = True

  pygame.display.update()
  clock.tick(60)

pygame.quit()