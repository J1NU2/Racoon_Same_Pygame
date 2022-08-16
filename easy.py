import random

import pygame
import sys
from pygame.locals import *
from time import sleep

# 전역 변수들
FPS = 30  # 화면 갱신 속도(30ms)
WINDOWWIDTH = 640  # 화면 가로 크기
WINDOWHEIGHT = 480  # 화면 세로 크기
REVEALSPEED = 5  # 그림을 보여주는 속도(높을수록 빠름)
BOXSIZE = 60  # 그림 박스 크기
GAPSIZE = 10  # 그림 박스 간 간격
# 박스의 총 갯수 조절 가능 (easy:5,4 / normal:6,5 / hard:7,6)
BOARDWIDTH = 5  # 그림 박스 가로 크기
BOARDHEIGHT = 4  # 그림 박스 세로 크기
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)  # 좌우 간격
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)  # 상하 간격

# RGB 색상
BLACK = (0, 0, 0)
WIHTE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 36, 36)
YELLOW = (255, 255, 36)

BGIMAGE = pygame.image.load("image/easy_racoon.png")
WONIMAGE1 = pygame.image.load("image/won_racoon1.png")
WONIMAGE2 = pygame.image.load("image/won_racoon2.png")
LOSEIMAGE1 = pygame.image.load("image/lose_racoon1.png")
LOSEIMAGE2 = pygame.image.load("image/lose_racoon2.png")
BOXCOLOR = BLACK  # 그림 박스 색상
HIGHLIGHTCOLOR = BLUE  # 선택된 박스 테두리 색상

# 해당 요소들의 순서르 random.shuffle로 섞어버린다.
ALLPICTURE = ['racoon1', 'racoon2', 'racoon3', 'racoon4',
              'racoon5', 'racoon6', 'racoon7', 'racoon8',
              'racoon9', 'racoon10', 'racoon11', 'racoon12',
              'racoon13', 'racoon14', 'racoon15', 'racoon16',
              'racoon17', 'racoon18', 'racoon19', 'racoon20', 'racoon21']


# 게임 보드 그리기
def draw_Board(board, revealed):
    # 모든 상자를 상태에 맞추어 그리기
    # BOARDWIDTH 값만큼 실행
    for boxx in range(BOARDWIDTH):
        # BOARDHEIGHT 값만큼 실행
        for boxy in range(BOARDHEIGHT):
            # left_Top_Coords_Of_Box의 boxx, boxy에 left, top 순서로 값을 집어넣음
            left, top = left_Top_Coords_Of_Box(boxx, boxy)
            if not revealed[boxx][boxy]:
                # 닫힌 상자
                pygame.draw.rect(DISPLAY, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # 열린 상자
                pic, num = get_Pic_And_Num(board, boxx, boxy)
                draw_Card(pic, num, boxx, boxy)


# 박스 섞기
def get_Randomized_Board():  # 무작위 박스 생성
    global ALLPICTURE
    cards = []  # cards 이라는 리스트의 형태 지정
    for pic in ALLPICTURE:
        for num in range(1, 2):
            # ALLPICTURE에서 1.1번 1.2번 형태로 나눈다
            # cards (shape,color) 형태로 추가
            cards.append((pic, num))

    random.shuffle(cards)  # 해당 리스트의 항목들을 랜덤으로 섞기
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2)  # 그림 박스 가로*세로 / 2 를 정수 형태로 저장
    cards = cards[:numIconsUsed] * 2  # numIconsUsed번째 까지의 값에 x2 한 값을 다시 저장
    random.shuffle(cards)  # 해당 리스트의 항목들을 랜덤으로 섞기

    # 게임 판 만들기
    board = []  # board 라는 리스트의 형태 지정
    for x in range(BOARDWIDTH):  # BOARDWIDTH 값만큼 실행
        column = []  # column 이라는 리스트의 형태 지정
        for y in range(BOARDHEIGHT):  # BOARDHEIGHT 값만큼 실행
            column.append(cards[0])  # column 리스트에 cards 0번째 값을 추가
            del cards[0]  # cards 리스트에 담긴 한개의 요소 삭제, 추가한 아이콘 삭제
        board.append(column)  # board 리스트에 column 값을 추가
    return board  # board 값을 다시 받게끔 설정


# 열려있는 박스 만들기
def generate_Revealed_Boxes_Data(val):  # 이미지 노출 함수
    revealedBoxes = []  # revealedBoxes 라는 리스트 생성
    for i in range(BOARDWIDTH):  # BOARDWIDTH 값만큼 실행
        revealedBoxes.append([val] * BOARDHEIGHT)
    return revealedBoxes


