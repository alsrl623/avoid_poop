import pygame, sys
from objects import Button, TextInput
from photo import Photo, Profile
from game import Game
from rank import Rank, Top3

username = ''
gamelevel = 1

def Yeongdo_Bold(size):
    '''폰트 입력을 편하게'''
    return pygame.font.Font("assets/font.ttf", size)

def get_screen():
    '''game.py에 screen 전달'''
    return screen

class ScreenTemplate:
    '''스크린 템플릿'''
    def __init__(self):
        pass # 초기 설정 ex) self.변수, 버튼, 텍스트 등 
    def update(self, screen, mouse_pos):
        pass # 반복 업데이트될 부분
    def handle_event(self, event, mouse_pos):
        pass # pygame.event ex) 키 입력, 마우스 클릭 감지 등

class Main_Screen: 
    '''접속시 보이는 가장 기본 메인 화면'''
    def __init__(self, char_img=None, poo_img=None):
        if char_img == None: # 캐릭터 이미지 변경시
            self.head_img = pygame.image.load("assets/default_char.png")
        else:
            self.head_img = char_img
        if poo_img == None: # 똥 이미지 변경시
            self.poo_img = pygame.image.load("assets/default_poo.png")
        else:
            self.poo_img = poo_img

        btn1_img = pygame.image.load("assets/300x100.png") # 버튼 이미지(300x100 흰 상자)
        btn2_img = pygame.image.load("assets/300x100.png")
        self.main_bg = pygame.image.load("assets/main_background.png") # 배경 이미지 로드

        # 버튼 생성 
        self.button1 = Button(btn1_img, (250,500), '게임방법', Yeongdo_Bold(60), "#000000", "#585858")
        self.button2 = Button(btn2_img, (650,500), '게임시작', Yeongdo_Bold(60), "#000000", "#585858")
        self.btn_list = [self.button1, self.button2] #버튼 여러 개 제어용 리스트

        # 메인 화면의 로고 생성
        self.text_logo = Yeongdo_Bold(167).render("똥 피하기", True, "#644608") 
        self.text_logo_rect = self.text_logo.get_rect(center=(450,230)) # 위치 rect 설정

        # 랭킹 받아오기
        rank_result = Top3('rank_log.csv').result()
        self.rank1_text = Yeongdo_Bold(20).render(rank_result[0], True, (0,0,0))
        self.rank2_text = Yeongdo_Bold(20).render(rank_result[1], True, (0,0,0))
        self.rank3_text = Yeongdo_Bold(20).render(rank_result[2], True, (0,0,0))
        
    def update(self, screen, mouse_pos):
        '''화면 업데이트'''
        # 화면에 표시
        screen.blit(self.main_bg, (0,0)) # 배경 화면
        screen.blit(self.text_logo, self.text_logo_rect) # 로고
        screen.blit(self.rank1_text, (20, 20)) # 랭킹 1,2,3
        screen.blit(self.rank2_text, (20, 60))
        screen.blit(self.rank3_text, (20, 100))

        # 버튼 위 마우스 감지
        for btn in self.btn_list:
            btn.check_hover_button(mouse_pos)
            btn.update(screen)

    def handle_event(self, event, mouse_pos):
        '''이벤트 감지'''
        global current_screen # 현재 화면을 알려 주고 바꾸는 전역 변수

        # 마우스 클릭 감지(좌, 우)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button1.check_button_click(mouse_pos): # 버튼1 -> 게임 방법
                current_screen = Game_Guide()
            elif self.button2.check_button_click(mouse_pos): # 버튼2 -> 프로필 설정
                current_screen = Set_Profile_Screen(self.head_img, self.poo_img)

