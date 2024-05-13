import pygame
import time
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image
import threading
import os

pygame.init()

timer = 30

class RadioMenuItem(MenuItem):
    def __init__(self, title, checked=False, on_clicked=None):
        super().__init__(title, on_clicked)
        self._checked = checked

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self._checked = value

    def draw(self, icon, surface, rect):
        super().draw(icon, surface, rect)
        if self.checked:
            pygame.draw.circle(surface, (0, 0, 255), (rect.left + 8, rect.centery), 4)

submenu_items = [
    RadioMenuItem('5 minutes', on_clicked=lambda: set_timer(5, submenu_items[0])),
    RadioMenuItem('15 minutes', on_clicked=lambda: set_timer(15, submenu_items[1])),
    RadioMenuItem('30 minutes', on_clicked=lambda: set_timer(30, submenu_items[2])),
    RadioMenuItem('1 hour', on_clicked=lambda: set_timer(60, submenu_items[3])),
    RadioMenuItem('2 hours', on_clicked=lambda: set_timer(120, submenu_items[4]))
]

def fart():
    sound = pygame.mixer.Sound('data/fart.mp3')
    sound.play()

def main():
    global timer
    while True:
        fart()
        time.sleep(timer * 60)

def run_icon():
    global timer, submenu_items

    update_menu_items(30, submenu_items[2])
    
    icon_image = Image.open('data/icon.png')
    
    timer_menu = MenuItem('Timer', Menu(*submenu_items))
    menu = Menu(timer_menu, MenuItem('Quit', lambda: os._exit(0)))
    
    icon = pystray.Icon('fart_icon', title='Fart App', icon=icon_image, menu=menu)
    icon.run()

def set_timer(duration, radioitem):
    global timer
    print(f"Timer set to {duration} minutes.")
    timer = duration
    update_menu_items(duration, radioitem)

def update_menu_items(duration, radioitem):
    global timer, submenu_items
    for item in submenu_items:
        item.checked = False
        
    radioitem.checked = True if timer == duration else False

icon_thread = threading.Thread(target=run_icon)
icon_thread.start()

main()
