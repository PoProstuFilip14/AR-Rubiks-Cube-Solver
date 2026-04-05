import numpy as np
import cv2

webcam = cv2.VideoCapture(0)

while (1):
    ret, imageFrame = webcam.read()
    if ret:
        imageFrame = cv2.flip(imageFrame, 1)

        hsvFrame = cv2.cvtColor(imageFrame, cv2.COLOR_BGR2HSV)

        red_lower = np.array([0, 100, 2], np.uint8)
        red_upper = np.array([7, 255, 210], np.uint8)
        red_mask = cv2.inRange(hsvFrame, red_lower, red_upper)

        green_lower = np.array([70, 100, 2], np.uint8)
        green_upper = np.array([90, 255, 210], np.uint8)
        green_mask = cv2.inRange(hsvFrame, green_lower, green_upper)

        blue_lower = np.array([100, 100, 2], np.uint8)
        blue_upper = np.array([120, 255, 210], np.uint8)
        blue_mask = cv2.inRange(hsvFrame, blue_lower, blue_upper)

        orange_lower = np.array([7, 100, 2], np.uint8)
        orange_upper = np.array([20, 255, 210], np.uint8)
        orange_mask = cv2.inRange(hsvFrame, orange_lower, orange_upper)

        yellow_lower = np.array([20, 100, 2], np.uint8)
        yellow_upper = np.array([30, 255, 210], np.uint8)
        yellow_mask = cv2.inRange(hsvFrame, yellow_lower, yellow_upper)

        white_lower = np.array([0, 0, 2], np.uint8)
        white_upper = np.array([255, 100, 255], np.uint8)
        white_mask = cv2.inRange(hsvFrame, white_lower, white_upper)

        middle = [int(imageFrame.shape[1] / 2), int(imageFrame.shape[0] / 2)]
        gap = 70

        targets = [[middle[0] - gap, middle[1] - gap],
                  [middle[0], middle[1] - gap],
                  [middle[0] + gap, middle[1] - gap],
                  [middle[0] - gap, middle[1]],
                  [middle[0], middle[1]],
                  [middle[0] + gap, middle[1]],
                  [middle[0] - gap, middle[1] + gap],
                  [middle[0], middle[1] + gap],
                  [middle[0] + gap, middle[1] + gap]]

        print(hsvFrame[targets[5][1], targets[5][0]])

        for target in targets:
            if red_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 0, 255), 8)
            elif green_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 255, 0), 8)
            elif blue_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (255, 0, 0), 8)
            elif orange_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 122, 255), 8)
            elif yellow_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (0, 255, 255), 8)
            elif white_mask[target[1], target[0]] > 0:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 5, (255, 255, 255), 8)
            else:
                imageFrame = cv2.circle(imageFrame, [target[0], target[1]], 10, (0, 0, 0), 8)

        cv2.imshow("Color Detection", imageFrame)

    else:
        print("Image reading error!!!")

    if cv2.waitKey(10) & 0xFF == ord('q'):
        webcam.release()
        cv2.destroyAllWindows()
        break