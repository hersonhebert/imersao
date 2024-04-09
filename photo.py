import pygame
import pygame.camera

def take_photo(cam):
    print("Tirando uma foto:")
    image = cam.get_image()

    filename = "photo_selfie.jpg"
    print(f"Salvando em {filename}")

    pygame.image.save(image, filename)
    return True  # Indica que a foto foi tirada

def main():
    pygame.init()
    pygame.camera.init()

    screen_width = 700
    screen_height = 500

    # Inicializando a câmera com o caminho da instância do dispositivo
    cam = pygame.camera.Camera("Integrated Webcam", (640, 480))
    cam.start()

    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Interface da Webcam")

    clock = pygame.time.Clock()

    background_color = (230, 230, 230)  # Cor de fundo mais clara

    font_path = "CascadiaCode-SemiBold.otf"  # Substitua pelo caminho real do arquivo TTF
    font_size = 20

    font = pygame.font.Font(font_path, font_size)

    taking_photo = False  # Variável de controle para indicar se uma foto está sendo tirada

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not taking_photo:  # Apenas tirar foto se não estiver tirando uma foto atualmente
                taking_photo = take_photo(cam)

        screen.fill(background_color)

        # Obtendo a imagem da câmera
        image = cam.get_image()

        # Calculando as coordenadas x e y para centralizar a imagem
        image_x = (screen_width - image.get_width()) // 2
        image_y = (screen_height - image.get_height()) // 2

        # Desenhando a imagem centralizada na tela
        screen.blit(image, (image_x, 40))

        # Renderizar o texto usando a fonte carregada
        text = font.render("PRESSIONE O BOTÃO DO MOUSE PARA TIRAR UMA FOTO", True, (0, 0, 0))  # Cor do texto: preto

        # Desenhar o texto na tela
        text_x = (screen_width - text.get_width()) // 2
        text_y = 10
        screen.blit(text, (text_x, text_y))

        pygame.display.flip()
        clock.tick(30)

        if taking_photo:  # Se uma foto foi tirada, feche a janela
            running = False

    cam.stop()
    pygame.quit()

if __name__ == "__main__":
    main()
