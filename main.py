import numpy as np
import cv2
import kociemba
from collections import Counter

webcam = cv2.VideoCapture(0)
counter = 0
cube = [[[-1 for _ in range(3)] for _ in range(3)] for _ in range(6)]
isSaved = [False] * 6
wallCounter = 0

while (wallCounter < 6):
    ret, imageFrame = webcam.read()
    if ret:
        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        red_lower = np.array([0, 90, 2], np.uint8)
        red_upper = np.array([7, 255, 255], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        green_lower = np.array([70, 90, 2], np.uint8)
        green_upper = np.array([95, 255, 255], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        blue_lower = np.array([95, 90, 2], np.uint8)
        blue_upper = np.array([120, 255, 255], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        orange_lower = np.array([7, 90, 2], np.uint8)
        orange_upper = np.array([20, 255, 255], np.uint8)
        orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

        yellow_lower = np.array([20, 90, 2], np.uint8)
        yellow_upper = np.array([30, 255, 255], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        white_lower = np.array([0, 0, 190], np.uint8)
        white_upper = np.array([255, 90, 255], np.uint8)
        white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

        middle = [int(imageFrame.shape[1] / 2), int(imageFrame.shape[0] / 2)]
        gap = 100

        targets = [[middle[0] - gap, middle[1] - gap, -1],
                  [middle[0], middle[1] - gap, -1],
                  [middle[0] + gap, middle[1] - gap, -1],
                  [middle[0] - gap, middle[1], -1],
                  [middle[0], middle[1], -1],
                  [middle[0] + gap, middle[1], -1],
                  [middle[0] - gap, middle[1] + gap, -1],
                  [middle[0], middle[1] + gap, -1],
                  [middle[0] + gap, middle[1] + gap, -1]]
        isRecognized = True

        #print(hsvFrame[targets[4][1], targets[4][0]])

        for target in targets:
            if red_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 0, 255), 8)
                target[2] = 2
            elif green_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 255, 0), 8)
                target[2] = 4
            elif blue_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (255, 0, 0), 8)
                target[2] = 1
            elif orange_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 122, 255), 8)
                target[2] = 5
            elif yellow_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 255, 255), 8)
                target[2] = 3
            elif white_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (255, 255, 255), 8)
                target[2] = 0
            else:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 10, (0, 0, 0), 8)
                isRecognized = False


        imageFrame = cv2.flip(imageFrame, 1)

        cv2.imshow("Color Detection", imageFrame)

        if isRecognized and not isSaved[targets[4][2]]:
            counter += 1
        else:
            counter = 0

        if counter == 25:
            #print(targets[0][2], targets[1][2], targets[2][2])
            #print(targets[3][2], targets[4][2], targets[5][2])
            #print(targets[6][2], targets[7][2], targets[8][2])
            isSaved[targets[4][2]] = True
            cube[targets[4][2]][0][0] = targets[0][2]
            cube[targets[4][2]][0][1] = targets[1][2]
            cube[targets[4][2]][0][2] = targets[2][2]
            cube[targets[4][2]][1][0] = targets[3][2]
            cube[targets[4][2]][1][1] = targets[4][2]
            cube[targets[4][2]][1][2] = targets[5][2]
            cube[targets[4][2]][2][0] = targets[6][2]
            cube[targets[4][2]][2][1] = targets[7][2]
            cube[targets[4][2]][2][2] = targets[8][2]
            wallCounter += 1
            print("Wall " + str(wallCounter) + " saved!!!")

        cv2.imshow("Color Detection", imageFrame)

    else:
        print("Image reading error!!!")

    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break

cube_string = ""
for wall in cube:
    for row in wall:
        for cell in row:
            if cell == 0:
                cube_string += 'U'
            elif cell == 1:
                cube_string += 'R'
            elif cell == 2:
                cube_string += 'F'
            elif cell == 3:
                cube_string += 'D'
            elif cell == 4:
                cube_string += 'L'
            elif cell == 5:
                cube_string += 'B'
            else:
                print("ERROR!!!")

print(cube_string)
print(Counter(cube_string))

cube_solution = kociemba.solve(cube_string)

print(cube_solution)