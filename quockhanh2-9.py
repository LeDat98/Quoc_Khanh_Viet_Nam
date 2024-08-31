import pygame
import math
import numpy as np
import os
import random

pygame.init()
pygame.mixer.init()

def draw_star(surface, color, x, y, size):
    points = []
    for i in range(10):
        angle = math.pi * 2 * i / 10 - math.pi / 2
        dist = size if i % 2 == 0 else size * 0.382
        points.append((x + math.cos(angle) * dist, y + math.sin(angle) * dist))
    pygame.draw.polygon(surface, color, points)

def create_gradient(color1, color2, height):
    gradient = []
    for i in range(height):
        ratio = i / height
        r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
        g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
        b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
        gradient.append((r, g, b))
    return gradient

# Thiết lập cửa sổ
width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chào Mừng Ngày Quốc Khánh 2/9")

# Màu sắc
RED = (218, 37, 29)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Tính toán kích thước cờ
a = min(width * 0.4, height * 0.8)
flag_width = a
flag_height = 2 * a / 3
star_size = (a / 5) * 2

# Tham số lá cờ
wave_length = 200
wave_amplitude = 20
num_points_x = 40
num_points_y = 30

# Tải và xử lý hình ảnh bản đồ Việt Nam
map_image = pygame.image.load("images/vietnam_map_vector.png")
map_image = pygame.transform.scale(map_image, (int(width * 0.4), int(height * 0.8)))


# Tạo gradient cho nền
sky_gradient = create_gradient((0, 0, 50), (50, 0, 0), height)

# Chuẩn bị font chữ
font_path = "font/Arial_Unicode_MS.TTF"
if not os.path.exists(font_path):
    print(f"Không tìm thấy file font: {font_path}")
    print("Vui lòng đặt file font vào cùng thư mục với script hoặc cung cấp đường dẫn chính xác.")
    pygame.quit()
    exit()

font = pygame.font.Font(font_path, 79)# kỷ niêm quốc khánh lần 79
text = font.render("Chào Mừng Ngày Quốc Khánh 2/9", True, YELLOW)
text_rect = text.get_rect(center=(width // 2, height - 80))

# Tải nhạc nền
music_path = "voice/audio.mp3"  
if not os.path.exists(music_path):
    print(f"Không tìm thấy file nhạc: {music_path}")
    print("Vui lòng đặt file nhạc vào thư mục music hoặc cung cấp đường dẫn chính xác.")
    pygame.quit()
    exit()

pygame.mixer.music.load(music_path)
pygame.mixer.music.play(-1)

class Firework:
    def __init__(self):
        self.x = random.randint(0, width)
        self.y = height
        self.color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
        self.speed = random.randint(5, 8)
        self.size = random.randint(2, 4)
        self.exploded = False
        self.particles = []
        self.max_height = random.randint(100, height // 2)
        self.trail = []

    def move(self):
        if not self.exploded:
            self.y -= self.speed
            self.trail.append((self.x, self.y))
            if len(self.trail) > 20:
                self.trail.pop(0)
            if self.y <= self.max_height:
                self.explode()

    def explode(self):
        self.exploded = True
        for _ in range(150):
            particle = Particle(self.x, self.y, self.color)
            self.particles.append(particle)

    def draw(self, surface):
        if not self.exploded:
            for i, (x, y) in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)))
                pygame.draw.circle(surface, (*self.color, alpha), (int(x), int(y)), self.size)
        else:
            for particle in self.particles:
                particle.move()
                particle.draw(surface)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(1, 3)
        self.speed = random.uniform(1, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.gravity = 0.1
        self.life = 255

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed + self.gravity
        self.speed *= 0.95
        self.gravity += 0.05
        self.size *= 0.97
        self.life -= 3

    def draw(self, surface):
        if self.life > 0:
            pygame.draw.circle(surface, (*self.color, self.life), (int(self.x), int(self.y)), int(self.size))

fireworks = []

running = True
clock = pygame.time.Clock()
t = 0
wind_strength = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Kiểm tra xem nhạc đã kết thúc chưa và phát lại nếu cần
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play()
        
    # Vẽ nền gradient
    for y, color in enumerate(sky_gradient):
        pygame.draw.line(screen, color, (0, y), (width, y))

    # Tạo lưới điểm cho lá cờ với hiệu ứng gió
    points = np.zeros((num_points_y, num_points_x, 2))
    for i in range(num_points_y):
        for j in range(num_points_x):
            x = j * flag_width / (num_points_x - 1)
            y = i * flag_height / (num_points_y - 1)
            wind_effect = math.sin(t * 2 + x / 50) * wind_strength * (j / num_points_x)
            z = math.sin(x / wave_length + t) * wave_amplitude + wind_effect
            points[i, j] = [width / 4 - flag_width / 2 + x, height / 2 - flag_height / 2 + y + z]

    # Vẽ lá cờ với hiệu ứng ánh sáng động
    for i in range(num_points_y - 1):
        for j in range(num_points_x - 1):
            color_intensity = int(255 * (0.7 + 0.3 * math.sin(points[i, j][0] / 20 + t)))
            flag_color = (min(255, color_intensity), 0, 0)
            pygame.draw.polygon(screen, flag_color, [
                points[i, j],
                points[i, j+1],
                points[i+1, j+1],
                points[i+1, j]
            ])

    # Tính toán vị trí của ngôi sao
    star_x = width / 4
    center_x = num_points_x // 2
    center_y = num_points_y // 2
    star_y = points[center_y, center_x][1]

    # Vẽ ngôi sao với kích thước cố định
    draw_star(screen, YELLOW, star_x, star_y, star_size / 2)

    # Vẽ bản đồ Việt Nam 
    screen.blit(map_image, (width * 0.6, height * 0.1))

    # Vẽ pháo hoa
    if random.random() < 0.05:
        fireworks.append(Firework())
    
    for firework in fireworks[:]:
        firework.move()
        firework.draw(screen)
        if firework.exploded and all(p.life <= 0 for p in firework.particles):
            fireworks.remove(firework)

    # Vẽ một số ngôi sao nhỏ trên nền
    for _ in range(20):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        size = np.random.randint(1, 3)
        brightness = int(128 + 127 * math.sin(t * 5 + x * y))
        pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), size)

    # Vẽ dòng chữ chào mừng
    screen.blit(text, text_rect)

    pygame.display.flip()
    t += 0.05
    wind_strength = 2 + math.sin(t / 5) * 1.5
    clock.tick(60)

pygame.quit()