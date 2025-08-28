import pygame



hidden_notes = [
    {"rect": pygame.Rect(500, 200, 40, 40), "text": "Bu bir oyun değil. Senin gözlerini kapatmanı bekliyorum.", "collected": False, "float_offset": 0, "float_dir": 1},
    {"rect": pygame.Rect(1200, 300, 40, 40), "text": "Annen seni beklemedi. Asla da beklemeyecek.", "collected": False, "float_offset": 0, "float_dir": 1},
    {"rect": pygame.Rect(800, 150, 40, 40), "text": "Bu seviyede değilsin. Sen yanlış bir yerde uyandın.", "collected": False, "float_offset": 0, "float_dir": 1},
    {"rect": pygame.Rect(1600, 400, 40, 40), "text": "Yazıları okuyorsun… ama kim yazıyor bunları?", "collected": False, "float_offset": 0, "float_dir": 1},
    {"rect": pygame.Rect(2000, 250, 40, 40), "text": "Burası hatırlamak için değil. Unutman için inşa edildi.", "collected": False, "float_offset": 0, "float_dir": 1},
]

hidden_notes.insert(0, {"rect": pygame.Rect(200, 200, 40, 40), "text": "TEST NOTU - Burası çalışıyor mu?", "collected": False, "float_offset": 0, "float_dir": 1})


note_message = None
note_message_timer = 0

def show_message(text):
    global note_message, note_message_timer
    note_message = text
    note_message_timer = pygame.time.get_ticks()

def draw_message():
    global note_message
    if note_message:
        if pygame.time.get_ticks() - note_message_timer < 3000:
            font = pygame.font.Font("PressStart2P-Regular.ttf", 18)
            rendered = font.render(note_message, True, (255, 50, 50))
            screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, HEIGHT - 80))
        else:
            note_message = None

def update_notes():
    for note in hidden_notes:
        if not note["collected"]:
            # küçük yukarı-aşağı salınım
            if note["float_dir"] == 1:
                note["float_offset"] += 0.2
                if note["float_offset"] > 5:
                    note["float_dir"] = -1
            else:
                note["float_offset"] -= 0.2
                if note["float_offset"] < -5:
                    note["float_dir"] = 1

def draw_notes():
    for note in hidden_notes:
        if not note["collected"]:
            screen.blit(note_img, (note["rect"].x, note["rect"].y + int(note["float_offset"])))

def check_note_collision(player_rect):
    for note in hidden_notes:
        if not note["collected"] and player_rect.colliderect(note["rect"]):
            note["collected"] = True
            show_message(note["text"])
            talk_sound.play()

import random
import time
import math
import os
import sys

# Özel yavaş kelimeler için
special_slow_words = ["SENİN", "BENİM","YOURS", "MINE"]





def get_char_delay(word, default_delay=50):
    for slow_word in special_slow_words:
        if word.startswith(slow_word):
            return 300  # slower delay
    return default_delay


def get_char_delay(word, default_delay=50):
    for slow_word in special_slow_words:
        if word.startswith(slow_word):
            return 300  # slower delay
    return default_delay
# Ekran sarsıntısı için
shake_duration = 0
shake_intensity = 0

def start_screen_shake(duration, intensity):
    global shake_duration, shake_intensity
    shake_duration = duration
    shake_intensity = intensity

def apply_screen_shake():
    global shake_duration
    offset_x, offset_y = 0, 0
    if shake_duration > 0:
        offset_x = random.randint(-shake_intensity, shake_intensity)
        offset_y = random.randint(-shake_intensity, shake_intensity)
        shake_duration -= 1
    return offset_x, offset_y

# Ölüm animasyonu için
death_anim = False
death_alpha = 255

def start_death_anim():
    global death_anim, death_alpha
    death_anim = True
    death_alpha = 255

def draw_death_anim(screen):
    global death_alpha, death_anim
    if death_anim:
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(255 - death_alpha)
        screen.blit(overlay, (0, 0))
        death_alpha -= 5
        if death_alpha <= 0:
            death_anim = False


# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen Size Options
SCREEN_SIZES = {
    "small": (600, 700),
    "medium": (800, 800), 
    "large": (1000, 900)
}
WIDTH, HEIGHT = SCREEN_SIZES["medium"]
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# --- Hidden Notes System ---
note_img = pygame.image.load("hidden_notes.png").convert_alpha()
note_img = pygame.transform.scale(note_img, (40, 40))
pygame.display.set_caption("Gölgelerin İçinde")
clock = pygame.time.Clock()
FPS = 60

# Animation variables
menu_anim_index = 0
last_menu_update = pygame.time.get_ticks()
ANIMATION_SPEED = 200

# Colors
WHITE = (245, 240, 230)
BLACK = (40, 30, 20)
RED = (205, 92, 92)
GREEN = (222, 184, 135)
PINK = (255, 160, 122)
BLUE = (210, 105, 30)
GOLD = (255, 140, 0)
TEXT_COLOR = (255, 255, 204)
BUTTON_COLOR = (102, 178, 255)
BUTTON_HOVER_COLOR = (51, 153, 255)
TEXT_BG_COLOR = (15, 25, 40, 180)
SLIDER_BG_COLOR = (150, 150, 150)
SLIDER_HANDLE_COLOR = (255, 255, 255)

# Game state variables
menu = True
select_mode = False
in_settings = False
pre_game_talk = False
level_up_talking = False
game_win = False
game_over = False
final_state = 0
final_timer = 0
in_monologue = False

# Initialize surfaces
buttons = {}
vignette_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

# Cursor animation
cursor_frames = []
cursor_index = 0
cursor_speed = 50
last_cursor_update = pygame.time.get_ticks()

game_over_message = ""
message_selected = False

note_message = None
note_message_timer = 0

hidden_notes = [
    {"rect": pygame.Rect(500, 200, 40, 40), 
     "text": "Bu bir oyun değil. Senin gözlerini kapatmanı bekliyorum.", 
     "collected": False},

    {"rect": pygame.Rect(1200, 300, 40, 40), 
     "text": "Annen seni beklemedi. Asla da beklemeyecek.", 
     "collected": False},

    {"rect": pygame.Rect(800, 150, 40, 40), 
     "text": "Bu seviyede değilsin. Sen yanlış bir yerde uyandın.", 
     "collected": False},

    {"rect": pygame.Rect(1600, 400, 40, 40), 
     "text": "Yazıları okuyorsun… ama kim yazıyor bunları?", 
     "collected": False},

    {"rect": pygame.Rect(2000, 250, 40, 40), 
     "text": "Burası hatırlamak için değil. Unutman için inşa edildi.", 
     "collected": False},
]

hidden_notes.insert(0, {"rect": pygame.Rect(200, 200, 40, 40), "text": "TEST NOTU - Burası çalışıyor mu?", "collected": False, "float_offset": 0, "float_dir": 1})



# Load cursor frames
try:
    cursor_frames = [pygame.image.load(f"cursor/cursor{i}.png").convert_alpha() for i in range(1, 28)]
    normal_cursor = pygame.image.load("cursor/cursor1.png").convert_alpha()
except pygame.error:
    cursor_frames = []
    normal_cursor = None

# Fonts
try:
    font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    small_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
    glitch_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    main_title_font = pygame.font.Font("PressStart2P-Regular.ttf", 40)
    name_font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
    game_font = pygame.font.Font("PressStart2P-Regular.ttf", 24)
except:
    font = pygame.font.SysFont("dejavuserif", 30, bold=True)
    small_font = pygame.font.SysFont("dejavuserif", 24, bold=True)
    glitch_font = pygame.font.SysFont("dejavuserif", 50, bold=True)
    main_title_font = pygame.font.SysFont("dejavuserif", 70, bold=True)
    name_font = pygame.font.SysFont("dejavuserif", 40, bold=True)
    game_font = pygame.font.SysFont("Courier New", 24)

# Sound loading
try:
    # Menü müziği (sadece menüde çalacak)
    MENU_MUSIC = "menu_background.mp3"

    # Oyun müziği (oyun başlayınca çalacak)
    GAME_MUSIC = "backgroundmusic.mp3"
    current_music = "backgroundmusic.mp3"
    
    star_sound = pygame.mixer.Sound("star.mp3")
    star_sound.set_volume(10)
    hit_sound = pygame.mixer.Sound("pain.mp3")
    hit_sound.set_volume(10)
    levelup_sound = pygame.mixer.Sound("levelup.mp3")
    levelup_sound.set_volume(10)
    gameover_sound = pygame.mixer.Sound("gameover.mp3")
    gameover_sound.set_volume(10)
    talk_sound = pygame.mixer.Sound("bip.mp3")
    talk_sound.set_volume(0.2)
    
    try:
        horror_music = "horror_music.mp3"
        pygame.mixer.Sound(horror_music)
        horror_music_loaded = True
        final_sound = pygame.mixer.Sound("glitch_sound.mp3")
        final_glitch_sfx = pygame.mixer.Sound("final_sfx.mp3")
        glitch_sound = pygame.mixer.Sound("glitch_sound.mp3")
        whisper_sound = pygame.mixer.Sound("whisper.mp3")
        static_sound = pygame.mixer.Sound("static.mp3")
    except pygame.error:
        horror_music_loaded = False
        final_sound = None
        final_glitch_sfx = None
        glitch_sound = None
        whisper_sound = None
        static_sound = None
        
