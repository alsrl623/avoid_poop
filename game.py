import pygame, sys, random
from pygame.locals import QUIT, K_LEFT, K_RIGHT

pygame.init()
clock = pygame.time.Clock()

pygame.display.set_caption('똥 피하기') 
ground = pygame.image.load('assets/main_background.png')
poo = pygame.image.load('assets/default_poo.png')

def Yeongdo_Bold(size):
    '''폰트 입력을 편하게'''
    return pygame.font.Font("assets/font.ttf", size)

class Difficulty:
    def __init__(self, Profile):
        '''Profile 클래스를 받아와 
        이름, 캐릭터, 난이도 변수 설정'''
        self.user_name = Profile.name
        self.char = Profile.char_img
        self.level = Profile.level

class Drop:
    '''장애물 Drop'''
    def __init__(self, screen):
        self.x = random.randint(0, 850) # 창 범위 내
        self.y = -3
        self.surface = screen

    def move(self):
        '''7픽셀씩 낙하'''
        self.y += 7

    def draw(self):
        '''화면 위 업데이트'''
        self.surface.blit(poo, (self.x, self.y))

class Game(Difficulty):
    '''본 게임'''

    def __init__(self, profile, screen, images):
        super().__init__(profile)

        self.surface = screen
        self.images = images
        self.char_img = self.char

        self.game_over = False
        self.pos_x, self.pos_y = 425, 570 # 캐릭터 초기 좌표
        self.score = 0
        self.drop_poos = []

    def update(self, screen, mouse_pos): 
        '''본게임 동작 업데이트
        main.py에서 반복문 실행'''

        # 난이도가 오르면 장애물 발생 틱이 감소
        if self.level == 1: A = 30
        elif self.level == 2: A = 25
        elif self.level == 3: A = 20
        elif self.level == 4: A = 15
        elif self.level == 5: A = 10
        elif self.level == 6: A = 5
        elif self.level == 7: A = 3
        if self.score % A == 0: self.drop_poos.append(Drop(self.surface))

        # 화면 위 표시
        self.surface.blit(ground, (0, 0))
        self.surface.blit(self.char, (self.pos_x, self.pos_y))

        # 장애물 발생
        for poo_obj in self.drop_poos:
            poo_obj.move()
            poo_obj.draw()

        # key press 감지
        key_press = pygame.key.get_pressed()
        if key_press[K_LEFT]: # 왼쪽 방향키 -> 범위 내 좌측으로 7픽셀 이동
            if self.pos_x > 0: self.pos_x -= 7
        if key_press[K_RIGHT]: # 오른쪽 방향키 -> 범위 내 우측으로 7픽셀 이동
            if self.pos_x < 850: self.pos_x += 7 

        # 생존 상태 -> 점수 추가
        self.score += 1
        text_score = Yeongdo_Bold(50).render(f'score: {self.score}', True, (255, 206, 27))
        self.surface.blit(text_score, (20, 10))
        # 180점마다 난이도 상승(최고 난이도 = 7)
        if (self.score % 180 == 0) and self.level < 7: self.level += 1
        # 화면 위 'level up!' 표시
        if (self.score % 180 <= 60) and (0 < self.score // 180 < 7):
            level_up = Yeongdo_Bold(50).render('level up!', True, (255, 206, 27))
            self.surface.blit(level_up, (700, 10))

        # 장애물과 충돌(좌표 겹침) -> 게임 오버
        for poo_obj in self.drop_poos:
            if self.pos_x - 45 < poo_obj.x < self.pos_x + 45:
                if self.pos_y - 30 < poo_obj.y + 10 < self.pos_y + 10:
                    text_gameover = Yeongdo_Bold(150).render("Game Over!", True, (255, 0, 0))
                    self.surface.blit(text_gameover, text_gameover.get_rect(center=(450, 250)))
                    self.game_over = True
                    
    def get_result(self):
        '''게임 결과 반환
        이후 랭크 csv 저장에 쓰임'''
        return {
            "user_name": self.user_name,
            "level": self.level,
            "score": self.score
            } 
    
    def handle_event(self, screen, mouse_pos):
        '''다른 화면에서 버튼클릭 감지때문에 실행하는 함수
        (여기선 역할없음, 지우면 오류)'''
        pass
