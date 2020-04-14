# -*- coding: utf-8 -*-
"""
@author: phd_mech
"""

import sys
import time
import numpy as np
import cv2

def decoration(board):
    """
    TEXT
    """
    if not STARTED and not GAMEOVER and not CLEAR:
        cv2.putText(board, str(TURN), (BOARD_WIDTH//2, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, str(SCORE).zfill(3), (50, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "BREAKOUT", (180, BOARD_HEIGHT//2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "DEMO SCREEN", (120, BOARD_HEIGHT//2+100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "ENTER SPACE", (130, BOARD_HEIGHT//2+200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
    if GAMEOVER and not CLEAR:
        cv2.putText(board, str(TURN), (BOARD_WIDTH//2, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, str(SCORE).zfill(3), (50, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "BREAKOUT", (180, BOARD_HEIGHT//2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "GAME OVER", (165, BOARD_HEIGHT//2+100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "ENTER Esc", (180, BOARD_HEIGHT//2+200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
    if CLEAR:
        cv2.putText(board, str(TURN), (BOARD_WIDTH//2, 45),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, str(SCORE).zfill(3), (50, 95),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "CONGRATULATIONS", (70, BOARD_HEIGHT//2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "GAME CLEAR", (165, BOARD_HEIGHT//2+100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.putText(board, "ENTER Esc", (180, BOARD_HEIGHT//2+200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board, "1", (0, 45),
                cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(board, "000", (BOARD_WIDTH//2 + 50, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                2, (255, 255, 255), 2, cv2.LINE_AA)

def mouse_event(event, cursol_x, cursol_y, flags, param):
    """
    MOVE PADDLE
    """
    global PADDLE_X
    x_max = BOARD_WIDTH - PADDLE_WIDTH
    x_min = PADDLE_WIDTH
    if event == cv2.EVENT_MOUSEMOVE:
        if x_min < cursol_x < x_max:
            PADDLE_X = cursol_x
        elif x_max <= cursol_x:
            PADDLE_X = x_max
        elif cursol_x <= x_min:
            PADDLE_X = x_min

def block_table():
    """
    BLOCK INFORMATION
    """
    blocks = []
    for row_i in range(BLOCK_ROW):
        for col_i in range(BLOCK_COL):
            blc_id = row_i//2 # block index
            blc_x = col_i*BLOCK_WIDTH
            blc_y = row_i*BLOCK_HEIGHT + MARGIN
            blc_xl = blc_x + SPACE # left
            blc_yt = blc_y + SPACE # top
            blc_xr = blc_x + BLOCK_WIDTH - SPACE # right
            blc_yb = blc_y + BLOCK_HEIGHT - SPACE # bottom
            upper_left = (blc_xl, blc_yt)  # upper left position
            lower_right = (blc_xr, blc_yb) # lower right position
            blocks.append((blc_id, upper_left, lower_right))
    return blocks

def level_select():
    """
    SELECT LEVEL
    """
    global LEVEL
    hit_num = len(HIT_ID_LEVEL)
    if (hit_num >= 4) and (LEVEL <= 1):
        LEVEL = 1
    if (hit_num >= 12) and (LEVEL <= 2):
        LEVEL = 2
    if 1 in BLC_ID_LEVEL:
        LEVEL = 3
    if 0 in BLC_ID_LEVEL:
        LEVEL = 4

def paddle_size():
    """
    paddle width
    """
    global PADDLE_WIDTH
    if HIT_TOP:
        PADDLE_WIDTH = PADDLE_WIDTH_DEFO//2
    else:
        PADDLE_WIDTH = PADDLE_WIDTH_DEFO

def bounce_and_blocks(board):
    """
    BAUNCE BALL: wall, paddle, blocks
    """
    global HIT_ID_SHOW, BLC_ID_SHOW, HIT_ID_LEVEL, BLC_ID_LEVEL,\
        SCORE, SPEED, BALL_POS, HIT_TOP
    # BALL POSITION
    ball_x_last, ball_y_last = BALL_POS # last
    speed_x, speed_y = SPEED # last
    ball_x_new = ball_x_last + speed_x*POWER # new
    ball_y_new = ball_y_last + speed_y*POWER # new
    # PADDLE POSITION (Bool for game start)
    if STARTED:
        pad_xl = PADDLE_X - PADDLE_WIDTH
        pad_xr = PADDLE_X + PADDLE_WIDTH
    else:
        pad_xl = 0
        pad_xr = BOARD_WIDTH
    # TOP WALL
    # if (ball_y_new <= BALL_RADIUS) or (ball_y_new >= BOARD_HEIGHT - BALL_RADIUS):
    if ball_y_new <= BALL_RADIUS:
        ball_x_new = ball_x_last
        ball_y_new = ball_y_last
        speed_y *= -1
        HIT_TOP = True
    # SIDE WALL
    if (ball_x_new <= BALL_RADIUS) or (ball_x_new >= BOARD_WIDTH - BALL_RADIUS):
        ball_x_new = ball_x_last
        ball_y_new = ball_y_last
        speed_x *= -1
    # PADDLE
    if (pad_xl - BALL_RADIUS <= ball_x_new <= pad_xr + BALL_RADIUS)\
        and (PAD_YT - BALL_RADIUS <= ball_y_new <= PAD_YB + BALL_RADIUS):
        ball_x_new = ball_x_last
        ball_y_new = ball_y_last
        speed_y *= -1
        if STARTED:
            speed_x = 2*(ball_x_new - PADDLE_X)//PADDLE_WIDTH

    # BLOCKS DRAW & BOUNCE
    for blc_i in range(BLOCK_NUM):
        blc_info = BLOCKS[blc_i]
        blc_id = blc_info[0] # 0,1,2,3
        blc_xl, blc_yt = blc_info[1] # upper left
        blc_xr, blc_yb = blc_info[2] # lower right
        if blc_i in HIT_ID_SHOW:
            pass
        else:
            if (blc_xl < ball_x_new < blc_xr)\
                and (blc_yt < ball_y_new < blc_yb):
                if STARTED or GAMEOVER:
                    BLC_ID_SHOW.append(blc_id)
                    HIT_ID_SHOW.append(blc_i)
                    BLC_ID_LEVEL.append(blc_id)
                    HIT_ID_LEVEL.append(blc_i)
                    SCORE += SCORE_TABLE[blc_id]
                    if blc_id == 2:
                        HIT_TOP = False
                ball_x_new = ball_x_last
                ball_y_new = ball_y_last
                speed_y *= -1
            else:
                cv2.rectangle(board,               # image
                              blc_info[1],         # upper left
                              blc_info[2],         # lower right
                              COLOR_TABLE[blc_id], # color
                              -1)                  # thickness
    SPEED = np.array([speed_x, speed_y])
    BALL_POS = (ball_x_new, ball_y_new) # new

def ball(board):
    """
    ball
    """
    cv2.circle(board,           # image
               BALL_POS,        # center
               BALL_RADIUS,     # radius
               (255, 255, 255), # color
               -1,              # thickness
               cv2.LINE_AA)     # linetype

def paddle(board):
    """
    paddle
    """
    if STARTED:
        pad_xl = PADDLE_X - PADDLE_WIDTH
        pad_xr = PADDLE_X + PADDLE_WIDTH
    else:
        pad_xl = 0
        pad_xr = BOARD_WIDTH
    cv2.rectangle(board,            # image
                  (pad_xl, PAD_YT), # upper left
                  (pad_xr, PAD_YB), # lower right
                  (255, 127, 0),    # color
                  -1)               # thickness
    cv2.rectangle(board,            # image
                  (PADDLE_X+5, PAD_YT), # upper left
                  (PADDLE_X-5, PAD_YB), # lower right
                  (0, 0, 255),    # color
                  -1)               # thickness

def game_over():
    """
    game over
    """
    global HIT_ID_LEVEL, BLC_ID_LEVEL, STARTED,\
        BALL_POS, SPEED, TURN, GAMEOVER, POWER, CLEAR
    ball_y = BALL_POS[1]
    if ball_y > BOARD_HEIGHT:
        STARTED = False
        TURN += 1
        BALL_POS = (BALL_X0, BALL_Y0)
        SPEED = np.array((1, 1))
        HIT_ID_LEVEL = []
        BLC_ID_LEVEL = []
        if TURN == 4:
            GAMEOVER = True
            TURN = "CPU"
            SPEED = np.array((4, 4))
            POWER = 1
    if len(HIT_ID_SHOW) == BLOCK_NUM:
        STARTED = False
        GAMEOVER = True
        CLEAR = True

def main():
    """
    MAIN PROGRAMING
    """
    global STARTED, LEVEL, SPEED, POWER, BALL_POS, HIT_TOP
    # WINDOW
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_AUTOSIZE)
    cv2.setMouseCallback(WIN_NAME, mouse_event)
    # INITIAL CONDITIONS
    while True:
        # DEMO SCREEN
        while not STARTED:
            board_demo = np.copy(BOARD)
            decoration(board_demo)
            # BOUNCE & BLOCKS EVENT
            bounce_and_blocks(board_demo)
            # BALL & PADDLE
            ball(board_demo)
            paddle(board_demo)
            cv2.imshow(WIN_NAME, board_demo)
            # KEY EVENT
            key = cv2.waitKey(1)
            # GAME START
            if key == 32 and not GAMEOVER: # space
                STARTED = True
                # Return initial conditions
                BALL_POS = (BALL_X0, BALL_Y0)
                SPEED = np.array((1, 1))
                LEVEL = 0
                HIT_TOP = False
                break
            # EXIT
            if key == 27: # Esc
                cv2.destroyAllWindows()
                sys.exit()
        # UPDATE BOARD
        board_new = np.copy(BOARD)
        # LEVEL SET
        level_select()
        POWER = POWER_TABLE[LEVEL]
        paddle_size()
        # BOUNCE & BLOCKS EVENT
        bounce_and_blocks(board_new)
        game_over()
        # DRAW
        ball(board_new)
        paddle(board_new)
        # TEXT: SCORE & TURN
        timer = round(time.time(), 1)
        dig = float(str(timer).split(".")[1])
        if dig%3 == 0:
            cv2.putText(board_new, str(SCORE).zfill(3),
                        (50, 95), cv2.FONT_HERSHEY_SIMPLEX,
                        2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board_new, str(TURN),
                    (BOARD_WIDTH//2, 45), cv2.FONT_HERSHEY_SIMPLEX,
                    2, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(board_new,
                    "LEVEL={}, COUNT={}, SPEED={}, POWER={}"\
                    .format(LEVEL+1, len(HIT_ID_SHOW), SPEED, POWER),
                    (5, BOARD_HEIGHT-10), cv2.FONT_HERSHEY_SIMPLEX,
                    .8, (255, 255, 255), 1)
        # SHOW BOARD
        decoration(board_new)
        cv2.imshow(WIN_NAME, board_new)
        # KEY EVENT
        key = cv2.waitKey(1)
        # PAUSE
        if key == 32: # Space
            cv2.waitKey(0)
        # EXIT
        elif key == 27: # Esc
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    # PARAMETER
    WIN_NAME = "BREAKOUT"
    STARTED = False
    HIT_TOP = False
    GAMEOVER = False
    CLEAR = False
    SCORE = 0
    TURN = 1
    LEVEL = 0
    SPEED = np.array((1, 1))
    POWER = 2
    POWER_TABLE = (3, # default
                   4, # hit 4
                   5, # hit 12
                   6, # hit orange
                   7) # hit red
    # GAME BOARD INFORMATION
    BOARD_WIDTH = 700
    BOARD_HEIGHT = 700
    BOARD = np.zeros((BOARD_HEIGHT, BOARD_WIDTH, 3), dtype=np.uint8)
    # BALL INFORMATION
    BALL_RADIUS = 5
    BALL_X0 = 6 # initial position
    BALL_Y0 = BOARD_HEIGHT//2 # initial position
    BALL_POS = (BALL_X0, BALL_Y0)
    # PADDLE INFORMATION
    PADDLE_HEIGHT = 12
    PADDLE_WIDTH_DEFO = 30
    PADDLE_WIDTH = PADDLE_WIDTH_DEFO
    PADDLE_X = BOARD_WIDTH//2 # initial position
    PADDLE_Y = BOARD_HEIGHT - 50
    PAD_YT = PADDLE_Y - PADDLE_HEIGHT//2 # top
    PAD_YB = PADDLE_Y + PADDLE_HEIGHT//2 # bottom
    # BLOCK INFORMATION
    BLOCK_COL = 14
    BLOCK_ROW = 8
    BLOCK_HEIGHT = 24
    BLOCK_WIDTH = BOARD_WIDTH//BLOCK_COL
    MARGIN = 100 # upper space
    SPACE = 2 # space between each blocks
    BLOCKS = block_table()
    BLOCK_NUM = len(BLOCKS)
    COLOR_TABLE = ((0, 0, 255),
                   (0, 120, 255),
                   (0, 255, 0),
                   (0, 255, 255))
    SCORE_TABLE = (7, 5, 3, 1)
    HIT_ID_SHOW = []
    BLC_ID_SHOW = []
    HIT_ID_LEVEL = []
    BLC_ID_LEVEL = []
    # MAIN PROGRAM
    main()
