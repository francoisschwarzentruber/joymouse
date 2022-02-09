#by François Schwarzentruber
# a few part comes from https://codereview.stackexchange.com/questions/151975/joystick-to-mouse-keyboard-mapping-program

import pygame

from pygame.locals import *
import pynput.mouse
import pynput.keyboard
mouse = pynput.mouse.Controller()
keyboard = pynput.keyboard.Controller()
Key = pynput.keyboard.Key

import math

def main():
   print('Welcome! Let us control the mouse via the joystick to cure your hand.')
   pygame.init()
   clock = pygame.time.Clock()
   joysticks = []
   for i in range(0, pygame.joystick.get_count()):
      joysticks.append(pygame.joystick.Joystick(i))
      joysticks[-1].init()

   while 1:
      clock.tick(60)

      updateData(pygame.joystick.Joystick(0))
      doActions()

      for event in pygame.event.get():
         if event.type == QUIT:
             print ("Received event 'Quit', exiting.")
             return


controls = { 
            'x-axis': 0,
            'y-axis': 0,
            'z-axis': 0,
            'hat-x': 0,
            'hat-y': 0,
            'slider': 0,
            'button-1': 0,
            'button-2': 0,
            'button-3': 0,
            'button-4': 0,
            'button-5': 0,
            'button-6': 0,
            'button-7': 0,
            'button-8': 0,
            'button-9': 0,
            'button-10': 0,
            'button-11': 0,
            'button-12': 0}


#contains the previous state of the controls
old_controls = controls.copy()

def updateData(joystick):
    global old_controls
    old_controls = controls.copy()

    for i in range(0, 12):
        controls['button-'+str(i+1)] = joystick.get_button(i)
    controls['slider'] = joystick.get_axis(2)
    controls['x-axis'] = joystick.get_axis(0)
    controls['y-axis'] = joystick.get_axis(1)
    controls['z-axis'] = joystick.get_axis(3)
    controls['hat-x'] = joystick.get_hat(0)[0]
    controls['hat-y'] = joystick.get_hat(0)[1]


######################################################
######################################################
######################################################


def keyAction(keyChar):
    return (lambda old, new:
        keyEvent(bool(new), keyChar))

def mousePressLeftAction(old, new):
	if new:
		mouse.press(pynput.mouse.Button.left)
	else:
		mouse.release(pynput.mouse.Button.left)

def mousePressRightAction(old, new):
	if new:
		mouse.press(pynput.mouse.Button.right)
	else:
		mouse.release(pynput.mouse.Button.right)



SPEEDFAST = 64
SPEEDNORMAL = 16
SPEEDSLOW = 3

speed = SPEEDNORMAL
isScroll = False



def mouseMove(axis, v):
	x, y = 0, 0
	d = abs(v)
	if axis == 0:
	     x += int(v*d*speed)
	else:
	     y += int(v*d*speed)
	     
	if isScroll:
             mouse.scroll(int(x/8), -int(y/8))
	else:
	     mouse.move(x, y)


def changeSpeed(old, new):
	global speed
	if new:
		speed = SPEEDFAST
	else:
	 	speed = SPEEDNORMAL


def skip(old, new):
	pass
	
	
	
def keyDirectionAction(old, new, left, right):
     if new > 0:
          keyboard.press(right)
     elif new < 0:
          keyboard.press(left)
     else:
          keyboard.release(left)
          keyboard.release(right)
          
def keyLeftRightAction(old, new):
     keyDirectionAction(old, new, Key.left, Key.right)



def switchToScroll(old, new):
     global isScroll
     isScroll = new
	
def keyDownUpAction(old, new):
     keyDirectionAction(old, new, Key.down, Key.up)



actions = {
    'x-axis': skip,
    'y-axis': skip,
    'z-axis': skip,
    'hat-x': keyLeftRightAction,
    'hat-y': keyDownUpAction,
    'slider': skip,
    'button-1': skip,
    'button-2': switchToScroll,
    'button-3': mousePressLeftAction,
    'button-4': changeSpeed,
    'button-5': mousePressRightAction,
    'button-6': skip,
    'button-7': skip,
    'button-8': skip,
    'button-9': skip,
    'button-10': skip,
    'button-11': skip,
    'button-12': keyAction('esc')
}


def doActions():
    mouseMove(0, controls['x-axis'])
    mouseMove(1, controls['y-axis'])
    for key in controls:
        if old_controls[key] != controls[key]:
            actions[key](old_controls[key], controls[key])


######################################################
######################################################
######################################################



def keyEvent(keyDown, keyName):
    if keyDown:
    	pyautogui.keyDown(keyName)
    else:
        pyautogui.keyUp(keyName)





if __name__ == "__main__":
    main()
