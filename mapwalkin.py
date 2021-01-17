# https://www.youtube.com/watch?v=dUU6ZsJlZKQ&ab_channel=sentdex
from grabscreen import grab_screen
import cv2
import numpy as np
import time
import keys as k

keys = k.Keys()


def turn_around():
    keys.directMouse(-3490, 0)
    time.sleep(0.1)


def pathing(minimap, just_turned):
    lower = np.array([75,150,150])
    upper = np.array([150,255,255])
    
    hsv = cv2.cvtColor(minimap, cv2.COLOR_RGB2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    
    matches = np.argwhere(mask==255)
    mean_y = np.mean(matches[:,1])
    target = minimap.shape[1] / 2
    
    err = target - mean_y
    
    print(err)
    
    if np.isnan(err) and not just_turned:
        turn_around()
        return True
    if np.isnan(err) and just_turned:
        return 'STOP'
    else:
        keys.directMouse(-1*int(err*3), 0)
        return False
    
# =============================================================================
#     cv2.imshow("cv2screen", mask)
#     cv2.waitKey(10)
# =============================================================================


for i in range(3):
    print(i)
    time.sleep(1)

keys.directKey("w")
keys.directKey("lshift")
just_turned = False

for i in range(1):
    screen = grab_screen(region=(1280, 0, 1780, 500))
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    minimap = screen[49:290, 347:577]
    miniminimap = screen[142:167, 430:490]
    
    just_turned = pathing(miniminimap, just_turned)

    if just_turned == 'STOP':
        break

keys.directKey("w", keys.key_release)
keys.directKey("lshift", keys.key_release)
cv2.destroyAllWindows()