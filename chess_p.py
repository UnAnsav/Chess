from stockfish import Stockfish
from selenium import webdriver
from time import sleep
import chess as chess_lb
import pyautogui as pg
import numpy as np
from bs4 import BeautifulSoup as bs


def rn(number):
    while number % 10 != 0:
        number -= 1

    return number

def number_to_letter(number):   # 11 -> a1
    minus = str(number - rn(number))
    number = rn(number)

    letters = {
        10: "a",
        20: "b",
        30: "c",
        40: "d",
        50: "e",
        60: "f",
        70: "g",
        80: "h",
    }

    number = letters[number] + minus

    return number

def letter_to_number(letter):   # e4 -> 54

    letters = {
        10: "a",
        20: "b",
        30: "c",
        40: "d",
        50: "e",
        60: "f",
        70: "g",
        80: "h",
    }

    for i in range(10, len(letters) * 10 + 10, 10):
        if letters[i] == letter[0]:
            letter = str(i)[0] + letter[-1]


    return int(letter)


def new_move(array1, array2, stockfish = None):
    new_fish = stockfish
    print("\n     start arrays: "); print("last: ", array1); print("now: ", array2)
    bug = 0

    new_1 = []
    new_2 = []

    # first
    for i in array1:
        if i not in array2:
            new_1.append(i)
    # second
    for j in array2:
        if j not in array1:
            new_2.append(j)
    
    array1 = new_1
    array2 = new_2 

    print("end two arrays: "); print(array1); print(array2)

    if len(array1) == 2 and len(array2) == 2:   # если была рокировка
        for i in range(len(array1)):
            if array1[i] == 81 or array1[i] == 61 or array1[i] == 31 or array1[i] == 41:
                del array1[i]
        for i in range(len(array2)):
            if array2[i] == 81 or array2[i] == 61 or array2[i] == 31 or array2[i] == 41:
                del array2[i]

    '''
    for i in range(len(array1)):
        #print(array1); print("a2:", array2)
        try:
            if array1[i] in array2:
                    
                # удаляем фигуры, которыми не был сделан ход
                #del array1[i]        # удаляем в первом массиве
                for j in range(len(array2)):    # удаляем во втором массиве
                    if array2[j] == array1[i]:
                        del array2[j]
                        #print("delete in array2")
                        break

                del array1[i]        # удаляем в первом массиве
                #print("delete in array1")
                        
                #print(array1); print(array2); print()
                
        except Exception as ex:
            #print('exept in new_move: ', ex)
            pass'''


    # return answer
    if len(array1) == 2 and len(array2) == 0:
        print(array1, array2)
        return array1[0], array1[1]
    if len(array1) == 2 and len(array2) == 1:
        bug += 1

        if bug > 3:
            print(array1, array2)
            return array1[0], array2[0]
        
    if len(array1) == 1 and len(array2) == 0:   # если одна фигура съела другую и клеточек стало меньше
        html = driver.page_source
        soup = bs(html, "html.parser")

        all_moves = soup.find_all("div", class_="black node selected")     # p-programms__item_has-player
        for m in all_moves:
            last_mv = m.text[-2:]

        

        try:
            last_mv = letter_to_number(last_mv)

            print("last eat mv: ", last_mv)

            n = int(last_mv)
            return array1[0], last_mv

        except ValueError:
            '''
            last_mv.replace("+", "1")
            while True:
                print("searching last mv: ", last_mv)
                if new_fish.is_move_correct(letter_to_number(array1[0])+last_mv) == True and chess_lb.Board(new_fish.make_moves_from_current_position([array1[0]+last_mv]).get_fen_position() ).is_check == True:
                    return array1[0], last_mv
                else:
                    last_mv[-1] =  int(last_mv[-1]) + 1
            '''

            return array1[0], letter_to_number(m.text[-3:-1])

    if array2 == [38, 48] or array2 == [48, 38] and len(array1) == 2:       # if black king make 0-0-0
        print("рокировка длин")
        return 58, 38

    elif array2 == [68, 78] or array2 == [78, 68] and len(array1) == 2:     # if black king make 0-0
        print("рокировка коротк")
        return 58, 78

    if len(array1) == 1 and len(array2) == 1:
        return array1[0], array2[0]
    
    #print("end two arrays: "); print(array1); print(array2)

    #return array1[0], array2[0]

# open driver    
driver = webdriver.Firefox()
print("driver complate")
driver.get("https://chess.com/play/computer")

def get_figures():
    global driver

    # получаем расположение фигур
    html = str(driver.page_source).split("<!--/Effects-->")[2].split("<!--/Pieces-->")[0].split("</div>', '<!--/Custom Items-->")[0]
    #print("html: ", html)

    moves = html.split("class=")
    new_moves = []
    for i in range(len(moves)):
        try:
            new_moves.append(int(moves[i][-24:-22])) 
        except:
            pass
    
    moves = new_moves
    

    #print("moves: ", moves)

    return moves


