import pygame
import time
import sys

import easy
import hard
import normal

pygame.init()

black = (0, 0, 0)
white = (255, 255, 255)

bg_img = pygame.image.load("image/main_racoon.png")

easy_img = pygame.image.load("image/easy.png")
normal_img = pygame.image.load("image/normal.png")
hard_img = pygame.image.load("image/hard.png")
quit_img = pygame.image.load("image/quit.png")

click_easy_img = pygame.image.load("image/click_easy.png")
click_normal_img = pygame.image.load("image/click_normal.png")
click_hard_img = pygame.image.load("image/click_hard.png")
click_quit_img = pygame.image.load("image/click_quit.png")

display_width = 640
display_height = 480
game_display = pygame.display.set_mode((display_width, display_height))

# pygame 타이틀 이름 지정
pygame.display.set_caption('A racoon trick')

# pygame 아이콘 이미지 변경
racoon_image = pygame.image.load('image/icon_racoon.png')
pygame.display.set_icon(racoon_image)

# ?
clock = pygame.time.Clock()


class c_button:
    def __init__(self, img_in, x, y, width, height, img_act, x_act, y_act, action=None):
        mouse = pygame.mouse.get_pos()  # 마우스 좌표 저장
        click = pygame.mouse.get_pressed()  # 클릭 시
        # 마우스가 해당 이미지 안에 있으면
        if x + width > mouse[0] > x and y + height > mouse[1] > y:
            # 클릭 이미지 불러오기
            game_display.blit(img_act, (x_act, y_act))
            if click[0] and action != None:
                time.sleep(0.1)  # 지연 시간
                action()  # 지정 함수 호출
        else:
            game_display.blit(img_in, (x, y))  # 마우스가 이미지 밖에 있으면 이미지 불러오기


# 클릭 시 게임 종료
def quit_game():
    pygame.quit()
    sys.exit()


# 클릭 시 easy 실행
def easy_level():
    easy.main()


# 클릭 시 normal 실행
def nomal_level():
    normal.main()


# 클릭 시 hard 실행
def hard_level():
    hard.main()


def main():
    menu = True

    # 음악 지정, pygame.mixer.music.play(숫자,0,0) : 숫자가 -1이면 반복 재생
    pygame.mixer.init()
    pygame.mixer.music.load("sound/menu.mp3")
    pygame.mixer.music.play(-1, 0.0)

    font_style = pygame.font.Font('font/LeeSeoyun.ttf', 60)

    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        title_text = font_style.render("[ A racoon trick ]", True, black)

        game_display.blit(bg_img, (0, 0))
        game_display.blit(title_text, (85, 100))

        easy_button = c_button(easy_img, 100, 200, 120, 60, click_easy_img, 100, 200, easy_level)
        normal_button = c_button(normal_img, 260, 200, 120, 60, click_normal_img, 260, 200, nomal_level)
        hard_button = c_button(hard_img, 420, 200, 120, 60, click_hard_img, 420, 200, hard_level)
        quit_button = c_button(quit_img, 260, 310, 120, 60, click_quit_img, 260, 310, quit_game)

        pygame.display.update()
        # 일정 주기로 화면 갱신, 화면 전환 프레임 설정
        clock.tick(5)


main()
