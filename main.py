from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from math import inf
import pyautogui as gui # allows me to simulate mouse/keyboard presses, lets me click on nordvpn chrome extension

import os
import time

# found bug, if mouse is already to the far right, can't move right anymore and cant find volume controls

browser = None
muted = False
direction = 1

def refresh(browser):
    browser.refresh()
    time.sleep(5)


def fullScreen():
    gui.press('f')
    time.sleep(1)
    screenWidth, screenHeight = gui.size()  # Get the size of the primary monitor.
    gui.moveTo(screenWidth-20, 10)
    gui.click()
    gui.moveTo(screenWidth/2, screenHeight/2)  # Move the mouse to XY coordinates.


# mute/unmute audio
def muteAudio(mute):
    global direction
    gui.move(direction, 0)
    if (mute):
        try:
            audio_button = browser.find_element_by_xpath("//button[@class='touchable PlayerControls--control-element nfp-button-control default-control-button button-volumeMax']")
            # class ="touchable PlayerControls--control-element nfp-button-control default-control-button button-volumeMax"
            audio_button.click()
            gui.move(direction, 0)
        except:
            print("couldn't find volume Max button")
            # if there is an error, then audio is already muted, couldnt find "volumeMax"
            # pass
    else:
        try:
            audio_button = browser.find_element_by_xpath("//button[@class='touchable PlayerControls--control-element nfp-button-control default-control-button button-volumeMuted']")
            audio_button.click()
            gui.move(direction, 0)
        except:
            print("couldn't find volume mute button")
            # if error, then already unmuted
            # pass
    direction *= -1


# login using credentials above
def signInNetflix(email, password):
    # enter email and continue
    email_input = browser.find_element_by_id('id_userLoginId')
    email_input.send_keys(email)
    # enter password to login
    password_input = browser.find_element_by_id('id_password')
    password_input.send_keys(password)

    signIn_button = browser.find_element_by_xpath("//button[@type='submit']")
    signIn_button.click()

    # once logged in, find "Paige" and click on Icon
    time.sleep(0.75)

    users = browser.find_elements_by_xpath("//span[@class='profile-name']")
    # locate user paige and click on profile
    for user in users:
        if user.text == "Landon":
            user.click()
            break


# log into nordvpn chrome extension and connect to canada's server
def logIntoVPN():
    wait_time = 0.5
    time.sleep(wait_time)
    gui.click('nordvpn_logo.PNG')
    time.sleep(0.5)
    gui.move(-25, 225)
    time.sleep(wait_time)
    gui.click()
    # enter username
    gui.write('landonhill07@gmail.com')
    gui.move(0, 50)
    time.sleep(wait_time)
    gui.click()
    # enter password
    gui.write('Wazupnord12!')
    gui.move(0, 50)
    time.sleep(wait_time)
    # log in
    gui.click()
    time.sleep(wait_time + 2)
    gui.move(0, 75)
    time.sleep(wait_time)
    gui.click()
    gui.write('canada')
    gui.move(0, -275)
    time.sleep(wait_time)
    gui.click()
    time.sleep(wait_time)
    gui.move(-400, 0)
    gui.click()
    time.sleep(2)


def searchAndPlayShow(show_name):
    # find search icon
    search = browser.find_element_by_xpath("//button[@class='searchTab']")
    search.click()

    search_box = browser.find_element_by_xpath("//input[@type='text']")
    search_box.send_keys(show_name)

    time.sleep(3)

    # find suits (assume first row first column)
    show = browser.find_element_by_xpath("//div[@class='slider-item slider-item-0']")
    show.click()
    time.sleep(2)
    resume_button = browser.find_element_by_xpath("//a[@class=' playLink']")
    resume_button.click()
    time.sleep(5)


def main():
    global browser
    executable_path = 'C:\\Users\\lhill5\\Downloads\\chromedriver_win32\\chromedriver.exe'

    os.environ["webdriver.chrome.driver"] = executable_path

    chrome_options = Options()
    chrome_options.add_extension('C:\\Users\\lhill5\\Downloads\\fjoaledfpmneenckfbpdfhkmimnjocfa.zip')

    browser = webdriver.Chrome(executable_path=executable_path, options=chrome_options)

    browser.get('https://www.netflix.com/login')
    email = 'ronhill6363@gmail.com'
    password = 'Crabby1963'


    signInNetflix(email, password)
    logIntoVPN()
    refresh(browser)

    searchAndPlayShow('suits')
    fullScreen()

    curse_words = ['goddamn', 'goddam', 'god-damn', 'god damn', 'jesus', 'christ', 'jesus christ']
    previous_subtitles = ""

    while True:
        try:
            subtitle_elem = browser.find_elements_by_xpath("//div[@class='player-timedtext-text-container']")
            subtitles = ""
            for subtitle in subtitle_elem:
                subtitles += subtitle.text
                subtitles += ' '

            subtitles = subtitles.strip() # removes trailing whitespace character
            subtitles = subtitles.lower()
            # if new subtitles exists
            # print(subtitles, previous_subtitles)
            if subtitles != "" and subtitles != previous_subtitles:
                # print('different')
                print(subtitles)
                previous_subtitles = subtitles
                for curse_word in curse_words:
                    if curse_word in subtitles:
                        muteAudio(True)
                        muted = True
                        break
                else:
                    # no curse word found in subtitles so unmute if muted
                    if muted:
                        muteAudio(False)
                        muted = False
        except:
            pass


if __name__ == '__main__':
    main()

