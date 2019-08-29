from selenium import webdriver
from os import path
from stockfish import Stockfish
from requests import get
from time import sleep, time
from random import choice
import logging

SCRIPT_PATH = path.dirname(path.realpath(__file__))
DRIVER_PATH = SCRIPT_PATH + "./chromedriver"
STOCKFISH_PATH = SCRIPT_PATH + "./stockfish-10-win/stockfish_10_x32.exe"

webdriver.remote.remote_connection.LOGGER.setLevel(logging.WARNING)

def find_best_move(stockfish, fen):
    stockfish.set_fen_position(fen)
    return stockfish.get_best_move()

def is_check_mate(driver, team):
    html = driver.execute_script("return document.documentElement.outerHTML;")
    if ("Şah Mat" in html):
        return True
    else:
        if ("Zaman doldu" in html):
            if (team == "white" and "Zafer Beyazın" in html):
                return True
            elif (team == "black" and "Zafer Siyahın" in html):
                return True
            else:
                return False
        else:
            return False

def get_team(driver):
    html = driver.execute_script("return document.documentElement.outerHTML;")
    if ("You play the white pieces" in html):
        print("u are white")
        return "white"
    else:
        print("u are black")
        return "black"

def make_move(driver, move):
    driver.execute_script("window.lichess.socket.send(\"move\", {u:\"" + move + "\", b:1})")

def is_ur_turn(driver):
    html = driver.execute_script("return document.documentElement.outerHTML;")
    if ("Sıra sizde" in html):
        return True
    else:
        return False

def get_fen(driver):
    resp = get(driver.current_url)

    if (resp.status_code != 200):
        print("get_fen response status was: ", resp.status_code)
        return ""
    
    return resp.text.split('"fen":"')[-1].split('"}')[0]

if __name__ == "__main__":
    stockfish = Stockfish(STOCKFISH_PATH)

    driver = webdriver.Chrome(
        executable_path=DRIVER_PATH,
    ) 

    driver.get("https://lichess.org/")

    input("Press enter when u enter a game: ")

    team = get_team(driver)

    print ("playing as", team)

    while (True):
        if (is_check_mate(driver, team)):
            print("check mate")
            break

        if (is_ur_turn(driver) == False):
            sleep(1)
            continue

        sleep(choice(range(5)))
        fen = get_fen(driver)
        move = find_best_move(stockfish, fen)
        print("best move", move)
        make_move(driver, move)
        sleep(1)
        
    driver.quit()