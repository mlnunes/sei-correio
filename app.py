import pyautogui
import os

print (os.getcwd())
im = pyautogui.screenshot()
arquivo = "print_screen.jpg"
im.save(arquivo)