class Set_Profile_Screen: 
    '''프로필 및 난이도 설정 화면'''
    def __init__(self, char_img, poo_img):
        self.char_img = char_img
        self.poo_img = poo_img

        self.main_bg = pygame.image.load("assets/main_background.png") # 배경 이미지 로드
        self.char_pic_btn_img = pygame.image.load("assets/200x100.png") # 버튼 이미지(200x100 흰 상자)

        # 난이도 버튼 생성
        self.easy_btn_img = pygame.image.load("assets/200x100.png")
        self.normal_btn_img = pygame.image.load("assets/200x100.png")
        self.hard_btn_img = pygame.image.load("assets/200x100.png")
        self.easy_btn = Button(self.easy_btn_img, (225, 600), 'easy', Yeongdo_Bold(60), "#000000", '#585858')
        self.normal_btn = Button(self.normal_btn_img, (450, 600), 'normal', Yeongdo_Bold(60), '#000000', '#585858')
        self.hard_btn = Button(self.hard_btn_img, (675, 600), 'hard', Yeongdo_Bold(60), '#000000', '#585858')
        self.char_pic_btn = Button(self.char_pic_btn_img, (225, 450), '사진 촬영', Yeongdo_Bold(50), '#000000', '#585858')
        self.btn_list = [self.char_pic_btn, self.easy_btn, self.normal_btn, self.hard_btn]
        
        # 닉네임 입력 (object.py 참고)
        self.text_input = TextInput(575, 425, 200, 50, Yeongdo_Bold(30), placeholder='닉네임 입력', max_length=11)
        self.text_logo = Yeongdo_Bold(167).render("똥 피하기", True, "#644608") # 로고
        self.char_img_rect = self.char_img.get_rect(center=(450, 450)) # 캐릭터 사진 rect
        self.text_logo_rect = self.text_logo.get_rect(center=(450,230)) # 로고 rect
        
    def update(self, screen, mouse_pos):
        '''업데이트'''
        # 화면에 표시
        screen.blit(self.main_bg, (0,0)) # 배경 화면
        screen.blit(self.char_img, self.char_img_rect) # 캐릭터
        screen.blit(self.text_logo, self.text_logo_rect) # 로고
        self.text_input.draw(screen) # text_input

        # 버튼 위 마우스 감지
        for btn in self.btn_list:
            btn.check_hover_button(mouse_pos)
            btn.update(screen)

    def handle_event(self, event, mouse_pos):
        '''이벤트 감지'''
        global username, gamelevel
        global current_screen
        self.text_input.handle_event(event)

        # 마우스 클릭 감지
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.char_pic_btn.check_button_click(mouse_pos): # 사진 버튼 -> 사진 촬영
                self.char_img_ts = Photo.take_picture(' ', 'ts') # 결과를 타임스탬프(파일이름)로
                if self.char_img_ts == None: #사진 안 찍히면 뒷 코드 실행 방지
                    return
                self.char_img = pygame.image.load(f"image/full/{self.char_img_ts}.png") # 캐릭터 전신 합본

            elif self.easy_btn.check_button_click(mouse_pos): # 하 난이도 버튼 -> (닉네임 확인 ->) 게임 시작
                gamelevel = 1
                username = self.text_input.get_value() # 유저 네임 입력받은대로 지정
                if len(username) < 1: # 닉네임 입력 안 되어있을 시 느낌표로 경고
                    self.text_input.add_placeholder('!')
                    return
                user_profile = Profile(username, self.char_img, gamelevel)
                current_screen = Game(user_profile, get_screen(), self.char_img)
                
            elif self.normal_btn.check_button_click(mouse_pos): # 중 난이도
                gamelevel = 2
                username = self.text_input.get_value()
                if len(username) < 1:
                    self.text_input.add_placeholder('!')
                    return
                user_profile = Profile(username, self.char_img, gamelevel)
                current_screen = Game(user_profile, get_screen(), self.char_img)

            elif self.hard_btn.check_button_click(mouse_pos): # 고 난이도
                gamelevel = 3
                username = self.text_input.get_value()
                if len(username) < 1:
                    self.text_input.add_placeholder('!')
                    return
                user_profile = Profile(username, self.char_img, gamelevel)
                current_screen = Game(user_profile, get_screen(), self.char_img)

