import pygame
import os
import time
import numpy as np
import RPi.GPIO as GPIO

os.putenv('SDL_VIDEODRIVER', 'fbcon')  # Display on piTFT
os.putenv('SDL_FBDEV', '/dev/fb1')
GPIO.setmode(GPIO.BCM)  # Set for broadcom numbering not board numbers
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def GPIO27_callback(channel):
    print("Exit Program...")
    exit(True)


pygame.init()
size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)
ball_a = pygame.image.load("img.png")
ball_a = pygame.transform.scale(ball_a,(100,100))
ball_b = pygame.image.load("img.png")
ball_b = pygame.transform.scale(ball_b,(100,100))
ballrect_a = ball_a.get_rect()
ballrect_b = ball_b.get_rect()
da, db = ballrect_a.height, ballrect_b.height
print(da,db)
ra, rb = np.array([50.0, 50.0]), np.array([200.0, 100.0])
va, vb = np.array([4.0, 3.0]), np.array([-2.0, 3.0])
ma, mb = 1.0, 0.5  # Set mass of two balls
counter = 0
GPIO.add_event_detect(27, GPIO.FALLING, callback=GPIO27_callback, bouncetime=300)
while True:
    time.sleep(0.02)
    r = ra - rb + va - vb
    # Check if two ball collide
    if (np.sqrt(r.dot(r)) < (da + db) / 2) and (r.dot(va - vb) < 0):
        counter = counter + 1
        print("Collision detected " + str(counter))
        r0 = r / np.sqrt(r.dot(r))
        # Calculate normal vector
        vra0, vrb0 = r0.dot(va) * r0, r0.dot(vb) * r0
        vta, vtb = va - vra0, vb - vrb0

        vra = (vra0 * (ma - mb) + 2 * vrb0 * mb) / (ma + mb)
        vrb = (vrb0 * (mb - ma) + 2 * vra0 * ma) / (ma + mb)
        va, vb = vra + vta, vrb + vtb

    ra, rb = ra + va, rb + vb
    ballrect_a.center = np.rint(ra)
    ballrect_b.center = np.rint(rb)
    # Check if balls are at the edge
    if (ballrect_a.left < 0 and va[0] < 0) or (ballrect_a.right > width and va[0] > 0):
        va[0] = -va[0]
    if (ballrect_a.top < 0 and va[1] < 0) or (ballrect_a.bottom > height and va[1] > 0):
        va[1] = -va[1]
    if (ballrect_b.left < 0 and vb[0] < 0) or (ballrect_b.right > width and vb[0] > 0):
        vb[0] = -vb[0]
    if (ballrect_b.top < 0 and vb[1] < 0) or (ballrect_b.bottom > height and vb[1] > 0):
        vb[1] = -vb[1]

    screen.fill(black)  # Clear the screen
    screen.blit(ball_a, ballrect_a)  # Attach 1st ball to the screen
    screen.blit(ball_b, ballrect_b)  # Attach 2nd ball to the screen
    pygame.display.flip()  # Display the new frame