def see_fields():
    i = input("input down left corner: ")
    dl = pg.position()
    i = input("input up left corner: ")
    ul = pg.position()
    i = input("input up right corner: ")
    ur = pg.position()
    i = input("input down right corner: ")
    dr = pg.position()

    letters = "abcdefgh"
    numbers = "12345678"

    arrays = []
    for i in range(9):
        arrays.append([])
  
    line = -1
    for k in range(0,  (ul[1] - dl[1]) + int( (ul[1] - dl[1]) / 7),   int( (ul[1] - dl[1]) / 7) ):
        line += 1
        for i in range(0,  (dr[0] - dl[0]) + int( (dr[0] - dl[0]) / 7),   int( (dr[0] - dl[0]) / 7) ):     # first line
            arrays[line].append(   [ dl[0] + i, dl[1] + k ]   )

    #print(arrays)

    for i in arrays:
        print(i, "\n")
    print("len: ", len(arrays))

    return arrays



# stockfish
stockfish = Stockfish(r"C:\Python\best_programm\chess\stockfish\stockfish_14_x64.exe", parameters={"Write Debug Log": True, "UCI_Chess960": True})
stockfish.set_skill_level(95)
print("stockfish complate")

fields = see_fields()

# srart
color = input("input your chess color(black/white): ")

if color == "white":
    while True:
    
        
        print("computer started thinking")
        best_move = stockfish.get_best_move_time(5000)          # stockfish.get_best_move()       # get the best move
        print("BEST MOVE: ", best_move)        

        moves = get_figures()       # get start
        #print("\n moves: ", moves)
        
        # delete my move on desk
        stop = False
        d = 0
        while stop == False:
            if d > 40:
                stop = True
                break

            print("try delete move ", letter_to_number(best_move[:2]))

            
            if best_move == "e1g1":     # если была коротка рокировка
                print("make 0-0")
                d += 1
                for i in range(len(moves)):
                    if moves[i] == 51:      # удаляем короля
                        del moves[i]
                        moves.append(71)
                for i in range(len(moves)):     # удаляем ладью
                    if moves[i] == 81:
                        del moves[i]
                        moves.append(61); 

                stop = True
                break

            elif best_move == "e1c1":       # 0-0-0
                print("make 0-0-0")
                d += 1
                for i in range(len(moves)):
                    if moves[i] == 51:      # удаляем короля
                        del moves[i]
                        moves.append(31)
                for i in range(len(moves)):     # удаляем ладью
                    if moves[i] == 11:
                        del moves[i]
                        moves.append(41)

                stop = True
                break

            else:
                print("make move")
                d += 1
                try:
                    for i in range(len(moves)):     # delete my move
                        if moves[i] == letter_to_number(best_move[:2]):
                            del moves[i]
                            moves.append( letter_to_number(best_move[-2:]) )

                            stop = True 
                            break
                    
                except Exception as ex:
                    print("except in delete my move: ", ex)

        print("my move complate")


        # make my move
        stockfish.make_moves_from_current_position([best_move])

        # take move
        to = int(  str(letter_to_number(best_move[:2]))[0]  ) - 1
        fr = int(  str(letter_to_number(best_move[:2]))[1]  ) - 1
        #print(f"from: {fr}; to: {to}")
        pg.click(fields[fr][to][0], fields[fr][to][1])
        sleep(0.5)
        to = int(  str(letter_to_number(best_move[-2:]))[0]  ) - 1
        fr = int(  str(letter_to_number(best_move[-2:]))[1]  ) - 1
        #print(f"from: {fr}; to: {to}")
        pg.click(fields[fr][to][0], fields[fr][to][1])

        # next (if I and enemy made moves)
        #next = input("complate? ")
        sleep(8)
        
        #########################
        # получаем новое расположение фигур с учётом хода соперника
        last_moves = moves
        moves = get_figures()
        
        try:
            # find enemy's move
            fr, to = new_move(last_moves, moves)
            mv = (number_to_letter(fr) + number_to_letter(to))
            print("enemy move: ", mv)
            # make enemy move
            stockfish.make_moves_from_current_position([mv])
        except TypeError:
            print("BUUUUG")
            '''sleep(5)
            # try again
            moves = get_figures()
            # find enemy's move
            fr, to = new_move(last_moves, moves)
            mv = (number_to_letter(fr) + number_to_letter(to))
            print("enemy move: ", mv)
            # make enemy move
            stockfish.make_moves_from_current_position([mv])'''
            pass 

        print(stockfish.get_board_visual())     # print board

        # checkmate
        board = chess_lb.Board(stockfish.get_fen_position() )
        if board.is_checkmate() == True:
            print("Game over. We win! ")
            exit()



else:
    pass

