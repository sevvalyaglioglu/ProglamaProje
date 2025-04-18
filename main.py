import pygame
import sys
from araba import Araba
from engel import Engel

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Yol Scroll + Oyuncu Hareketi Yarışı")

clock = pygame.time.Clock()

# Scroll offset - ekranın yukarıya ne kadar kaydığını tutar
scroll_offset = 0
scroll_hizi = 2  # yolun kendi kendine akış hızı

# Bitiş çizgisi ekranın dışında başlar
bitis_y_global = -1000

# Engeller (global koordinatlarda tanımlanır)
engeller = [
    Engel(290, 400),
    Engel(350, 200),
    Engel(410, -200)
]

# Arabalar başlangıçta aşağıdadır
araba1 = Araba(280, 500, (255, 0, 0), ["W", "S", "A", "D"], "Assets/araba1.png")
araba2 = Araba(400, 500, (0, 0, 255), ["UP", "DOWN", "LEFT", "RIGHT"], "Assets/araba2.png")

kazanan = None

def uzun_duz_yol_ciz(screen, scroll_offset):
    pygame.draw.rect(screen, (50, 50, 50), (200, -scroll_offset, 400, HEIGHT + scroll_offset + 1000))

    # Şerit çizgileri
    pygame.draw.line(screen, (255, 255, 255), (300, 0), (300, HEIGHT), 4)
    pygame.draw.line(screen, (255, 255, 255), (500, 0), (500, HEIGHT), 4)

    # Orta kesikli çizgi
    for y in range(-scroll_offset % 40, HEIGHT, 40):
        pygame.draw.line(screen, (255, 255, 255), (400, y), (400, y + 20), 4)

def bitis_cizgisi_satrancli(screen, y_pos):
    kare_w, kare_h = 40, 40
    renkler = [(255, 255, 255), (0, 0, 0)]
    for x in range(0, WIDTH, kare_w):
        for y in range(y_pos, y_pos + kare_h * 2, kare_h):
            renk = renkler[((x // kare_w) + (y // kare_h)) % 2]
            pygame.draw.rect(screen, renk, (x, y, kare_w, kare_h))

# Ana oyun döngüsü
running = True
while running:
    screen.fill((0, 150, 0))  # Çimen

    # Scroll'u artır
    scroll_offset += scroll_hizi

    # Yolu çiz
    uzun_duz_yol_ciz(screen, scroll_offset)

    # Bitiş çizgisi
    bitis_y_ekranda = bitis_y_global + scroll_offset
    if 0 <= bitis_y_ekranda <= HEIGHT:
        bitis_cizgisi_satrancli(screen, bitis_y_ekranda)

    # Engelleri çiz
    for engel in engeller:
        engel_screen_y = engel.y + scroll_offset
        engel_rect = pygame.Rect(engel.x, engel_screen_y, engel.genislik, engel.yukseklik)
        pygame.draw.rect(screen, engel.renk, engel_rect)

        # Çarpışma kontrolü
        if engel.carpti_mi(araba1, scroll_offset):
            font = pygame.font.SysFont(None, 60)
            text = font.render("Oyuncu 1 Kaza Yaptı!", True, (255, 0, 0))
            screen.blit(text, (200, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()
        if engel.carpti_mi(araba2, scroll_offset):
            font = pygame.font.SysFont(None, 60)
            text = font.render("Oyuncu 2 Kaza Yaptı!", True, (255, 0, 0))
            screen.blit(text, (200, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

    # Olaylar
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    araba1.hareketEt(keys, WIDTH, HEIGHT)
    araba2.hareketEt(keys, WIDTH, HEIGHT)

    araba1.ciz(screen)
    araba2.ciz(screen)

    # Kazanan kontrolü (ekrandaki y ile)
    if araba1.y <= bitis_y_ekranda and kazanan is None:
        kazanan = "Oyuncu 1"
    if araba2.y <= bitis_y_ekranda and kazanan is None:
        kazanan = "Oyuncu 2"

    if kazanan:
        font = pygame.font.SysFont(None, 60)
        text = font.render(f"{kazanan} Kazandı!", True, (0, 0, 0))
        screen.blit(text, (200, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(3000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
