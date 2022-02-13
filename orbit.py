import pygame, datetime
from pygame import image, transform

class Planet(pygame.sprite.Sprite):
    def __init__(self, pos, name, offset, velocity, angle, *groups):
        super().__init__(*groups)
        self.image = transform.scale(image.load(f"{name}.png"), (30, 30))
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.offset = pygame.math.Vector2(offset, 0)
        self.angle = angle
        self.velocity = velocity

    def update(self):
        self.angle += self.velocity * velocity_multipler
        self.rect.center = self.pos + self.offset.rotate(-self.angle)

# main loop
pygame.init()
screen = pygame.display.set_mode((850, 850))
screen_rect = screen.get_rect()
clock = pygame.time.Clock()
sprites = pygame.sprite.Group()

# load planets
background = pygame.transform.scale(pygame.image.load("background.png"), (1000, 1000)) # load background
au_units = 149_597_870.7
planet_names = {
    #           length of year      # degrees
    "Mercury" : [365 / 88,          360 - 240],
    "Venus" :   [365 / 224.7,       360 - 0],
    "Earth" :   [365 / 365.2564,    360 - 80],
    "Mars" :    [365 / 687,         360 - 80],
    "Jupiter" : [365 / 4332.59,     360 - 250],
    "Saturn" :  [365 / 10759,       360 - 20],
    "Uranus" :  [365 / 30688.5,     360 - 190],
    "Neptune" : [365 / 60182,       360 - 230]
}
sun = pygame.transform.scale(pygame.image.load("sun.png"), (50, 50)) # load sun
planets = [Planet(screen_rect.center, value[0], (i*50)+50, value[1][0], value[1][1], sprites) 
            for i,value in enumerate(planet_names.items())]

velocity_multipler = 0
refrence_point = datetime.datetime(2007, 12, 28)
txt1 = pygame.font.SysFont("Arial", 20).render("-speed", True, (0, 20, 52))
txt2 = pygame.font.SysFont("Arial", 20).render("+speed", True, (0, 20, 52))
text = ""
years = 0
fast_forward = False
target_angle = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if 25 <= mouse[0] <= 105 and 800 <= mouse[1] <= 825:
                velocity_multipler = max(0, velocity_multipler - 0.1)
            elif 125 <= mouse[0] <= 208 and 800 <= mouse[1] <= 825:
                velocity_multipler = max(0, velocity_multipler + 0.1)
        
        elif event.type == pygame.KEYDOWN:
            if fast_forward == False:
                if "\r" in text:
                    fast_forward = True
                    years = int(text.replace("\r",""))
                    velocity_multipler = 10
                    target_angle = planets[2].angle + (360 * years)
                    text = ""

                elif text != "" and text.isdigit() == False: text = ""
                elif event.key == pygame.K_BACKSLASH: text = text[:-1]
                else: text += event.unicode
    
    sprites.update()
    screen.fill((30, 30, 30))
    screen.blit(background, background.get_rect()) # add background image
    screen.blit(sun, (400, 400)) # add sun

    # draw orbital paths
    for i in range(50, 9 * 50, 50):
        pygame.draw.circle(screen, (0, 191, 255), screen_rect.center, i, width=1)

    sprites.draw(screen) # draw planets

    # draw buttons
    mouse = pygame.mouse.get_pos()
    pygame.draw.rect(screen, (112, 166, 200), (25, 800, 80, 25))
    pygame.draw.rect(screen, (112, 166, 255), (125, 800, 80, 25))
    screen.blit(txt1, (38, 800))
    screen.blit(txt2, (138, 800))

    # fast forward
    if fast_forward:
        if planets[2].angle >= (target_angle - velocity_multipler):
            fast_forward = False
            velocity_multipler = 0.01
            target_angle = 0
    
    # current date
    current_date = refrence_point + datetime.timedelta(days = ((planets[2].angle - 280) / 360) * 365)
    date_text = pygame.font.SysFont("Arial Black", 30).render(current_date.strftime("%d %B %Y %H:%M").ljust(25), True, (0, 161, 35))
    screen.blit(date_text, (240, 5))

    pygame.display.flip()
    clock.tick(60)