class Game_Guide:
    '''게임 방법 설명 화면'''
    def __init__(self):
        # 버튼 생성
        self.back_btn_img = pygame.image.load("assets/300x100.png") # 돌아가기 버튼
        self.img = pygame.image.load("assets/game_guide.jpg") # 게임 설명 화면 로드
        self.img_rect = self.img.get_rect(center=(450,350))
        self.back_btn = Button(self.back_btn_img, (450,600), '돌아가기', Yeongdo_Bold(40), "#000000", "#585858")
        self.btn_list = [self.back_btn]

    def update(self, screen, mouse_pos):
        '''화면 업데이트'''
        # 화면에 표시
        screen.blit(self.img, self.img_rect)

        # 버튼 위 마우스 감지
        for btn in self.btn_list:
            btn.check_hover_button(mouse_pos)
            btn.update(screen)

    def handle_event(self, event, mouse_pos):
        '''이벤트 감지'''
        global current_screen

        # 마우스 클릭 감지
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_btn.check_button_click(mouse_pos): # 돌아가기 버튼 -> 메인 화면
                current_screen = Main_Screen()

class Score_screen:
    '''아웃트로 화면'''
    def __init__(self, result, char_img):
        self.char_img = char_img
        self.score = result['score']
        self.username = result['user_name']
        self.level = result['level']
        
        # 점수 저장
        Rank(self.username, self.level, self.score).to_csv()
        self.text = Yeongdo_Bold(50).render(f'name : {self.username}, level : {self.level}, score : {self.score}', True, '#000000')

        # 버튼 생성
        btn1_img = pygame.image.load("assets/300x100.png")
        btn2_img = pygame.image.load("assets/300x100.png")
        self.main_bg = pygame.image.load("assets/main_background.png")
        self.button1 = Button(btn1_img, (250,500), '게임 재시작', Yeongdo_Bold(60), "#000000", "#585858")
        self.button2 = Button(btn2_img, (650,500), '메인화면', Yeongdo_Bold(60), "#000000", "#585858")
        self.btn_list = [self.button1, self.button2]

    def update(self, screen, mouse_pos):
        '''화면 업데이트'''
        # 화면에 표시
        screen.blit(self.text, (100,300)) # 점수 정보

        # 버튼 위 마우스 감지
        for btn in self.btn_list:
            btn.check_hover_button(mouse_pos)
            btn.update(screen)

    def handle_event(self, event, mouse_pos):
        '''이벤트 감지'''
        global current_screen

        # 마우스 클릭 감지
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.button1.check_button_click(mouse_pos): # 재시작 버튼 -> 동일 프로필로 게임 재시작
                user_profile = Profile(self.username, self.char_img, gamelevel)
                current_screen = Game(user_profile, screen, self.char_img)
            elif self.button2.check_button_click(mouse_pos): # 메인화면 버튼 -> 메인화면으로 이동
                current_screen = Main_Screen()


if __name__ == '__main__': # import 시 실행 방지
    '''초기화'''
    pygame.init()
    pygame.display.set_caption('똥 피하기') # 창 이름
    screen = pygame.display.set_mode((900, 700)) # 창 사이즈
    clock = pygame.time.Clock() # 아래에서 60 프레임 제한
    current_screen = Main_Screen() # 메인 화면으로 시작

    while True:
        mouse_pos = pygame.mouse.get_pos() # 마우스 현재 위치
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # 창의 x 클릭 시 종료
                pygame.quit()
                exit()
            current_screen.handle_event(event, mouse_pos) # 화면 클래스의 이벤트 감지 모듈

        current_screen.update(screen, mouse_pos) # 화면 클래스의 업데이트 모듈
        pygame.display.update() # 화면 업데이트
        clock.tick(60)

        '''게임오버 감지'''
        if isinstance(current_screen, Game) and current_screen.game_over:
            result = current_screen.get_result()
            current_screen = Score_screen(result, current_screen.char_img)

