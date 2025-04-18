import pygame

class Araba:
    def __init__(self, x, y, renk, kontroller, resim_yolu):
        self.x = x
        self.y = y
        self.renk = renk
        self.kontroller = kontroller
        self.hiz = 5
        self.genislik = 50
        self.yukseklik = 80
        self.gorsel = pygame.image.load(resim_yolu)
        self.gorsel = pygame.transform.scale(self.gorsel, (self.genislik, self.yukseklik))

    def hareketEt(self, keys, ekran_genislik, ekran_yukseklik):
        eski_x = self.x
        eski_y = self.y

        if self.kontroller[0] == "W":
            if keys[pygame.K_w]:
                self.y -= self.hiz
            if keys[pygame.K_s]:
                self.y += self.hiz
            if keys[pygame.K_a]:
                self.x -= self.hiz
            if keys[pygame.K_d]:
                self.x += self.hiz
        elif self.kontroller[0] == "UP":
            if keys[pygame.K_UP]:
                self.y -= self.hiz
            if keys[pygame.K_DOWN]:
                self.y += self.hiz
            if keys[pygame.K_LEFT]:
                self.x -= self.hiz
            if keys[pygame.K_RIGHT]:
                self.x += self.hiz

        # Ekran dışına çıkmasını engelle
        self.x = max(0, min(self.x, ekran_genislik - self.genislik))
        self.y = max(0, min(self.y, ekran_yukseklik - self.yukseklik))

        # 🚫 Yeşil alana çıkmasını engelle: yol 200 ≤ x ≤ 600 arası
        if self.x < 200:
            self.x = 200
        if self.x + self.genislik > 600:
            self.x = 600 - self.genislik

    def ciz(self, ekran):
        ekran.blit(self.gorsel, (self.x, self.y))