# 박스 좌표
def left_Top_Coords_Of_Box(boxx, boxy):  # 박스 간격 지정 함수
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)  # boxx와 boxy에 left와 top의 값을 저장


# 게임 시작 애니메이션
def start_Game_Animation(board):  # 애니메이션이 시작되도록 함수 지정 : main_Game_Start()에서 호출
    # 랜덤으로 상자를 열어서 잠깐 보여준다.
    coveredBoxes = generate_Revealed_Boxes_Data(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    boxGroups = split_Into_Groups_Of(8, boxes)

    draw_Board(board, coveredBoxes)
    for boxGroup in boxGroups:
        # 보였다가 안보였다 해주는 함수 지정
        reveal_Boxes_Animation(board, boxGroup)
        cover_Boxes_Animation(board, boxGroup)


# 퍼즐 그룹
def split_Into_Groups_Of(groupSize, theList):
    # 2차원 리스트 생성, 최대 groupSize만큼의 요소 포함
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


# 박스 열기 애니메이션
def reveal_Boxes_Animation(board, boxesToReveal):  # 보였다가 안보였다가 해주는 함수
    # 숫자 변경 시 보여주는 속도 조절 가능
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_Box_Covers(board, boxesToReveal, coverage)


# 박스 닫기 애니메이션
def cover_Boxes_Animation(board, boxesToCover):  # 보였다가 안보였다가 해주는 함수
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_Box_Covers(board, boxesToCover, coverage)


# 박스 커버 그리기
def draw_Box_Covers(board, boxes, coverage):
    # 닫히거나 열린 상태의 상자를 그린다.
    # 상자는 요소 2개를 가진 리스트의 형태이며, x와 y 위치를 가진다.
    for box in boxes:
        left, top = left_Top_Coords_Of_Box(box[0], box[1])
        pygame.draw.rect(DISPLAY, BLACK, (left, top, BOXSIZE, BOXSIZE))
        pic, num = get_Pic_And_Num(board, box[0], box[1])
        draw_Card(pic, num, box[0], box[1])
        if coverage > 0:  # 닫힌 상태라면, 덮개만 덮혀있다.
            pygame.draw.rect(DISPLAY, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


# 박스 이미지 그리기
def draw_Card(pic, num, boxx, boxy):  # 결정된 모양과 색상으로 이미지를 그리는 함수
    eight = int(BOXSIZE * 0.01)

    # left_Top_Coords_Of_Box의 boxx, boxy에 left, top 순서로 값을 집어넣음
    left, top = left_Top_Coords_Of_Box(boxx, boxy)

    racoon1Img = pygame.image.load('image/racoon1.png')
    racoon2Img = pygame.image.load('image/racoon2.png')
    racoon3Img = pygame.image.load('image/racoon3.png')
    racoon4Img = pygame.image.load('image/racoon4.png')
    racoon5Img = pygame.image.load('image/racoon5.png')
    racoon6Img = pygame.image.load('image/racoon6.png')
    racoon7Img = pygame.image.load('image/racoon7.png')
    racoon8Img = pygame.image.load('image/racoon8.png')
    racoon9Img = pygame.image.load('image/racoon9.png')
    racoon10Img = pygame.image.load('image/racoon10.png')
    racoon11Img = pygame.image.load('image/racoon11.png')
    racoon12Img = pygame.image.load('image/racoon12.png')
    racoon13Img = pygame.image.load('image/racoon13.png')
    racoon14Img = pygame.image.load('image/racoon14.png')
    racoon15Img = pygame.image.load('image/racoon15.png')
    racoon16Img = pygame.image.load('image/racoon16.png')
    racoon17Img = pygame.image.load('image/racoon17.png')
    racoon18Img = pygame.image.load('image/racoon18.png')
    racoon19Img = pygame.image.load('image/racoon19.png')
    racoon20Img = pygame.image.load('image/racoon20.png')
    racoon21Img = pygame.image.load('image/racoon21.png')

    if pic == 'racoon1':
        DISPLAY.blit(racoon1Img, (left + eight, top + eight))
    elif pic == 'racoon2':
        DISPLAY.blit(racoon2Img, (left + eight, top + eight))
    elif pic == 'racoon3':
        DISPLAY.blit(racoon3Img, (left + eight, top + eight))
    elif pic == 'racoon4':
        DISPLAY.blit(racoon4Img, (left + eight, top + eight))
    elif pic == 'racoon5':
        DISPLAY.blit(racoon5Img, (left + eight, top + eight))
    elif pic == 'racoon6':
        DISPLAY.blit(racoon6Img, (left + eight, top + eight))
    elif pic == 'racoon7':
        DISPLAY.blit(racoon7Img, (left + eight, top + eight))
    elif pic == 'racoon8':
        DISPLAY.blit(racoon8Img, (left + eight, top + eight))
    elif pic == 'racoon9':
        DISPLAY.blit(racoon9Img, (left + eight, top + eight))
    elif pic == 'racoon10':
        DISPLAY.blit(racoon10Img, (left + eight, top + eight))
    elif pic == 'racoon11':
        DISPLAY.blit(racoon11Img, (left + eight, top + eight))
    elif pic == 'racoon12':
        DISPLAY.blit(racoon12Img, (left + eight, top + eight))
    elif pic == 'racoon13':
        DISPLAY.blit(racoon13Img, (left + eight, top + eight))
    elif pic == 'racoon14':
        DISPLAY.blit(racoon14Img, (left + eight, top + eight))
    elif pic == 'racoon15':
        DISPLAY.blit(racoon15Img, (left + eight, top + eight))
    elif pic == 'racoon16':
        DISPLAY.blit(racoon16Img, (left + eight, top + eight))
    elif pic == 'racoon17':
        DISPLAY.blit(racoon17Img, (left + eight, top + eight))
    elif pic == 'racoon18':
        DISPLAY.blit(racoon18Img, (left + eight, top + eight))
    elif pic == 'racoon19':
        DISPLAY.blit(racoon19Img, (left + eight, top + eight))
    elif pic == 'racoon20':
        DISPLAY.blit(racoon20Img, (left + eight, top + eight))
    elif pic == 'racoon21':
        DISPLAY.blit(racoon21Img, (left + eight, top + eight))


# 모양과 색상 가져오기
def get_Pic_And_Num(board, boxx, boxy):  # 그림의 모양과 색상 결정
    # 아이콘 값은 board[x][y][0]
    # 색깔 값은 board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


# 박스 좌표 얻기
def get_Box_At_Pixel(x, y):  # 박스의 픽셀 값을 얻는 함수
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = left_Top_Coords_Of_Box(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


# 박스에 마우스를 올리면 하이라이트 박스 생성
def draw_Highlight_Box(boxx, boxy):  # 박스에 마우스를 올리면, 하이라이트 박스 그리기 함수
    left, top = left_Top_Coords_Of_Box(boxx, boxy)
    # pygame.draw.rect(Surface,color,Rect,Width=0: 사각형을 그려주는 함수
    # Surface : pygame 실행 시 전체적으로 화면을 선언한 변수 값
    # color : 사각형의 색깔
    # Rect : 사각형의 (x축,y축,가로,세로)
    # Width : 기본적으로 0, 사각형 테두리의 굵기
    pygame.draw.rect(DISPLAY, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


# 게임에서 이겼을 때 화면 전환
def game_Won_Animation(board):
    wimage1 = WONIMAGE1
    wimage2 = WONIMAGE2

    for i in range(9):
        wimage1, wimage2 = wimage2, wimage1
        DISPLAY.blit(wimage1, (0, 0))
        pygame.display.update()
        pygame.time.wait(500)


# 게임에서 졌을 때 화면 전환
def game_Lose_Animation(board):
    limage1 = LOSEIMAGE1
    limage2 = LOSEIMAGE2

    for i in range(9):
        limage1, limage2 = limage2, limage1
        DISPLAY.blit(limage1, (0, 0))
        pygame.display.update()
        pygame.time.wait(500)


# 게임 Clear 함수
def game_clear():
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    font_clear = pygame.font.Font('font/LeeSeoyun.ttf', 70)
    font_after = pygame.font.Font('font/LeeSeoyun.ttf', 50)

    clear_message = font_clear.render("Game Clear!!", True, YELLOW)
    next_message = font_after.render("End after 5 seconds.", True, YELLOW)

    DISPLAY.blit(WONIMAGE2, (0, 0))
    DISPLAY.blit(clear_message, (120, 140))
    DISPLAY.blit(next_message, (75, 220))

    pygame.display.update()
    sleep(5)

    pygame.quit()
    sys.exit()

# 게임 Over 함수
def game_over():
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    font_clear = pygame.font.Font('font/LeeSeoyun.ttf', 70)
    font_after = pygame.font.Font('font/LeeSeoyun.ttf', 50)

    clear_message = font_clear.render("Game Over.", True, RED)
    next_message = font_after.render("End after 5 seconds.", True, RED)

    DISPLAY.blit(LOSEIMAGE2, (0, 0))
    DISPLAY.blit(clear_message, (140, 140))
    DISPLAY.blit(next_message, (75, 220))

    pygame.display.update()
    sleep(5)

    pygame.quit()
    sys.exit()


# 이미지 고정
def has_Won(revealedBoxes):
    # 모든 상자가 열리면 True, 아니면 False
    for i in revealedBoxes:
        if False in i:
            return False
    return True


# 메인 함수
def main():
    global FPSCLOCK, DISPLAY
    pygame.init()

    # 게임 시작 시 음악 재생
    pygame.mixer.init()
    pygame.mixer.music.load("sound/easy.mp3")
    pygame.mixer.music.play(-1, 0.0)

    FPSCLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    FONT = pygame.font.Font('font/LeeSeoyun.ttf', 30)

    # 마우스 좌표 저장
    mousex = 0
    mousey = 0

    # 게임 타이틀 제목
    pygame.display.set_caption('A racoon trick')

    # 맞췄을 때(Success), 틀렸을 때(Fail) 점수 설정, 초기값 0
    Success = 0
    Fail = 0

    # pygame 아이콘 이미지 변경
    racoon_image = pygame.image.load('image/icon_racoon.png')
    pygame.display.set_icon(racoon_image)

    mainBoard = get_Randomized_Board()
    revealedBoxes = generate_Revealed_Boxes_Data(False)

    firstSelection = None  # 첫 클릭 좌표 저장

    DISPLAY.blit(BGIMAGE, (0, 0))
    start_Game_Animation(mainBoard)

    while_true = True

    while (while_true):  # 게임 루프(Game Loof)
        mouseClicked = False

        DISPLAY.blit(BGIMAGE, (0, 0))
        draw_Board(mainBoard, revealedBoxes)

        message_Success = FONT.render("Success : {} / 10".format(Success), True, BLACK)
        message_Fail = FONT.render("Fail : {} / 15".format(Fail), True, BLACK)

        DISPLAY.blit(message_Success, (5, 2))
        DISPLAY.blit(message_Fail, (5, 32))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        boxx, boxy = get_Box_At_Pixel(mousex, mousey)

        if boxx != None and boxy != None:
            # 마우스가 현재 박스 위에 있을 시
            if not revealedBoxes[boxx][boxy]:  # 닫힌 상자라면 하이라이트만 표시
                draw_Highlight_Box(boxx, boxy)
            if not revealedBoxes[boxx][boxy] and mouseClicked:
                reveal_Boxes_Animation(mainBoard, [(boxx, boxy)])
                revealedBoxes[boxx][boxy] = True  # 닫힌 상자를 클릭하면 > 박스를 열기
                if firstSelection == None:  # 첫번째 클릭이 비어있으면, 1번 박스 좌표 기록
                    firstSelection = (boxx, boxy)  # 박스 좌표를 저장
                else:  # 첫번째와 두번째 클릭의 모양과 색상을 저장
                    # 1번 박스와 2번 박스의 짝 검사
                    icon1shape, icon1color = get_Pic_And_Num(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = get_Pic_And_Num(mainBoard, boxx, boxy)

                    # 만약 색상과 모양의 값이 서로 다르다면? 서로 다르니 둘 다 닫기
                    if icon1shape != icon2shape or icon1color != icon2color:
                        pygame.time.wait(500)  # 0.5초 후
                        # 박스를 덮는다.
                        cover_Boxes_Animation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        # 선택된 첫번째와 두번째 박스를 닫는다.
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False
                        revealedBoxes[boxx][boxy] = False

                        # Fail 점수 추가
                        Fail += 1
                        # Fail의 값이 10일 경우
                        if Fail == 15:
                            game_Lose_Animation(mainBoard)
                            game_over()

                    # 만약 색상과 컬러 모두 같을 경우? Success 점수 추가
                    # or로 설정 시 모양이나 색상이 같아도 점수가 추가됐었음 > and로 바꾸니 해결
                    if icon1shape == icon2shape and icon1color == icon2color:
                        pygame.time.wait(500)  # 0.5초 후
                        Success += 1
                        # Success의 값이 10일 경우
                        if Success == 10:
                            game_Won_Animation(mainBoard)
                            game_clear()

                    firstSelection = None  # 첫번째 클릭 초기화, 1번 박스 리셋

        # 화면을 다시 그린 뒤 다음 판의 시간이 지연되는 것을 기다린다.
        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()  # 메인 함수 호출