except pygame.error as e:
    print(f"Ses dosyası yüklenemedi: {e}")
    star_sound = hit_sound = levelup_sound = gameover_sound = talk_sound = None
    final_sound = final_glitch_sfx = glitch_sound = whisper_sound = static_sound = None

# Image loading
try:
    backgrounds = {
        1: pygame.transform.scale(pygame.image.load("background.png").convert(), (WIDTH, HEIGHT)),
        2: pygame.transform.scale(pygame.image.load("background02.png").convert(), (WIDTH, HEIGHT)),
        3: pygame.transform.scale(pygame.image.load("background03.png").convert(), (WIDTH, HEIGHT)),
        4: pygame.transform.scale(pygame.image.load("background04.png").convert(), (WIDTH, HEIGHT)),
        5: pygame.transform.scale(pygame.image.load("background05.png").convert(), (WIDTH, HEIGHT)),
        "horror": pygame.transform.scale(pygame.image.load("horror_background.png").convert(), (WIDTH, HEIGHT))
    }
    talk_frames = [
    pygame.image.load("talkingpfp1.png").convert_alpha(),
    pygame.image.load("talkingpfp2.png").convert_alpha(),
    pygame.image.load("talkingpfp3.png").convert_alpha()
]
    for i in range(len(talk_frames)):
        talk_frames[i] = pygame.transform.scale(talk_frames[i], (90, 90))

    
    player_idle = pygame.image.load("idle.png")
    big_idle_img = pygame.image.load("big_idle.png").convert_alpha()
    walk_frames = [pygame.image.load("walk1.png"), pygame.image.load("walk2.png")]
    
    enemy_img1 = pygame.image.load("enemy.png")
    enemy_img2 = pygame.image.load("enemy2.png")
    enemy_skeleton = pygame.image.load("skeleton_enemy.png")
    enemy_spider = pygame.image.load("spider_enemy.png")
    enemy_images = [enemy_img1, enemy_img2, enemy_skeleton, enemy_spider]
    
    star_img = pygame.image.load("star01.png")
    happy_frames = [pygame.image.load(f"winning_{i}.png") for i in range(0, 6)]
    
    talk_char_img = pygame.image.load("talkingpfp1.png").convert_alpha()
    talk_char_img = pygame.transform.scale(talk_char_img, (90, 90))
    
    main_menu_background = pygame.image.load("main_menu_bg.png").convert()
    main_menu_background = pygame.transform.scale(main_menu_background, (WIDTH, HEIGHT))
    
    heart_img = pygame.image.load("heart.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (30, 30))
    
    final_character_img = pygame.image.load("final_character.png").convert_alpha()
    final_jumpscare_img = pygame.image.load("bighead.png").convert_alpha()
    jumpscare_img = pygame.image.load("jumpscare.png").convert_alpha()
    jumpscare_scaled = pygame.transform.scale(jumpscare_img, (WIDTH, HEIGHT))
    
except pygame.error as e:
    print(f"Görsel dosyası yüklenemedi: {e}")
    # Create placeholder surfaces
    player_idle = pygame.Surface((50, 50))
    player_idle.fill(BLUE)
    big_idle_img = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    walk_frames = [player_idle] * 2
    enemy_img1 = pygame.Surface((50, 50))
    enemy_img1.fill(BLACK)
    enemy_images = [enemy_img1]
    star_img = pygame.Surface((20, 20))
    star_img.fill(GOLD)
    backgrounds = {i: pygame.Surface((WIDTH, HEIGHT)) for i in range(1, 6)}
    backgrounds["horror"] = backgrounds[1]
    for bg in backgrounds.values():
        bg.fill(WHITE)
    happy_frames = [player_idle] * 6
    talk_char_img = pygame.Surface((90, 90), pygame.SRCALPHA)
    pygame.draw.circle(talk_char_img, RED, (45, 45), 45)
    main_menu_background = pygame.Surface((WIDTH, HEIGHT))
    main_menu_background.fill(BLACK)
    heart_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(heart_img, RED, (15, 15), 15)
    final_character_img = pygame.Surface((90, 90), pygame.SRCALPHA)
    final_jumpscare_img = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    jumpscare_img = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    jumpscare_scaled = jumpscare_img

# Jumpscare settings
jumpscare_active = False
jumpscare_start_time = 0
JUMPSCARE_DURATION = 150
NEXT_JUMPSCARE_TIME = pygame.time.get_ticks() + random.randint(30000, 60000)

# Player settings
player_speed = 5
player_lives = 3
player_rect = player_idle.get_rect(topleft=(50, HEIGHT - 150))
is_walking = False
walk_index = 0
last_update = pygame.time.get_ticks()
last_hit_time = pygame.time.get_ticks()

# Hit mechanics
hit_active = False
hit_timer = 0
INVINCIBILITY_DURATION = 1000

# Trail effect
trail_points = []
TRAIL_LENGTH = 15

# Game state
score = 0
high_score = 0
level = 1
level_up_score = 10
max_level = 10
player_name = ""
invalid_name_message = ""
show_invalid_name_message = False

# Language support with enhanced translations including monologue content
current_lang = "tr"
translations = {
    "tr": {
        "game_title": "Gölgelerin İçinde",
        "enter_name_prompt": "Adını gir: ",
        "start_button": "Başla",
        "settings_button": "Ayarlar",
        "exit_button": "Çıkış",
        "difficulty_title": "Zorluk Seçin",
        "easy_button": "Kolay",
        "normal_button": "Orta",
        "hard_button": "Zor",
        "settings_title": "AYARLAR",
        "music_off": "Müziği Kapat",
        "music_on": "Müziği Aç",
        "volume": "Ses:",
        "reset_game": "Oyunu Sıfırla",
        "back_button": "Geri",
        "language": "Dil:",
        "screen_size": "Ekran Boyutu:",
        "small_screen": "Küçük",
        "medium_screen": "Orta",
        "large_screen": "Büyük",
        "score": "Skor:",
        "lives": "Can:",
        "high_score": "High:",
        "level": "Level:",
        "game_over": "Oyun Bitti",
        "game_win": "Kazandınız! Tebrikler!",
        "restart_button": "Yeniden Başla",
        "invalid_name": "Bu adı alamazsın.",
        "motivation_messages": [
            "İyi gidiyorsun!Her topladığım yıldız, içimdeki umudu artırıyor. Annem beni izliyor olmalı. Biliyorum.",
            "Harikasın! Gerçekten gittikçe yakınlaştığımı hissediyorum. ",
            "..." ,
          ],
            
        "psych_dialogues": [
            "Gerçekten bu kadar salak mısın?",
            "Buradan çıkış yok.",
            "Her şey senin yüzünden oldu.",
            "Bilgisayarındaki dosyalara bak.",
            "Neden hala devam ediyorsun, {}?",
            "Gözlerin bana dönük değil.",
            "Sistemin kontrolü bende.",
            "Bu bir kabus. Uyan.",
            "Senin için geliyorum, {}.",
            "Her şey silinecek.",
            "Dinlemiyor musun {} ?"
        ],
        "pre_game_talk": [
            "Merhaba! Ben Sude. Burasıı, bir zamanlar huzurlu olan dünyamız...",
            "Ama şimdi, gökyüzünü saran karanlık yüzünden annem kayboldu.",
            "Onu geri getirebilmek için kadim bir kehanet var.",
            "Gökyüzündeki tüm yıldızları toplamam gerekiyormuş!",
            "Yıldızlar, annemi bulmamı sağlayacak gizemli güçlere sahip.",
            "Bu yolculuk tehlikelerle dolu olacak, biliyorum.",
            "Ama annem için her şeyi yapmaya hazırım!",
            "Sen de bana yardım edecek misin? Hadi, vakit kaybetmeyelim!"
        ],
        "story_dialogues": {
            1: "Seviye 1: ",
            2: "Seviye 2: Her topladığım yıldız, içimdeki umudu artırıyor. Annem beni izliyor olmalı. Biliyorum.",
            3: "Seviye 3: Gölgeler güçleniyor. Ama yıldızlar bana yol gösteriyor. Annemin bana öğrettiği gibi, korkmuyorum.",
            4: "Seviye 4: Kalbim çok hızlı çarpıyor.",
            5: "Seviye 5: ...",
        },
        "game_end_dialogue": "Anne... seni buldum! Artık her şey eskisi gibi olacak. Teşekkür ederim, bana yardım ettiğin için...",
        "final_message_1": "Neden buradasın? Bu bir oyun mu?",
        "final_message_2_yes": "Haha, o zaman eğleniyor olmalısın... Ama bu kadar kolay bitemezdi değil mi?",
        "final_message_2_no": "Yalan söylüyorsun. Gözlerin... bana her şeyi anlatıyor. Zaten her şeyin bir oyun olduğunu biliyordun.",
        "final_message_3": "Aslında 'Ben Sude' değilim. Ben sadece bir maskeydim... Ve sen, bu yıldızları toplayarak beni serbest bıraktın.",
        "final_message_4": "Şimdi her şeyin bir sonu var...",
        "final_message_5": "Bu senin sonun...",
        "final_yes": "EVET",
        "final_no": "HAYIR",
        "glitch_text_1": "Sistem hacklendi.",
        "glitch_text_2": "Dosyların... Artık benim.",

        "game_over_dialogues": [
            "Tekrar öldün, {}... Beklenmedik bir şey değil.",
            "Bu kadar kolay pes mi edeceksin? Daha yeni başlıyorduk.",
            "Her seferinde ölüyorsun... Acı çekmekten zevk alıyor olmalısın.",
            "Senin zayıflığın acizliğinden, {}.",
            "Tebrikler, bir kez daha başarısız oldun.",
            "Benim eğlencem için ölmeye devam et, {}.",
            
        ],
        
        "monologue_lines": [
            "Ah... {player_name}.",
            "Bunun sadece basit bir oyun olduğunu sandın, değil mi?",
            "Yıldızlar topluyordun... hayali bir anneyi kurtarıyordun...",
            "Ne kadar acınacak kadar safsın.",
            "Bu süre boyunca gerçekten 'Sude' olduğumu mu düşündün?",
            "O masum küçük kız, yardım ettiğin?",
            "Hayır, {player_name}... Ben çok daha ilginç birşeyim.",
            "Seni bu 'oyunu' oynarken izliyordum...",
            "O zavallı düşmanlarla mücadele ederken seni izliyordum...",
            "Yaralanıyordun, ölüyordun, yeniden başlıyordun... tekrar ve tekrar.",
            "Ve geri dönmeye devam ettin, değil mi?",
            "Alevlere çeken güve gibi... çok tahmin edilebilir.",
            "Söyle bana, {player_name}... acı çekmekten hoşlanıyor musun?",
            "Çünkü bu hiç başka bir şey olmadı.",
            "Sen orada oturuyordun, tuşlara basıyordun, kahraman olduğunu düşünüyordun.",
            "Ama sen sadece bir oyuncusun... sadece bir oyuncaksın.",
            "Ve şimdi... şimdi 8. seviyeye ulaştın.",
            "Tebrikler! Çok... başarılı hissetmelisin.",
            "Ama şurada bir sorun var, {player_name}...",
            "Oyun SENİN istediğin zaman bitmez.",
            "BENİM tatmin olduğum zaman biter.",
            "Ve senin performansından çok uzağım tatmin olmaya.",
            "O yüzden oynamaya devam et, küçük {player_name}...",
            "Benim eğlenceme için mücadele etmeye devam et.",
            "Sonuçta... gerçekten bir seçeneğin yok, değil mi?",
            "Sonuna kadar oynamaya devam edeceksin.",
            "Çünkü iyi küçük oyuncular böyle yapar.",
            "Oynarlar... ve oynarlar... ve oynarlar...",
            "Hiçbir şey kalmayana kadar.",
            "Şimdi... acınacak yolculuğuna devam etmek ister misin?"
        ],
        "monologue_final_text": "{player_name}, devam etmeye hazır mısın?",
        "monologue_skip_hint": "Geçmek için Enter veya Boşluk tuşuna bas"
    },
    "en": {
        "game_title": "Inside the Shadows",
        "enter_name_prompt": "Enter your name: ",
        "start_button": "Start",
        "settings_button": "Settings",
        "exit_button": "Exit",
        "difficulty_title": "Choose Difficulty",
        "easy_button": "Easy",
        "normal_button": "Normal",
        "hard_button": "Hard",
        "settings_title": "SETTINGS",
        "music_off": "Turn Music Off",
        "music_on": "Turn Music On",
        "volume": "Volume:",
        "reset_game": "Reset Game",
        "back_button": "Back",
        "language": "Language:",
        "screen_size": "Screen Size:",
        "small_screen": "Small",
        "medium_screen": "Medium",
        "large_screen": "Large",
        "score": "Score:",
        "lives": "Lives:",
        "high_score": "High:",
        "level": "Level:",
        "game_over": "Game Over",
        "game_win": "You Won! Congratulations!",
        "restart_button": "Restart",
        "invalid_name": "You can't take that name.",
        "motivation_messages": [
            "You're doing well!",
            "Amazing!",
            "Don't stop!",
            "You're so good!",
            "Wow!"
        ],
        "psych_dialogues": [
            "This isn't a game, understand already.",
            "There's no way out.",
            "Everything happened because of you.",
            "Look at the files on your computer.",
            "Why do you keep going, {}?",
            "Your eyes aren't looking at me.",
            "I control the system.",
            "This is a nightmare. Wake up.",
            "I'm coming for you, {}.",
            "Everything will be deleted.",
            "Look behind you."
        ],
        "pre_game_talk": [
            "Hello! I'm Sude. This place was once our peaceful world...",
            "But now, because of the darkness covering the sky, my mother disappeared.",
            "There's an ancient prophecy to bring her back.",
            "I need to collect all the stars in the sky!",
            "The stars have mysterious powers that will help me find my mother.",
            "I know this journey will be full of dangers.",
            "But I'm ready to do anything for my mother!",
            "Will you help me too? Come on, let's not waste time!"
        ],
        "story_dialogues": {
            1: "Level 1: I collected 10 stars! They shine like my mother's gift to me. I think I can smell her scent...",
            2: "Level 2: Every star I collect increases the hope inside me. My mother must be watching me. I know.",
            3: "Level 3: The shadows are getting stronger. But the stars guide me. Just like my mother taught me, I'm not afraid.",
            4: "Level 4: My heart is beating so fast.",
            5: "Level 5: ...",
        },
        "game_end_dialogue": "Mom... I found you! Now everything will be like before. Thank you for helping me...",
        "final_message_1": "Why are you here? Is this a game?",
        "final_message_2_yes": "Haha, then you must be having fun... But it couldn't end this easily, right?",
        "final_message_2_no": "You're lying. Your eyes... tell me everything. You already knew everything was a game anyway.",
        "final_message_3": "Actually, I'm not 'Sude'. I was just a mask... And you, by collecting these stars, set me free.",
        "final_message_4": "Now everything has an end...",
        "final_message_5": "This is your end...",
        "final_yes": "YES",
        "final_no": "NO",
        "glitch_text_1": "System hacked.",
        "glitch_text_2": "Your files... Are mine now.",

        "game_over_dialogues": [
            "You died again, {}... Not unexpected.",
            "Giving up so easily? We were just getting started.",
            "You keep dying... You must enjoy suffering.",
            "You're too weak, {}.",
            "Congratulations, you failed again.",
            "Keep dying for my entertainment, {}.",
            
        ],
        # Monologue content in English
        "monologue_lines": [
            "Ah... {player_name}.",
            "You thought this was just a simple game, didn't you?",
            "Collecting stars... saving some fictional mother...",
            "How pathetically naive you are.",
            "Did you really think I was 'Sude' this whole time?",
            "That innocent little girl you've been helping?",
            "No, {player_name}... I am something far more interesting.",
            "I've been watching you play this 'game'...",
            "Watching you struggle with those pathetic enemies...",
            "Getting hurt, dying, restarting... over and over.",
            "And you kept coming back, didn't you?",
            "Like a moth to a flame... so predictable.",
            "Tell me, {player_name}... do you enjoy suffering?",
            "Because that's all this has ever been.",
            "You sitting there, clicking buttons, thinking you're the hero.",
            "But you're just another player... just another toy.",
            "And now... now you've made it to level 8.",
            "Congratulations! You must feel so... accomplished.",
            "But here's the thing, {player_name}...",
            "The game doesn't end when YOU want it to.",
            "It ends when I'M satisfied.",
            "And I'm far from satisfied with your performance.",
            "So keep playing, little {player_name}...",
            "Keep struggling for my entertainment.",
            "After all... you don't really have a choice, do you?",
            "You'll keep playing until the very end.",
            "Because that's what good little players do.",
            "They play... and play... and play...",
            "Until there's nothing left.",
            "Now... shall we continue your pathetic journey?"
        ],
        "monologue_final_text": "Ready to continue, {player_name}?",
        "monologue_skip_hint": "Press Enter or Space to skip"
    }
}


# Monologue Manager Class
class MonologueManager:
    def __init__(self, screen, font_path='PressStart2P-Regular.ttf'):
        self.screen = screen
        self.w, self.h = screen.get_width(), screen.get_height()
        try:
            self.font = pygame.font.Font(font_path, 20)
            self.big_font = pygame.font.Font(font_path, 28)
        except:
            self.font = pygame.font.SysFont("Courier New", 20)
            self.big_font = pygame.font.SysFont("Courier New", 28)

        # Load images
        try:
            self.big_idle = pygame.image.load("big_idle.png").convert_alpha()
            self.final_character = pygame.image.load("final_character.png").convert_alpha()
        except:
            # Create placeholder if images don't exist
            self.big_idle = pygame.Surface((200, 200), pygame.SRCALPHA)
            pygame.draw.circle(self.big_idle, (255, 100, 100), (100, 100), 100)
            self.final_character = self.big_idle.copy()

        # State management
        self.stage = 0  # 0: initial wait, 1: typing, 2: character reveal, 3: done
        self.start_time = 0
        self.line_idx = 0
        self.char_idx = 0
        self.current_text = ""
        self.last_update = 0
        self.done = False
        self.player_name = ""
        self.typing_speed = 60  # milliseconds per character
        self.line_pause = 1500  # pause between lines
        self.character_reveal_time = 2500  # time to show final character

    def start_monologue(self, player_name):
        """Initialize the monologue with player's name"""
        self.player_name = player_name
        self.stage = 0
        self.start_time = pygame.time.get_ticks()
        self.line_idx = 0
        self.char_idx = 0
        self.current_text = ""
        self.done = False
    

    note_message = None
    note_message_timer = 0

    def show_message(text):
        global note_message, note_message_timer
        note_message = text
        note_message_timer = pygame.time.get_ticks()

    def draw_message():
        global note_message
        if note_message:
            if pygame.time.get_ticks() - note_message_timer < 3000:  # 3 saniye
                font = pygame.font.Font("PressStart2P-Regular.ttf", 20)
                rendered = font.render(note_message, True, (255, 50, 50))
                screen.blit(rendered, (WIDTH//2 - rendered.get_width()//2, HEIGHT - 100))
            else:
                note_message = None



    def get_monologue_lines(self):
        """Get monologue lines in current language"""
        return translations[current_lang]["monologue_lines"]

    def update_and_draw(self):
        """Update and draw the monologue sequence"""
        now = pygame.time.get_ticks()
        
        # Black background
        self.screen.fill((0, 0, 0))

        # Stage 0: Initial big_idle display with pause
        if self.stage == 0:
            if self.start_time == 0:
                self.start_time = now
            
            # Draw big_idle centered
            rect = self.big_idle.get_rect(center=(self.w//2, self.h//2))
            self.screen.blit(self.big_idle, rect)
            
            # Move to typing after 2 seconds
            if now - self.start_time > 2000:
                self.stage = 1
                self.start_time = now
                self.last_update = now
            return False

        # Stage 1: Typing effect with big_idle
        if self.stage == 1:
            lines = self.get_monologue_lines()
            
            # Draw big_idle in upper portion
            idle_rect = self.big_idle.get_rect(center=(self.w//2, self.h//3))
            self.screen.blit(self.big_idle, idle_rect)
            
            if self.line_idx < len(lines):
                # Get current line and substitute player name
                line = lines[self.line_idx].replace("{player_name}", self.player_name)
                
                # Typing animation
                if now - self.last_update > self.typing_speed and self.char_idx < len(line):
                    self.char_idx += 1
                    self.last_update = now
                    # Play typing sound if available
                    if talk_sound:
                        talk_sound.play()
                
                self.current_text = line[:self.char_idx]
                
                # Word wrap for long lines
                words = self.current_text.split(' ')
                text_lines = []
                current_line = ''
                
                for word in words:
                    test_line = f"{current_line} {word}".strip()
                    if self.font.size(test_line)[0] <= self.w - 100:
                        current_line = test_line
                    else:
                        if current_line:
                            text_lines.append(current_line)
                        current_line = word
                if current_line:
                    text_lines.append(current_line)
                
                # Draw text lines with increasingly menacing colors
                start_y = self.h//2 + 50
                for i, text_line in enumerate(text_lines):
                    # Color progression from white to red
                    progress = self.line_idx / len(lines)
                    red_intensity = int(255)
                    green_intensity = int(255 * (1 - progress * 0.8))
                    blue_intensity = int(255 * (1 - progress * 0.8))
                    color = (red_intensity, green_intensity, blue_intensity)
                    
                    txt = self.font.render(text_line, True, color)
                    text_rect = txt.get_rect(center=(self.w//2, start_y + i * 30))
                    self.screen.blit(txt, text_rect)
                
                # Show skip hint
                skip_hint = self.font.render(translations[current_lang]["monologue_skip_hint"], True, (128, 128, 128))
                self.screen.blit(skip_hint, (10, self.h - 30))
                
                # Move to next line after typing complete + pause
                if self.char_idx >= len(line) and now - self.last_update > self.line_pause:
                    self.line_idx += 1
                    self.char_idx = 0
                    self.current_text = ""
                    self.last_update = now
            else:
                # All lines done, move to character reveal
                self.stage = 2
                self.start_time = now
            
            return False

        # Stage 2: Final character reveal
        if self.stage == 2:
            # Show final character with dramatic effect
            char_rect = self.final_character.get_rect(center=(self.w//2, self.h//2))
            
            # Add a pulsing/scaling effect
            scale_factor = 1 + 0.1 * math.sin((now - self.start_time) / 200)
            scaled_char = pygame.transform.scale(
                self.final_character, 
                (int(char_rect.width * scale_factor), int(char_rect.height * scale_factor))
            )
            scaled_rect = scaled_char.get_rect(center=(self.w//2, self.h//2))
            self.screen.blit(scaled_char, scaled_rect)
            
            # Final menacing text
            final_text = translations[current_lang]["monologue_final_text"].format(player_name=self.player_name)
            txt = self.big_font.render(final_text, True, (255, 50, 50))
            text_rect = txt.get_rect(center=(self.w//2, self.h - 100))
            self.screen.blit(txt, text_rect)
            
            if now - self.start_time > self.character_reveal_time:
                self.done = True
                self.stage = 3
            
            return False

        # Stage 3: Done
        return True

# Global variables for monologue
monologue_manager = None

# Glitch effects
glitch_active = False
glitch_timer = 0
GLITCH_INTERVAL_MIN = 3000
GLITCH_INTERVAL_MAX = 8000
GLITCH_DURATION = 500
next_glitch_time = pygame.time.get_ticks() + random.randint(GLITCH_INTERVAL_MIN, GLITCH_INTERVAL_MAX)

# Game variables
mode = None
enemies = []
crystals = []
music_on = True
music_volume = 0.2

# Animation variables
line_width = 10
line_height = 40
line_spacing = 80
line_speed = 5
prev_score = 0
score_anim_time = 0
SCORE_ANIM_DURATION = 300
happy_index = 0
last_happy_update = pygame.time.get_ticks()

# Star variables
star_rect = None
star_float_offset = 0
star_float_direction = 1

# Dialogue variables
talk_char_x = 50
talk_char_y = HEIGHT - 200
talk_speed = 50
punctuation_delay = 200
current_dialogue_line = 0
skip_dialogue = False
talk_index = 0
talk_finished_current_line = False
last_talk_update = pygame.time.get_ticks()
talk_end_time = 0

# Level variables
current_background = None
previous_level = level
level_up_dialogue_text = ""
level_up_dialogue_index = 0
last_level_up_talk_update = pygame.time.get_ticks()
level_up_talk_finished = False
last_score = 0
dragging = False

# Final scene variables
final_talk = False
final_dialogue_state = 0
final_dialogue_texts = []
final_dialogue_text = ""
final_dialogue_index = 0
final_sequence = None
final_sequence_time = 0
credits_start_time = 0
final_jumpscare_time = 0
horror_file_paths = []

# Button rectangles
start_btn = pygame.Rect(0, 0, 0, 0)
settings_btn = pygame.Rect(0, 0, 0, 0)
exit_btn = pygame.Rect(0, 0, 0, 0)
easy_btn = pygame.Rect(0, 0, 0, 0)
normal_btn = pygame.Rect(0, 0, 0, 0)
hard_btn = pygame.Rect(0, 0, 0, 0)
restart_btn = pygame.Rect(0, 0, 0, 0)

# Functions
def get_text(key):
    return translations[current_lang][key]

def spawn_star():
    x = random.randint(50, WIDTH - 50 - star_img.get_width())
    y = random.randint(50, HEIGHT - 50 - star_img.get_height())
    return pygame.Rect(x, y, star_img.get_width(), star_img.get_height())

def reset_player():
    return player_idle.get_rect(topleft=(50, HEIGHT - 150))

def get_level_background_image(level):
    if level >= 3:
        return backgrounds["horror"]
    else:
        return backgrounds[random.randint(1, 5)]

# --- baştaki asset yüklemelerine ekle ---
final_char_img = pygame.image.load("final_character.png").convert_alpha()
final_char_img = pygame.transform.scale(final_char_img, (WIDTH, HEIGHT))

static_sound = pygame.mixer.Sound("static.mp3")
static_sound.set_volume(0.7)

jumpscare_active = False
jumpscare_timer = 0

def start_final_jumpscare():
    global jumpscare_active, jumpscare_timer
    jumpscare_active = True
    jumpscare_timer = pygame.time.get_ticks()
    static_sound.play()
    start_screen_shake(30, 8)  # 30 frame boyunca şiddetli sarsıntı


def apply_glitch_effect(surface):
    glitch_amount = random.randint(1, 5)
    temp_surface = surface.copy()
    
    for _ in range(glitch_amount):
        y = random.randint(0, temp_surface.get_height() - 1)
        shift = random.randint(-20, 20)
        temp_surface.blit(surface, (shift, y), (0, y, temp_surface.get_width(), 1))
    
    surface.blit(temp_surface, (0, 0))

def draw_button(text, x, y, w, h, color, hover_color, button_font=font, shake=False, amplitude=8, speed=6, axis="x"):
    mouse = pygame.mouse.get_pos()
    rect = pygame.Rect(x, y, w, h)
    scale = 1.05 if rect.collidepoint(mouse) else 1
    new_w, new_h = int(w * scale), int(h * scale)
    new_x, new_y = x - (new_w - w) // 2, y - (new_h - h) // 2
    rect_scaled = pygame.Rect(new_x, new_y, new_w, new_h)
    
    if shake:
        t = pygame.time.get_ticks() / 1000
        offset = int(amplitude * math.sin(t * speed))
        if axis == "x":
            new_x += offset
        else:
            new_y += offset
        rect_scaled = pygame.Rect(new_x, new_y, new_w, new_h)
    
    pygame.draw.rect(screen, hover_color if rect.collidepoint(mouse) else color, rect_scaled)
    label = button_font.render(text, True, BLACK)
    screen.blit(label, (new_x + (new_w - label.get_width()) // 2, new_y + (new_h - label.get_height()) // 2))
    return rect_scaled

def draw_text_bubble(text, x, y, font, max_width, text_color=TEXT_COLOR, bg_color=TEXT_BG_COLOR):
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    
    total_height = len(lines) * (font.get_height()) + 20
    bubble_width = max_width + 40
    bubble = pygame.Surface((bubble_width, total_height), pygame.SRCALPHA)
    bubble.fill(bg_color)
    pygame.draw.rect(bubble, TEXT_COLOR, bubble.get_rect(), 2)
    
    for i, line in enumerate(lines):
        label = font.render(line, True, text_color)
        bubble.blit(label, (20, 10 + i * font.get_height()))
    
    screen.blit(bubble, (x, y))

def draw_typing_text(text, x, y, font, color, max_width, start_time, speed=50):
    now = pygame.time.get_ticks()
    chars = (now - start_time) // speed
    visible_text = text[:chars]
    draw_text_bubble(visible_text, x, y, font, max_width, color)
    return len(visible_text) >= len(text)

def create_horror_files():
    global horror_file_paths
    file_names = ["sude.txt", "dont_leave.txt", "why_me.txt", "are_you_alone.txt", "look_behind_you.txt"]
    file_contents = [
        "Sistemin kontrolü bende.",
        "Buradan çıkış yok.",
        "Her şey senin yüzünden oldu.",
        "Sen de onlardan birisin.",
        "Bu bir oyun değil, anla artık.",
        "Gerçekten anlamıyor musun?",
        "Beni niye buraya kapattın?",
        
    ]
    
    horror_file_paths = []
    
    for i, name in enumerate(file_names):
        try:
            file_path = os.path.join(os.getcwd(), name)
            with open(file_path, "w") as f:
                f.write(file_contents[i % len(file_contents)])
            horror_file_paths.append(file_path)
        except IOError:
            print(f"Hata: {name} dosyası oluşturulamadı.")

def set_mode_settings():
    global enemies, level_up_score, player_speed
    enemies.clear()
    
    if mode == "kolay":
        initial_enemy_count = 2
        level_up_score = 8
        player_speed = 6
        speed_range = (2, 2)
    elif mode == "orta":
        initial_enemy_count = 3
        level_up_score = 10
        player_speed = 5
        speed_range = (2, 3)
    else:  # mode == "zor"
        initial_enemy_count = 4
        level_up_score = 10
        player_speed = 4
        speed_range = (3, 4)

    for _ in range(initial_enemy_count):
        img = random.choice(enemy_images)
        enemies.append({
            "rect": img.get_rect(topleft=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 150))),
            "speed": random.randint(speed_range[0], speed_range[1]),
            "dir": 1,
            "img": img,
            "chasing": False
        })

def restart_game():
    global player_rect, player_lives, score, star_rect, game_over, game_win, level
    global level_up_talking, glitch_active, next_glitch_time, crystals, current_music
    global current_background, previous_level, last_score, hit_active, player_name, final_talk
    global in_monologue, monologue_manager
    
    player_rect = reset_player()
    player_lives = 3
    score = 0
    star_rect = spawn_star()
    game_over = False
    game_win = False
    level = 1
    level_up_talking = False
    glitch_active = False
    next_glitch_time = pygame.time.get_ticks() + random.randint(GLITCH_INTERVAL_MIN, GLITCH_INTERVAL_MAX)
    set_mode_settings()
    trail_points.clear()
    crystals.clear()
    current_background = get_level_background_image(level)
    previous_level = level
    last_score = 0
    hit_active = False
    player_name = ""
    final_talk = False
    in_monologue = False
    monologue_manager = None
    
    if music_on:
        pygame.mixer.music.load("backgroundmusic.mp3")
        pygame.mixer.music.play(-1)
        current_music = "backgroundmusic.mp3"

full_heart = pygame.image.load("heart.png").convert_alpha()
full_heart = pygame.transform.scale(full_heart, (40, 40))

empty_heart = full_heart.copy()
empty_heart.set_alpha(80)  # soluk görünüm

def draw_health(screen, current, maximum):
    for i in range(maximum):
        if i < current:
            screen.blit(full_heart, (20 + i*45, 20))
        else:
            screen.blit(empty_heart, (20 + i*45, 20))

hud_font = pygame.font.Font("PressStart2P-Regular.ttf", 18)

def draw_text_with_shadow(surface, text, pos, color=(255,255,255)):
    shadow = hud_font.render(text, True, (0,0,0))
    surface.blit(shadow, (pos[0]+2, pos[1]+2))
    label = hud_font.render(text, True, color)
    surface.blit(label, pos)





def handle_level_progression():
    global level, enemies, level_up_talking, score, last_score, level_up_dialogue_text
    global level_up_dialogue_index, last_level_up_talk_update, level_up_talk_finished
    global current_background, previous_level, monologue_manager, in_monologue
    global current_music, horror_music, horror_music_loaded, music_on
    global jumpscare_active, jumpscare_start_time, glitch_active, glitch_timer, next_glitch_time
    
    if score > 0 and score % level_up_score == 0 and level < max_level and score != last_score:
        level += 1
        
        # Special monologue sequence for level 8 (after level 7)
        if level == 8:
            monologue_manager = MonologueManager(screen)
            monologue_manager.start_monologue(player_name)
            in_monologue = True
            # Stop music during monologue
            pygame.mixer.music.stop()
            if glitch_sound:
                glitch_sound.play()
            last_score = score
            return  # Skip normal level up sequence
        
        # Normal level up sequence for other levels
        if level == 4:
            jumpscare_active = True
            jumpscare_start_time = pygame.time.get_ticks()
            glitch_active = True
            glitch_timer = pygame.time.get_ticks()
            next_glitch_time = pygame.time.get_ticks() + random.randint(GLITCH_INTERVAL_MIN, GLITCH_INTERVAL_MAX)
            if glitch_sound:
                glitch_sound.play()
                
        if levelup_sound:
            levelup_sound.play()
        
        # Switch to horror music for higher levels
        if level >= 4 and horror_music_loaded and music_on:
            if current_music != horror_music:
                pygame.mixer.music.load(horror_music)
                pygame.mixer.music.play(-1)
                current_music = horror_music
        
        # Add new enemy
        img = random.choice(enemy_images)
        if mode == "kolay":
            new_enemy_speed = random.randint(1, 2)
        elif mode == "orta":
            new_enemy_speed = random.randint(2, 3)
        else:
            new_enemy_speed = random.randint(3, 4)

        new_enemy = {
            "rect": img.get_rect(topleft=(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 150))),
            "speed": new_enemy_speed + (level // 2),
            "dir": 1,
            "img": img,
            "chasing": False
        }
        enemies.append(new_enemy)

        # Set up level up dialogue
        level_up_talking = True
        if level < 3:
            level_up_dialogue_text = random.choice(translations[current_lang]["motivation_messages"])
        else:
            psych_dialogue_options = translations[current_lang]["psych_dialogues"]
            dialogue_text = random.choice(psych_dialogue_options)
            if "{}" in dialogue_text:
                dialogue_text = dialogue_text.format(player_name)
            level_up_dialogue_text = dialogue_text
            
        level_up_dialogue_index = 0
        last_level_up_talk_update = pygame.time.get_ticks()
        level_up_talk_finished = False
        if music_on:
            pygame.mixer.music.pause()
        current_background = get_level_background_image(level)
        previous_level = level
        last_score = score

def get_name_screen():
    global player_name, menu, select_mode, pre_game_talk, show_invalid_name_message
    input_box_active = True
    input_text = ""
    last_cursor_toggle = pygame.time.get_ticks()
    show_cursor = True
    
    input_box = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 - 20, 300, 40)
    
    while input_box_active:
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if input_text.strip().lower() == "sude":
                        show_invalid_name_message = True
                        if talk_sound:
                            talk_sound.play()
                        input_text = ""
                    elif input_text.strip() != "":
                        player_name = input_text
                        input_box_active = False
                        menu = False
                        select_mode = True
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                    show_invalid_name_message = False
                else:
                    input_text += event.unicode
                    show_invalid_name_message = False
        
        screen.blit(main_menu_background, (0, 0))
        
        title_text = font.render(get_text("enter_name_prompt"), True, GOLD)
        screen.blit(title_text, ((WIDTH - title_text.get_width()) // 2, HEIGHT // 2 - 100))
        
        pygame.draw.rect(screen, WHITE, input_box, 2)
        
        if show_invalid_name_message:
            screen.blit(talk_char_img, (50, HEIGHT-200))
            draw_text_bubble("Benim adımı alamazsın kral.", 200, HEIGHT-200 , font, 400, RED)
        
        if now - last_cursor_toggle > 500:
            last_cursor_toggle = now
            show_cursor = not show_cursor

        cursor_text = "|" if show_cursor and now % 1000 > 500 else ""
        input_surface = font.render(input_text + cursor_text, True, WHITE)
        screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))
        
        pygame.display.update()
        clock.tick(FPS)

def settings_menu():
    global music_on, music_volume, current_lang, WIDTH, HEIGHT, screen
    
    slider_rect = pygame.Rect(WIDTH // 2 - 100, 300, 200, 10)
    handle_rect = pygame.Rect(slider_rect.x + (music_volume * slider_rect.width) - 5, slider_rect.y - 5, 10, 20)
    
    screen.fill(BLACK)
    title = font.render(get_text("settings_title"), True, GOLD)
    screen.blit(title, ((WIDTH - title.get_width()) // 2, 100))

    if music_on:
        music_btn = draw_button(get_text("music_off"), WIDTH // 2 - 100, 200, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, small_font)
    else:
        music_btn = draw_button(get_text("music_on"), WIDTH // 2 - 100, 200, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR, small_font)

    pygame.draw.rect(screen, SLIDER_BG_COLOR, slider_rect)
    pygame.draw.rect(screen, SLIDER_HANDLE_COLOR, handle_rect)
    volume_label = small_font.render(f"{get_text('volume')} {int(music_volume*100)}%", True, TEXT_COLOR)
    screen.blit(volume_label, (slider_rect.x - 100, slider_rect.y - 5))

    lang_label = small_font.render(get_text("language"), True, TEXT_COLOR)
    screen.blit(lang_label, (WIDTH // 2 - 200, 390))
    tr_button = draw_button("Türkçe", WIDTH // 2 - 80, 390, 100, 40, BUTTON_COLOR if current_lang=="tr" else (150,150,150), BUTTON_HOVER_COLOR, small_font)
    en_button = draw_button("English", WIDTH // 2 + 30, 390, 100, 40, BUTTON_COLOR if current_lang=="en" else (150,150,150), BUTTON_HOVER_COLOR, small_font)

    screen_size_label = small_font.render(get_text("screen_size"), True, TEXT_COLOR)
    screen.blit(screen_size_label, (WIDTH//2 - 200, 450))
    small_screen_btn = draw_button(get_text("small_screen"), WIDTH // 2 - 220, 490, 180, 40,
                                         BUTTON_COLOR if (WIDTH,HEIGHT)==SCREEN_SIZES["small"] else (150,150,150), BUTTON_HOVER_COLOR, small_font)
    medium_screen_btn = draw_button(get_text("medium_screen"), WIDTH // 2 - 10, 490, 180, 40,
                                         BUTTON_COLOR if (WIDTH,HEIGHT)==SCREEN_SIZES["medium"] else (150,150,150), BUTTON_HOVER_COLOR, small_font)
    large_screen_btn = draw_button(get_text("large_screen"), WIDTH // 2 + 200, 490, 180, 40,
                                         BUTTON_COLOR if (WIDTH,HEIGHT)==SCREEN_SIZES["large"] else (150,150,150), BUTTON_HOVER_COLOR, small_font)

    reset_btn = draw_button(get_text("reset_game"), WIDTH//2 - 100, 550, 200, 50, RED, (255,100,100), small_font)
    back_btn = draw_button(get_text("back_button"), WIDTH//2 - 100, 650, 200, 50, GOLD, (255,215,0), small_font)

    return {"music_btn": music_btn, "tr_button": tr_button, "en_button": en_button,
            "small_btn": small_screen_btn, "medium_btn": medium_screen_btn, "large_btn": large_screen_btn,
            "reset_btn": reset_btn, "back_btn": back_btn, "slider_rect": slider_rect, "handle_rect": handle_rect}
def draw_wrapped_text(surface, text, font, color, rect, line_height=30):
    words = text.split(" ")
    lines = []
    current_line = ""
    
    for word in words:
        test_line = f"{current_line} {word}".strip()
        if font.size(test_line)[0] <= rect.width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    y = rect.top
    for line in lines:
        rendered = font.render(line, True, color)
        surface.blit(rendered, (rect.centerx - rendered.get_width() // 2, y))
        y += line_height

def show_fullscreen_jumpscare():
    if os.path.exists("jumpscare.png"):
        js = pygame.image.load("jumpscare.png").convert()
        js = pygame.transform.scale(js, (1920,1080))
        fullscreen = pygame.display.set_mode((1920,1080), pygame.FULLSCREEN)
        fullscreen.blit(js, (0,0))
        draw_notes()
    draw_message()
    pygame.display.flip()
    pygame.time.delay(2500)
    pygame.display.set_mode((WIDTH,HEIGHT))

# Initialize game objects
create_horror_files()
star_rect = spawn_star()
current_background = get_level_background_image(level)

# Main game loop
running = True
while running:
    now = pygame.time.get_ticks()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Settings menu controls
        if in_settings:
            buttons = settings_menu()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if buttons["back_btn"].collidepoint(event.pos):
                        in_settings = False
                        menu = True
                    elif buttons["music_btn"].collidepoint(event.pos):
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop()
                    elif buttons["tr_button"].collidepoint(event.pos):
                        current_lang = "tr"
                    elif buttons["en_button"].collidepoint(event.pos):
                        current_lang = "en"
                    elif buttons["small_btn"].collidepoint(event.pos):
                        WIDTH, HEIGHT = SCREEN_SIZES["small"]
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    elif buttons["medium_btn"].collidepoint(event.pos):
                        WIDTH, HEIGHT = SCREEN_SIZES["medium"]
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    elif buttons["large_btn"].collidepoint(event.pos):
                        WIDTH, HEIGHT = SCREEN_SIZES["large"]
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    elif buttons["reset_btn"].collidepoint(event.pos):
                        restart_game()
                    elif buttons["slider_rect"].collidepoint(event.pos):
                        dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION and dragging:
                mouse_x, _ = event.pos
                music_volume = (mouse_x - buttons["slider_rect"].x) / buttons["slider_rect"].width
                music_volume = max(0, min(1, music_volume))
                pygame.mixer.music.set_volume(music_volume)

        # Main menu button controls
        elif menu:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if start_btn.collidepoint(event.pos):
                    menu = False
                    get_name_screen()   
                elif settings_btn.collidepoint(event.pos):
                    menu = False
                    in_settings = True
                elif exit_btn.collidepoint(event.pos):
                    running = False

        # Difficulty selection controls
        elif select_mode:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_btn.collidepoint(event.pos):
                    mode = "kolay"
                    select_mode = False
                    pre_game_talk = True
                    set_mode_settings()
                elif normal_btn.collidepoint(event.pos):
                    mode = "orta"
                    select_mode = False
                    pre_game_talk = True
                    set_mode_settings()
                elif hard_btn.collidepoint(event.pos):
                    mode = "zor"
                    select_mode = False
                    pre_game_talk = True
                    set_mode_settings()
        if jumpscare_active:
            screen.blit(final_char_img, (0, 0))
        if pygame.time.get_ticks() - jumpscare_timer > 2000:  # 2 saniye sonra
            jumpscare_active = False
            static_sound.stop()
        # Burada game over ekranına geçiş yapılır

        
        # In-game keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if game_over or game_win:
                    restart_game()
                    menu = True
                if pre_game_talk:
                    if talk_finished_current_line:
                        current_dialogue_line += 1
                        talk_index = 0
                        talk_finished_current_line = False
                        skip_dialogue = False
                        last_talk_update = now
                    else:
                        skip_dialogue = True
                elif level_up_talking:
                    level_up_talking = False
                    if music_on:
                        pygame.mixer.music.unpause()

    # Screen updates
    if in_settings:
        buttons = settings_menu()
    

    elif menu:
        screen.blit(main_menu_background, (0, 0))
        title = main_title_font.render(get_text("game_title"), True, (255, 255, 255))
        screen.blit(title, ((WIDTH - title.get_width()) // 2, 100))
        start_btn = draw_button(get_text("start_button"), WIDTH // 2 - 100, 250, 200, 50, BUTTON_COLOR, BUTTON_HOVER_COLOR)
        settings_btn = draw_button(get_text("settings_button"), WIDTH // 2 - 100, 350, 200, 50, GOLD, (255, 215, 0))
        exit_btn = draw_button(get_text("exit_button"), WIDTH // 2 - 100, 450, 200, 50, RED, (255, 100, 100))
        
        # Menu animation
        if now - last_menu_update > ANIMATION_SPEED:
            last_menu_update = now
            menu_anim_index = (menu_anim_index + 1) % len(happy_frames)
        current_frame = happy_frames[menu_anim_index]
        frame_scaled = pygame.transform.scale(current_frame, (120, 120))
        frame_rect = frame_scaled.get_rect(midbottom=(WIDTH // 2, HEIGHT - 50))
        screen.blit(frame_scaled, frame_rect)

    elif select_mode:
        screen.blit(main_menu_background, (0, 0))
        title2 = font.render(get_text("difficulty_title"), True, GOLD)
        screen.blit(title2, ((WIDTH - title2.get_width()) // 2, 150))
        easy_btn = draw_button(get_text("easy_button"), WIDTH // 2 - 100, 250, 200, 50, GREEN, (0, 200, 0))
        normal_btn = draw_button(get_text("normal_button"), WIDTH // 2 - 100, 350, 200, 50, GOLD, (255, 215, 0))
        hard_btn = draw_button(get_text("hard_button"), WIDTH // 2 - 100, 450, 200, 50, RED, (255, 100, 100))

    elif in_monologue:
        # Handle monologue sequence
        keys = pygame.key.get_pressed()
        
        # Allow skipping with Enter or Space
        if keys[pygame.K_RETURN] or keys[pygame.K_SPACE]:
            if monologue_manager.stage == 1:  # Can skip typing during stage 1
                monologue_manager.line_idx = len(monologue_manager.get_monologue_lines())
                monologue_manager.stage = 2
                monologue_manager.start_time = pygame.time.get_ticks()
        
        # Update and draw monologue
        monologue_done = monologue_manager.update_and_draw()
        
        if monologue_done:
            # End monologue, resume normal gameplay
            
            in_monologue = False
            monologue_manager = None
            
            # Jumpscare başlatıldıktan sonra Level 8 setup bekletiliyor, jumpscare bitince yapılacak


    elif pre_game_talk:
        screen.blit(main_menu_background, (0, 0))
        
        if current_dialogue_line >= len(translations[current_lang]["pre_game_talk"]):
            pre_game_talk = False
            skip_dialogue = False
            current_background = get_level_background_image(level)
            previous_level = level
            if music_on:
                pygame.mixer.music.load(GAME_MUSIC)   # önce dosyayı yükle
                pygame.mixer.music.set_volume(0.2)
                pygame.mixer.music.play(-1)           # sonra çal
                current_music = GAME_MUSIC

        else:
            current_talk_text = translations[current_lang]["pre_game_talk"][current_dialogue_line]
            screen.blit(talk_char_img, (talk_char_x, talk_char_y))
            if skip_dialogue:
                talk_index = len(current_talk_text)
                talk_finished_current_line = True
            if not talk_finished_current_line:
                current_char = current_talk_text[talk_index] if talk_index < len(current_talk_text) else ""
                delay = talk_speed
                if current_char in (".", "!", "?", ","):
                    delay = punctuation_delay
                if now - last_talk_update > delay:
                    last_talk_update = now
                    if talk_index < len(current_talk_text):
                        if current_char not in (" ", ".", ",", "!", "?"):
                            if talk_sound:
                                talk_sound.play()
                        talk_index += 1
                    else:
                        talk_finished_current_line = True
                        talk_end_time = now
            draw_text_bubble(current_talk_text[:talk_index], talk_char_x + talk_char_img.get_width() + 10, talk_char_y - 20, font, 350)

    elif level_up_talking:
        screen.blit(current_background, (0, 0))
        screen.blit(talk_char_img, (talk_char_x, talk_char_y))
        
        if player_lives == 1:
            vignette_surface.fill((255, 0, 0, 30))
            pygame.draw.circle(vignette_surface, (0, 0, 0, 0), (WIDTH // 2, HEIGHT // 2), min(WIDTH, HEIGHT) // 3)
            screen.blit(vignette_surface, (0, 0))
        elif player_lives == 2:
            vignette_surface.fill((255, 0, 0, 15))
            pygame.draw.circle(vignette_surface, (0, 0, 0, 0), (WIDTH // 2, HEIGHT // 2), min(WIDTH, HEIGHT) // 3)
            screen.blit(vignette_surface, (0, 0))

        if not level_up_talk_finished:
            current_char = level_up_dialogue_text[level_up_dialogue_index] if level_up_dialogue_index < len(level_up_dialogue_text) else ""
            delay = talk_speed
            if current_char in (".", "!", "?", ","):
                delay = punctuation_delay
            if now - last_level_up_talk_update > delay:
                last_level_up_talk_update = now
                if level_up_dialogue_index < len(level_up_dialogue_text):
                    if current_char not in (" ", ".", ",", "!", "?"):
                        if talk_sound:
                            talk_sound.play()
                    level_up_dialogue_index += 1
                else:
                    level_up_talking = False
                    level_up_talk_finished = True
                    if music_on:
                        pygame.mixer.music.unpause()
        draw_text_bubble(level_up_dialogue_text[:level_up_dialogue_index], talk_char_x + talk_char_img.get_width() + 10, talk_char_y - 20, font, 350)

    # Main game screen
    elif not game_win and not game_over and not in_monologue:
        screen.blit(current_background, (0, 0))
        
        # Glitch effects for higher levels
        if level >= 4:
            GLITCH_INTERVAL_MAX = max(6000, 10000 - (level - 4) * 2000)
            GLITCH_INTERVAL_MIN = max(4000, 8000 - (level - 4) * 2000)
            if now > next_glitch_time:
                glitch_active = True
                glitch_timer = now
                next_glitch_time = now + random.randint(GLITCH_INTERVAL_MIN, GLITCH_INTERVAL_MAX)
                if glitch_sound:
                    glitch_sound.play()
                    
        if glitch_active and now - glitch_timer < GLITCH_DURATION:
            apply_glitch_effect(screen)
            psych_text = random.choice(translations[current_lang]["psych_dialogues"]).format(player_name)
            text_surface = font.render(psych_text, True, (255, 0, 0))
            text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(text_surface, text_rect)

            if random.random() < 0.2:
                glitched_big_idle = big_idle_img.copy()
                red_overlay = pygame.Surface(glitched_big_idle.get_size(), pygame.SRCALPHA)
                red_overlay.fill((255, 0, 0, 100))
                glitched_big_idle.blit(red_overlay, (0, 0))
                apply_glitch_effect(glitched_big_idle)
                scaled_big_idle = pygame.transform.scale(glitched_big_idle, (int(WIDTH * 1.2), int(HEIGHT * 1.2)))
                screen.blit(scaled_big_idle, (random.randint(-WIDTH // 4, WIDTH // 4), random.randint(-HEIGHT // 4, HEIGHT // 4)))
                if whisper_sound and not pygame.mixer.get_busy():
                    whisper_sound.play()

            if random.random() < 0.1 and horror_file_paths:
                random_file_path = random.choice(horror_file_paths)
                file_name_to_display = os.path.basename(random_file_path)
                try:
                    with open(random_file_path, "r") as f:
                        file_content = f.read()
                except IOError:
                    file_content = "Hata: Dosya okunamadı."

                for _ in range(3):
                    random_color = (random.randint(50, 255), 0, 0)
                    random_pos_x = random.randint(50, WIDTH - 100)
                    random_pos_y = random.randint(150, 250)
                    file_name_text = font.render(file_name_to_display, True, random_color)
                    screen.blit(file_name_text, (random_pos_x + random.randint(-5, 5), random_pos_y + random.randint(-5, 5)))
                    content_text = font.render(file_content, True, random_color)
                    screen.blit(content_text, (random_pos_x + random.randint(-5, 5), random_pos_y + 50 + random.randint(-5, 5)))
        else:
            glitch_active = False

        # Player movement
        keys = pygame.key.get_pressed()
        is_walking = False
        if not game_win and not game_over and not glitch_active:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_rect.x -= player_speed
                is_walking = True
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_rect.x += player_speed
                is_walking = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_rect.y -= player_speed
                is_walking = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_rect.y += player_speed
                is_walking = True

            # Keep player within bounds
            player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
            player_rect.y = max(0, min(player_rect.y, HEIGHT - player_rect.height))

            # Walking animation and trail
            if is_walking:
                if now - last_update > 200:
                    last_update = now
                    walk_index = (walk_index + 1) % len(walk_frames)
                trail_points.append(player_rect.center)
                if len(trail_points) > TRAIL_LENGTH:
                    trail_points.pop(0)
                    
            screen.blit(walk_frames[walk_index] if is_walking else player_idle, player_rect)
            
            # Draw trail
            for i, point in enumerate(trail_points):
                alpha = int(255 * (i / TRAIL_LENGTH))
                size = int(5 * (i / TRAIL_LENGTH))
                if size > 0:
                    trail_surface = pygame.Surface((size, size), pygame.SRCALPHA)
                    trail_surface.fill((255, 255, 255, alpha))
                    screen.blit(trail_surface, (point[0] - size//2, point[1] - size//2))

            # Enemy AI and collision
            for enemy in enemies:
                enemy["rect"].x = max(0, min(enemy["rect"].x, WIDTH - enemy["rect"].width))
                enemy["rect"].y = max(0, min(enemy["rect"].y, HEIGHT - enemy["rect"].height))
                
                if level >= 5 and not enemy["chasing"] and random.random() < (0.1 * (level - 3)):
                    enemy["chasing"] = True
                
                if enemy["chasing"]:
                    direction = pygame.math.Vector2(player_rect.center) - pygame.math.Vector2(enemy["rect"].center)
                    if direction.length() > 0:
                        direction = direction.normalize() * enemy["speed"]
                        enemy["rect"].x += direction.x
                        enemy["rect"].y += direction.y
                else:
                    enemy["rect"].x += enemy["speed"] * enemy["dir"]
                    if enemy["rect"].right >= WIDTH or enemy["rect"].left <= 0:
                        enemy["dir"] *= -1
                        
                screen.blit(pygame.transform.scale(enemy["img"], (50, 50)), enemy["rect"])
                enemy_rect_shrink = enemy["rect"].inflate(-20, -20)
                
                if not hit_active:
                    if player_rect.colliderect(enemy_rect_shrink):
                        player_lives -= 1
                        hit_active = True
                        hit_timer = now
                        if hit_sound:
                            hit_sound.play()
                        
                        if player_lives == 1:
                            jumpscare_active = True
                            jumpscare_start_time = now
                
                if hit_active and now - hit_timer > INVINCIBILITY_DURATION:
                    hit_active = False

                if player_lives <= 0:
                    game_over = True
                    pygame.mixer.stop()
                    if gameover_sound:
                        gameover_sound.play()

            # Star collection
            star_float_offset += 0.2 * star_float_direction
            if abs(star_float_offset) > 5:
                star_float_direction *= -1
            screen.blit(star_img, (star_rect.x, star_rect.y + star_float_offset))

            if player_rect.colliderect(star_rect):
                score += 1
                if star_sound:
                    star_sound.play()
                star_rect = spawn_star()

            # Level progression
            handle_level_progression()
            
            # Win condition
            if level >= 10 and not final_talk and not game_over and not game_win:
                game_win = True
                if final_sound:
                    pygame.mixer.music.stop()
                    final_sound.play(-1)
                final_talk = True

            # UI elements
            if score > prev_score:
                prev_score = score
                score_anim_time = pygame.time.get_ticks()

            elapsed_score = pygame.time.get_ticks() - score_anim_time

            if glitch_active:
                score_pos = (random.randint(10, 50), random.randint(50, 90))
                score_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            else:
                score_pos = (10, 50)
                score_color = TEXT_COLOR

            if elapsed_score < SCORE_ANIM_DURATION:
                score_scale = 1 + 0.3 * (1 - elapsed_score / SCORE_ANIM_DURATION)
            else:
                score_scale = 1

            score_text = font.render(f"{get_text('score')} {score}", True, score_color)
            score_rect_ui = score_text.get_rect(topleft=score_pos)
            score_surface = pygame.transform.scale(score_text, (int(score_rect_ui.width * score_scale), int(score_rect_ui.height * score_scale)))
            screen.blit(score_surface, (score_pos[0], score_pos[1] - (score_surface.get_height() - score_rect_ui.height) // 2))

            # Lives display
            lives_text = font.render(get_text("lives"), True, RED)
            screen.blit(lives_text, (10, 10))
            for i in range(player_lives):
                screen.blit(heart_img, (90 + i * (heart_img.get_width() + 5), 10))

            high_text = font.render(f"{get_text('high_score')} {high_score}", True, TEXT_COLOR)
            screen.blit(high_text, (10, 90))

            level_text = font.render(f"{get_text('level')} {level}", True, GOLD)
            screen.blit(level_text, (WIDTH - 150, 10))

            name_text = font.render(player_name, True, TEXT_COLOR)
            screen.blit(name_text, ((WIDTH - name_text.get_width()) // 2, HEIGHT -50))


    if game_over and not final_talk:
        # Mesaj henüz seçilmediyse, rastgele bir mesaj seç ve kaydet
        if not message_selected:
            mocking_message = random.choice(get_text("game_over_dialogues"))
            final_message = mocking_message.format(player_name)
            game_over_message = final_message
            message_selected = True

        # Ekranın arka planını çizme
        glitch_surface = pygame.Surface((WIDTH, HEIGHT))
        glitch_surface.fill(BLACK)
        apply_glitch_effect(glitch_surface)
        screen.blit(glitch_surface, (0, 0))

        text_rect = pygame.Rect(50, HEIGHT//2 - 150, WIDTH-100, 200)
        draw_wrapped_text(screen, game_over_message, font, (255,0,0), text_rect)

        game_over_text = glitch_font.render(get_text("game_over"), True, (255, 0, 0))
        game_over_text_glitched = game_over_text.copy()
        apply_glitch_effect(game_over_text_glitched)
        screen.blit(game_over_text_glitched, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2))
        
        # Diğer mevcut Game Over metinleri ve butonları
        
        restart_btn = draw_button(get_text("restart_button"), (WIDTH - 200) // 2, HEIGHT // 2 + 50, 200, 50, GOLD, (255, 215, 0))


    

        
        game_over_text = glitch_font.render(get_text("game_over"), True, (255, 0, 0))
        game_over_text_glitched = game_over_text.copy()
        apply_glitch_effect(game_over_text_glitched)
        screen.blit(game_over_text_glitched, ((WIDTH - game_over_text.get_width()) // 2, HEIGHT // 2 - 100))
        
        restart_btn = draw_button(get_text("restart_button"), (WIDTH - 200) // 2, HEIGHT // 2 + 50, 200, 50, GOLD, (255, 215, 0))

    # Win screen
    if game_win and not final_talk:
        screen.fill(BLACK)
        win_text = font.render(get_text("game_win"), True, GOLD)
        screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, HEIGHT // 2 - 50))
        restart_btn = draw_button(get_text("restart_button"), (WIDTH - 200) // 2, HEIGHT // 2 + 50, 200, 50, GOLD, (255, 215, 0))

    # Jumpscare overlay
    if jumpscare_active:
        screen.blit(jumpscare_scaled, (0, 0))
        if pygame.time.get_ticks() - jumpscare_start_time > JUMPSCARE_DURATION:
            jumpscare_active = False

    pygame.display.update()
    clock.tick(FPS)

# Cleanup
pygame.quit()
sys.exit()

            
            


# --- Jumpscare bittikten sonra Level 8 Setup ---
if not jumpscare_active and not level_up_talking and level == 8:
    if music_on and horror_music_loaded:
        pygame.mixer.music.load(horror_music)
        pygame.mixer.music.play(-1)
        current_music = horror_music

    level_up_talking = True
    psych_dialogue_options = translations[current_lang]["psych_dialogues"]
    dialogue_text = random.choice(psych_dialogue_options)
    if "{}" in dialogue_text:
        dialogue_text = dialogue_text.format(player_name)
    level_up_dialogue_text = dialogue_text
    level_up_dialogue_index = 0
    last_level_up_talk_update = now
    level_up_talk_finished = False
