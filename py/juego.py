import pygame
import random

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Juego de Reciclaje')

# Colores
white = (255, 255, 255)
black = (0, 0, 0)

# Configuración de las canecas
bin_width = 150
bin_height = 200

# Cargar imágenes locales de las canecas
bin_images = {
    'organico': pygame.image.load('bin_organico.png'),
    'reciclable': pygame.image.load('bin_reciclacle.png'),
    'no_reciclable': pygame.image.load('bin_noreciclable.png')
}

# Redimensionar imágenes de las canecas
bin_images = {key: pygame.transform.scale(img, (bin_width, bin_height)) for key, img in bin_images.items()}

# Cargar imágenes locales de residuos
waste_images = {
    'papel': pygame.image.load('waste_papel.png'),
    'vidrio': pygame.image.load('waste_vidrio.png'),
    'plastico': pygame.image.load('waste_plastico.png')
}

# Redimensionar imágenes de residuos
waste_images = {key: pygame.transform.scale(img, (50, 50)) for key, img in waste_images.items()}

# Residuos en juego
waste_size = 50
waste_types = ['papel', 'vidrio', 'plastico']
waste = pygame.Rect(random.randint(0, screen_width-waste_size), random.randint(0, screen_height-waste_size), waste_size, waste_size)
current_waste = random.choice(waste_types)

# Fuente
font = pygame.font.SysFont(None, 35)

# Intentos
max_attempts = 3
attempts = max_attempts

# Configuración de las canecas
bins = {
    'organico': pygame.Rect(50, 100, bin_width, bin_height),
    'reciclable': pygame.Rect(300, 100, bin_width, bin_height),
    'no_reciclable': pygame.Rect(550, 100, bin_width, bin_height)
}

def draw_bins():
    for waste_type, rect in bins.items():
        screen.blit(bin_images[waste_type], rect.topleft)

def draw_waste():
    screen.blit(waste_images[current_waste], (waste.x, waste.y))

def draw_attempts():
    attempt_text = font.render(f'Intentos restantes: {attempts}', True, black)
    screen.blit(attempt_text, (10, 10))

def main():
    global attempts, waste, current_waste
    clock = pygame.time.Clock()
    running = True
    dragging = False

    while running:
        screen.fill(white)
        draw_bins()
        draw_waste()
        draw_attempts()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if waste.collidepoint(event.pos):
                    dragging = True
                    offset_x = waste.x - event.pos[0]
                    offset_y = waste.y - event.pos[1]
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    correct = False
                    if bins['organico'].colliderect(waste) and current_waste == 'papel':
                        correct = True
                    elif bins['reciclable'].colliderect(waste) and current_waste in ['vidrio', 'plastico']:
                        correct = True
                    elif bins['no_reciclable'].colliderect(waste) and current_waste == 'no_reciclable':
                        correct = True
                    
                    if correct:
                        print("¡Correcto!")
                        waste.x = random.randint(0, screen_width-waste_size)
                        waste.y = random.randint(0, screen_height-waste_size)
                        current_waste = random.choice(waste_types)
                        attempts = max_attempts  # Reiniciar intentos
                    else:
                        attempts -= 1
                        if attempts <= 0:
                            print("¡Juego terminado! Has agotado todos los intentos.")
                            running = False
                        else:
                            print(f"Intento fallido. Quedan {attempts} intentos.")
                    # Reubicar el residuo en una posición aleatoria si se equivocó
                    waste.x = random.randint(0, screen_width-waste_size)
                    waste.y = random.randint(0, screen_height-waste_size)
            elif event.type == pygame.MOUSEMOTION and dragging:
                waste.x = event.pos[0] + offset_x
                waste.y = event.pos[1] + offset_y

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
