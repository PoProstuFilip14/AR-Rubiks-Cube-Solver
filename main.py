import math
import numpy as np
import cv2
import kociemba
import datetime
import csv
import os
from collections import Counter

results = [[[[] for _ in range(2)]] for _ in range(6)]
stats = [
    ['Kolor', 'Correct-Color', 'Wrong-Color', 'Non-Color', 'All', 'Highest_H', 'Highest_S','Highest_V', 'Lowest_H', 'Lowest_S', 'Lowest_V', 'No-Square'],
    ['White', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0],
    ['Blue', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0],
    ['Red', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0],
    ['Yellow', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0],
    ['Green', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0],
    ['Orange', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0],
    ['None', 0, 0, 0, 0, -1, -1, -1, 256, 256, 256, 0]
]
color_groups = [[0 for _ in range(7)] for _ in range(60)]
cube = [[[-1 for _ in range(3)] for _ in range(3)] for _ in range(6)]
limits = [[[0, 77, 16], [4, 225, 255]],#red1
          [[165, 77, 16], [179, 225, 255]],#red2
          [[36, 48, 24], [98, 255, 255]],#green
          [[99, 0, 20], [119, 255, 225]],#blue
          [[5, 48, 29], [14, 255, 255]],#orange
          [[15, 26, 86], [35, 255, 255]],#yellow
          [[37, 0, 114], [164, 117, 255]],#white
          [[6, 48, 29], [14, 255, 255]]]#orange2 (not in use)
middle = [int(0), int(0)]
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
is_recognized = True

def main():
    exit = False

    while not exit:
        option = input()
        if option == '1':
            cube_solver()
        elif option == '2':
            take_photos()
        elif option == '3':
            test_photos()
        elif option == '4':
            exit = True

def take_photos():
    is_accepted = False
    counter = 0
    cam = cv2.VideoCapture(0)

    while 1:
        ret, frame = cam.read()

        if counter == 10:
            cam.release()
            cv2.destroyWindow("Captured")
            break
        if ret:
            frame = cv2.flip(frame, 1)

            if not is_accepted:
                middle = [int(frame.shape[1] / 2), int(frame.shape[0] / 2)]
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

                for target in targets:
                    frame = cv2.circle(frame, [target[0], target[1]], 10, (0, 0, 0), 8)

            cv2.imshow("Captured", frame)

            if is_accepted:
                filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                cv2.imwrite(f"photos/{filename}_{counter}.png", frame)
                counter += 1

        else:
            print("Failed to capture image.")
            break

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            cam.release()
            cv2.destroyWindow("Captured")
            break

        if key == ord('0'):
            is_accepted = True

def test_photos():
    global targets

    directory = 'temp_photos'

    counter = 0
    wall_counter = 0
    row_counter = 0
    cell_counter = 0
    last_keys = ['n' for _ in range(3)]

    for frame in os.scandir(directory):
        if frame.is_file():
            img = cv2.imread(frame)
            middle = [int(img.shape[1] / 2), int(img.shape[0] / 2)]
            gap = 100

            hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            hsv_frame[:,:,2] = cv2.equalizeHist(hsv_frame[:,:,2])

            targets = [[middle[0] - gap, middle[1] - gap, -1],
                       [middle[0], middle[1] - gap, -1],
                       [middle[0] + gap, middle[1] - gap, -1],
                       [middle[0] - gap, middle[1], -1],
                       [middle[0], middle[1], -1],
                       [middle[0] + gap, middle[1], -1],
                       [middle[0] - gap, middle[1] + gap, -1],
                       [middle[0], middle[1] + gap, -1],
                       [middle[0] + gap, middle[1] + gap, -1]]

            squares = square_finder(img, False)
            print(len(squares))

            red_lower = np.array([limits[0][0][0], limits[0][0][1], limits[0][0][2]], np.uint8)
            red_upper = np.array([limits[0][1][0], limits[0][1][1], limits[0][1][2]], np.uint8)

            red_lower_2 = np.array([limits[1][0][0], limits[1][0][1], limits[1][0][2]], np.uint8)
            red_upper_2 = np.array([limits[1][1][0], limits[1][1][1], limits[1][1][2]], np.uint8)

            green_lower = np.array([limits[2][0][0], limits[2][0][1], limits[2][0][2]], np.uint8)
            green_upper = np.array([limits[2][1][0], limits[2][1][1], limits[2][1][2]], np.uint8)

            blue_lower = np.array([limits[3][0][0], limits[3][0][1], limits[3][0][2]], np.uint8)
            blue_upper = np.array([limits[3][1][0], limits[3][1][1], limits[3][1][2]], np.uint8)

            orange_lower = np.array([limits[4][0][0], limits[4][0][1], limits[4][0][2]], np.uint8)
            orange_upper = np.array([limits[4][1][0], limits[4][1][1], limits[4][1][2]], np.uint8)

            yellow_lower = np.array([limits[5][0][0], limits[5][0][1], limits[5][0][2]], np.uint8)
            yellow_upper = np.array([limits[5][1][0], limits[5][1][1], limits[5][1][2]], np.uint8)

            white_lower = np.array([limits[6][0][0], limits[6][0][1], limits[6][0][2]], np.uint8)
            white_upper = np.array([limits[6][1][0], limits[6][1][1], limits[6][1][2]], np.uint8)

            orange_lower_2 = np.array([limits[7][0][0], limits[7][0][1], limits[7][0][2]], np.uint8)
            orange_upper_2 = np.array([limits[7][1][0], limits[7][1][1], limits[7][1][2]], np.uint8)

            for target in targets:
                scale_up = 2

                x_start, y_start, x_end, y_end = target[0] - int(gap), target[1] - int(gap), target[0] + int(gap), target[1] + int(gap)
                cropped_img = img[y_start:y_end, x_start:x_end]

                cropped_img = cv2.resize(cropped_img, None, fx=scale_up, fy=scale_up, interpolation=cv2.INTER_LINEAR)

                cv2.imshow("Cropped Image", cropped_img)
                
                detected_color = 'n'

                counter += 1

                if wall_counter == 0:
                    if cell_counter == 0:
                        key = cv2.waitKey(0) & 0xFF
                        last_keys[row_counter] = key
                        cell_counter = cell_counter + 1
                    else:
                        key = last_keys[row_counter]
                        cell_counter = cell_counter + 1
                        if cell_counter == 3:
                            cell_counter = 0
                            row_counter = row_counter + 1
                    if row_counter == 3:
                        row_counter = 0
                        wall_counter = wall_counter + 1
                else:
                    key = last_keys[row_counter]
                    cell_counter = cell_counter + 1
                    if cell_counter == 3:
                        cell_counter = 0
                        row_counter = row_counter + 1
                    if row_counter == 3:
                        row_counter = 0
                        wall_counter = wall_counter + 1
                    if wall_counter == 10:
                        wall_counter = 0
                is_square = False
                for square in squares:
                    mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
                    cv2.drawContours(mask, [square], -1, 255, -1)
                    kernel = np.ones((5, 5), np.uint8)
                    mask = cv2.erode(mask, kernel)

                    x, y, w, h = cv2.boundingRect(square)
                    roi = hsv_frame[y:y + h, x:x + w]

                    h_channel = hsv_frame[:, :, 0]
                    s_channel = hsv_frame[:, :, 1]
                    v_channel = hsv_frame[:, :, 2]

                    valid_mask = (mask == 255) & (s_channel > 60) & (v_channel > 50)

                    h_vals = h_channel[valid_mask]

                    if len(h_vals) == 0:
                        continue

                    hist = np.bincount(h_vals, minlength=180)
                    h_dom = np.argmax(hist)

                    s_vals = s_channel[mask == 255]
                    v_vals = v_channel[mask == 255]

                    s_med = np.median(s_vals)
                    v_med = np.median(v_vals)

                    hsv_med = np.array([h_dom, s_med, v_med], np.uint8)

                    x, y, w, h = cv2.boundingRect(square)

                    rect = cv2.minAreaRect(square)
                    box = cv2.boxPoints(rect)
                    box = box.astype(int)

                    if x <= target[0] <= x + w and y <= target[1] <= y + h:
                        is_square = True
                        if (white_lower[0] <= h_dom <= white_upper[0] and
                            white_lower[1] <= s_med <= white_upper[1] and
                            white_lower[2] <= v_med <= white_upper[2]):
                            detected_color = 'w'
                        elif ((red_lower[0] <= h_dom <= red_upper[0] and
                            red_lower[1] <= s_med <= red_upper[1] and
                            red_lower[2] <= v_med <= red_upper[2]) or
                            (red_lower_2[0] <= h_dom <= red_upper_2[0] and
                            red_lower_2[1] <= s_med <= red_upper_2[1] and
                            red_lower_2[2] <= v_med <= red_upper_2[2])):
                            detected_color = 'r'
                        elif (green_lower[0] <= h_dom <= green_upper[0] and
                            green_lower[1] <= s_med <= green_upper[1] and
                            green_lower[2] <= v_med <= green_upper[2]):
                            detected_color = 'g'
                        elif (blue_lower[0] <= h_dom <= blue_upper[0] and
                            blue_lower[1] <= s_med <= blue_upper[1] and
                            blue_lower[2] <= v_med <= blue_upper[2]):
                            detected_color = 'b'
                        elif (orange_lower[0] <= h_dom <= orange_upper[0] and
                            orange_lower[1] <= s_med <= orange_upper[1] and
                            orange_lower[2] <= v_med <= orange_upper[2]):
                            detected_color = 'o'
                        elif (yellow_lower[0] <= h_dom <= yellow_upper[0] and
                            yellow_lower[1] <= s_med <= yellow_upper[1] and
                            yellow_lower[2] <= v_med <= yellow_upper[2]):
                            detected_color = 'y'
                        #print(f"counter={counter}, cell={cell_counter}, row={row_counter}, wall={wall_counter}")

                        if key == ord('w'):
                            stats[1][4] += 1
                            color_groups[math.floor(hsv_med[0] / 3)][0] += 1
                            if hsv_med[0] > stats[1][5]:
                                stats[1][5] = hsv_med[0]
                            if hsv_med[1] > stats[1][6]:
                                stats[1][6] = hsv_med[1]
                            if hsv_med[2] > stats[1][7]:
                                stats[1][7] = hsv_med[2]
                            if hsv_med[0] < stats[1][8]:
                                stats[1][8] = hsv_med[0]
                            if hsv_med[1] < stats[1][9]:
                                stats[1][9] = hsv_med[1]
                            if hsv_med[2] < stats[1][10]:
                                stats[1][10] = hsv_med[2]
                            if detected_color == 'w':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[1][1] += 1
                            elif detected_color == 'n':
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[1][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[1][2] += 1
                        elif key == ord('b'):
                            color_groups[math.floor(hsv_med[0] / 3)][1] += 1
                            if hsv_med[0] > stats[2][5]:
                                stats[2][5] = hsv_med[0]
                            if hsv_med[1] > stats[2][6]:
                                stats[2][6] = hsv_med[1]
                            if hsv_med[2] > stats[2][7]:
                                stats[2][7] = hsv_med[2]
                            if hsv_med[0] < stats[2][8]:
                                stats[2][8] = hsv_med[0]
                            if hsv_med[1] < stats[2][9]:
                                stats[2][9] = hsv_med[1]
                            if hsv_med[2] < stats[2][10]:
                                stats[2][10] = hsv_med[2]
                            stats[2][4] += 1
                            if detected_color == 'b':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[2][1] += 1
                            elif detected_color == 'n':
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[2][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[2][2] += 1
                        elif key == ord('r'):
                            color_groups[math.floor(hsv_med[0] / 3)][2] += 1
                            if hsv_med[0] > stats[3][5] and hsv_med[0] < 90:
                                stats[3][5] = hsv_med[0]
                            if hsv_med[1] > stats[3][6]:
                                stats[3][6] = hsv_med[1]
                            if hsv_med[2] > stats[3][7]:
                                stats[3][7] = hsv_med[2]
                            if hsv_med[0] < stats[3][8] and hsv_med[0] > 90:
                                stats[3][8] = hsv_med[0]
                            if hsv_med[1] < stats[3][9]:
                                stats[3][9] = hsv_med[1]
                            if hsv_med[2] < stats[3][10]:
                                stats[3][10] = hsv_med[2]
                            stats[3][4] += 1
                            if detected_color == 'r':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[3][1] += 1
                            elif detected_color == 'n':
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[3][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[3][2] += 1
                        elif key == ord('y'):
                            color_groups[math.floor(hsv_med[0] / 4)][3] += 1
                            if hsv_med[0] > stats[4][5]:
                                stats[4][5] = hsv_med[0]
                            if hsv_med[1] > stats[4][6]:
                                stats[4][6] = hsv_med[1]
                            if hsv_med[2] > stats[4][7]:
                                stats[4][7] = hsv_med[2]
                            if hsv_med[0] < stats[4][8]:
                                stats[4][8] = hsv_med[0]
                            if hsv_med[1] < stats[4][9]:
                                stats[4][9] = hsv_med[1]
                            if hsv_med[2] < stats[4][10]:
                                stats[4][10] = hsv_med[2]
                            stats[4][4] += 1
                            if detected_color == 'y':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[4][1] += 1
                            elif detected_color == 'n':
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[4][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[4][2] += 1
                        elif key == ord('g'):
                            color_groups[math.floor(hsv_med[0] / 3)][4] += 1
                            if hsv_med[0] > stats[5][5]:
                                stats[5][5] = hsv_med[0]
                            if hsv_med[1] > stats[5][6]:
                                stats[5][6] = hsv_med[1]
                            if hsv_med[2] > stats[5][7]:
                                stats[5][7] = hsv_med[2]
                            if hsv_med[0] < stats[5][8]:
                                stats[5][8] = hsv_med[0]
                            if hsv_med[1] < stats[5][9]:
                                stats[5][9] = hsv_med[1]
                            if hsv_med[2] < stats[5][10]:
                                stats[5][10] = hsv_med[2]
                            stats[5][4] += 1
                            if detected_color == 'g':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[5][1] += 1
                            elif detected_color == 'n':
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[5][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[5][2] += 1
                        elif key == ord('o'):
                            color_groups[math.floor(hsv_med[0] / 3)][5] += 1
                            if hsv_med[0] > stats[6][5] and hsv_med[0] < 90:
                                stats[6][5] = hsv_med[0]
                            if hsv_med[1] > stats[6][6]:
                                stats[6][6] = hsv_med[1]
                            if hsv_med[2] > stats[6][7]:
                                stats[6][7] = hsv_med[2]
                            if hsv_med[0] < stats[6][8] and hsv_med[0] > 90:
                                stats[6][8] = hsv_med[0]
                            if hsv_med[1] < stats[6][9]:
                                stats[6][9] = hsv_med[1]
                            if hsv_med[2] < stats[6][10]:
                                stats[6][10] = hsv_med[2]
                            stats[6][4] += 1
                            if detected_color == 'o':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[6][1] += 1
                            elif detected_color == 'n':
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[6][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[0].append([False, hsv_med])
                                stats[6][2] += 1
                        else:
                            color_groups[math.floor(hsv_med[0] / 3)][6] += 1
                            if hsv_med[0] > stats[7][5]:
                                stats[7][5] = hsv_med[0]
                            if hsv_med[1] > stats[7][6]:
                                stats[7][6] = hsv_med[1]
                            if hsv_med[2] > stats[7][7]:
                                stats[7][7] = hsv_med[2]
                            if hsv_med[0] < stats[7][8]:
                                stats[7][8] = hsv_med[0]
                            if hsv_med[1] < stats[7][9]:
                                stats[7][9] = hsv_med[1]
                            if hsv_med[2] < stats[7][10]:
                                stats[7][10] = hsv_med[2]
                            stats[7][4] += 1
                            if detected_color == 'n':
                                print("Poprawny odczyt: " + str(hsv_med))
                                results[0].append([True, hsv_med])
                                stats[7][3] += 1
                            else:
                                print("Nieoprawny odczyt: " + str(hsv_med) + " " + str(detected_color))
                                results[5].append([False, hsv_med])
                                stats[7][2] += 1
                if not is_square:
                    if key == ord('w'):
                        stats[1][4] += 1
                        stats[1][3] += 1
                        stats[1][11] += 1
                    elif key == ord('b'):
                        stats[2][4] += 1
                        stats[2][3] += 1
                        stats[2][11] += 1
                    elif key == ord('r'):
                        stats[3][4] += 1
                        stats[3][3] += 1
                        stats[3][11] += 1
                    elif key == ord('y'):
                        stats[4][4] += 1
                        stats[4][3] += 1
                        stats[4][11] += 1
                    elif key == ord('g'):
                        stats[5][4] += 1
                        stats[5][3] += 1
                        stats[5][11] += 1
                    elif key == ord('o'):
                        stats[6][4] += 1
                        stats[6][3] += 1
                        stats[6][11] += 1
                    else:
                        stats[7][4] += 1
                        stats[7][2] += 1
                        stats[7][11] += 1

    cv2.destroyAllWindows()

    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"results/{filename}_results.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)
    with open(f"stats/{filename}_stats.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(stats)
    with open(f"color_groups/{filename}_color_groups.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(color_groups)

def read_colors(image_frame, squares):
    global targets, is_recognized

    for target in targets:
        target[2] = -1

    hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    hsv_frame = cv2.GaussianBlur(hsv_frame, (5, 5), 0)

    #cv2.imshow("hsv_frame", hsv_frame)

    red_lower = np.array([limits[0][0][0], limits[0][0][1], limits[0][0][2]], np.uint8)
    red_upper = np.array([limits[0][1][0], limits[0][1][1], limits[0][1][2]], np.uint8)

    red_lower_2 = np.array([limits[1][0][0], limits[1][0][1], limits[1][0][2]], np.uint8)
    red_upper_2 = np.array([limits[1][1][0], limits[1][1][1], limits[1][1][2]], np.uint8)

    green_lower = np.array([limits[2][0][0], limits[2][0][1], limits[2][0][2]], np.uint8)
    green_upper = np.array([limits[2][1][0], limits[2][1][1], limits[2][1][2]], np.uint8)

    blue_lower = np.array([limits[3][0][0], limits[3][0][1], limits[3][0][2]], np.uint8)
    blue_upper = np.array([limits[3][1][0], limits[3][1][1], limits[3][1][2]], np.uint8)

    orange_lower = np.array([limits[4][0][0], limits[4][0][1], limits[4][0][2]], np.uint8)
    orange_upper = np.array([limits[4][1][0], limits[4][1][1], limits[4][1][2]], np.uint8)

    yellow_lower = np.array([limits[5][0][0], limits[5][0][1], limits[5][0][2]], np.uint8)
    yellow_upper = np.array([limits[5][1][0], limits[5][1][1], limits[5][1][2]], np.uint8)

    white_lower = np.array([limits[6][0][0], limits[6][0][1], limits[6][0][2]], np.uint8)
    white_upper = np.array([limits[6][1][0], limits[6][1][1], limits[6][1][2]], np.uint8)

    orange_lower_2 = np.array([limits[7][0][0], limits[7][0][1], limits[7][0][2]], np.uint8)
    orange_upper_2 = np.array([limits[7][1][0], limits[7][1][1], limits[7][1][2]], np.uint8)

    #print(hsv_frame[targets[4][1], targets[4][0]])

    counter = 0

    for square in squares:
        mask = np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
        cv2.drawContours(mask, [square], -1, 255, -1)
        kernel = np.ones((5,5), np.uint8)
        mask = cv2.erode(mask, kernel)
        
        x, y, w, h = cv2.boundingRect(square)
        roi = hsv_frame[y:y + h, x:x + w]

        h_channel = hsv_frame[:, :, 0]
        s_channel = hsv_frame[:, :, 1]
        v_channel = hsv_frame[:, :, 2]

        #valid_mask = (mask == 255) & (s_channel > 50) & (v_channel > 60)
        valid_mask = (mask == 255) & ((s_channel > 50) | (v_channel > 150))

        h_vals = h_channel[valid_mask]

        if len(h_vals) == 0:
            continue

        hist = np.bincount(h_vals, minlength=180)
        h_dom = np.argmax(hist)

        s_vals = s_channel[mask == 255]
        v_vals = v_channel[mask == 255]

        s_med = np.median(s_vals)
        v_med = np.median(v_vals)

        hsv_med = np.array([h_dom, s_med, v_med], np.uint8)

        x, y, w, h = cv2.boundingRect(square)

        rect = cv2.minAreaRect(square)
        box = cv2.boxPoints(rect)
        box = box.astype(int)

        for target in targets:
            if x <= target[0] <= x + w and y <= target[1] <= y + h and target[2] < 0:
                counter += 1
                if (green_lower[0] <= h_dom <= green_upper[0] and
                    green_lower[1] <= s_med <= green_upper[1] and
                    green_lower[2] <= v_med <= green_upper[2]):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 255, 0), 8)
                    cv2.drawContours(image_frame, [box], 0, (0, 255, 0), 2)
                    target[2] = 4
                elif (white_lower[0] <= h_dom <= white_upper[0] and
                    white_lower[1] <= s_med <= white_upper[1] and
                    white_lower[2] <= v_med <= white_upper[2]):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (255, 255, 255), 8)
                    cv2.drawContours(image_frame, [box], 0, (255, 255, 255), 2)
                    target[2] = 0
                elif ((red_lower[0] <= h_dom <= red_upper[0] and
                    red_lower[1] <= s_med <= red_upper[1] and
                    red_lower[2] <= v_med <= red_upper[2]) or
                    (red_lower_2[0] <= h_dom <= red_upper_2[0] and
                    red_lower_2[1] <= s_med <= red_upper_2[1] and
                    red_lower_2[2] <= v_med <= red_upper_2[2])):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 0, 255), 8)
                    cv2.drawContours(image_frame, [box], 0, (0, 0, 255), 2)
                    target[2] = 2
                elif (green_lower[0] <= h_dom <= green_upper[0] and
                    green_lower[1] <= s_med <= green_upper[1] and
                    green_lower[2] <= v_med <= green_upper[2]):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 255, 0), 8)
                    cv2.drawContours(image_frame, [box], 0, (0, 255, 0), 2)
                    target[2] = 4
                elif (blue_lower[0] <= h_dom <= blue_upper[0] and
                    blue_lower[1] <= s_med <= blue_upper[1] and
                    blue_lower[2] <= v_med <= blue_upper[2]):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (255, 0, 0), 8)
                    cv2.drawContours(image_frame, [box], 0, (255, 0, 0), 2)
                    target[2] = 1
                elif (orange_lower[0] <= h_dom <= orange_upper[0] and
                    orange_lower[1] <= s_med <= orange_upper[1] and
                    orange_lower[2] <= v_med <= orange_upper[2]):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 122, 255), 8)
                    cv2.drawContours(image_frame, [box], 0, (0, 122, 255), 2)
                    target[2] = 5
                elif (yellow_lower[0] <= h_dom <= yellow_upper[0] and
                    yellow_lower[1] <= s_med <= yellow_upper[1] and
                    yellow_lower[2] <= v_med <= yellow_upper[2]):
                    image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 255, 255), 8)
                    cv2.drawContours(image_frame, [box], 0, (0, 255, 255), 2)
                    target[2] = 3
                else:
                    cv2.drawContours(image_frame, [box], 0, (0, 0, 0), 2)
                    counter -= 1

    for target in targets:
        if target[2] < 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 10, (0, 0, 0), 8)

    return counter

def is_same(last_wall):
    i = 0
    while i < 9:
        if not targets[i][2] == last_wall[i][2]:
            return False
        i += 1
    return True

def generate_solution():
    global cube
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

    formatted = ' '.join(cube_string[i:i + 9] for i in range(0, len(cube_string), 9))
    print(formatted)
    print(Counter(cube_string))

    try:
        cube_solution = kociemba.solve(cube_string)
        print(cube_solution)
    except:
        print("Invalid cube!!!")

def square_finder(image_frame, isConfigurable):
    global targets

    #img_hsv = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    #if isConfigurable:
    #    l_h = cv2.getTrackbarPos("L-H", "Trackbars")
    #    l_s = cv2.getTrackbarPos("L-S", "Trackbars")
    #    l_v = cv2.getTrackbarPos("L-V", "Trackbars")
    #    h_h = cv2.getTrackbarPos("H-H", "Trackbars")
    #    h_s = cv2.getTrackbarPos("H-S", "Trackbars")
    #    h_v = cv2.getTrackbarPos("H-V", "Trackbars")

    #    lower = np.array([l_h, l_s, l_v])
    #    upper = np.array([h_h, h_s, h_v])
    #else:
    #    lower = np.array([0, 0, 0])
    #    upper = np.array([179, 255, 115])

    #mask = cv2.inRange(equalized_image, lower, upper)

    #kernel = np.ones((3, 3), np.uint8)
    #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    img_grey = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    equalized_image = clahe.apply(img_grey)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    background = cv2.morphologyEx(equalized_image, cv2.MORPH_DILATE, kernel)
    shadow_removed = cv2.subtract(background, equalized_image)

    blur = cv2.GaussianBlur(shadow_removed, (9, 9), 0)
    sharpened_image = cv2.addWeighted(shadow_removed, 2.0, blur, -0.5, 0)

    bilateral_filter = cv2.bilateralFilter(sharpened_image, 7, 50, 50)

    median = np.median(bilateral_filter)

    lower = int(max(0, 0.66 * median))
    upper = int(max(255, 1.33 * median))
    
    segmented_map = cv2.Canny(bilateral_filter, lower, upper)
    segmented_map = cv2.dilate(segmented_map, None, iterations=2)

    cv2.imshow("segmented_map", segmented_map)

    contours, _ = cv2.findContours(segmented_map, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    filtered_contours = []

    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 2000 or area > 15000:
            continue

        rect = cv2.minAreaRect(contour)
        (w, h) = rect[1]

        if w == 0 or h == 0:
            continue

        aspectRatio = max(w, h) / min(w, h)

        if aspectRatio < 1.3:
            box = cv2.boxPoints(rect)
            box = box.astype(int)
            #cv2.drawContours(image_frame, [box], 0, (0, 0, 255), 2)

            x,y,w,h = cv2.boundingRect(contour)

            count = 0
            for target in targets:
                if x <= target[0] <= x + w and y <= target[1] <= y + h:
                    count += 1

            if count == 1:
                filtered_contours.append(contour)

    #for contour in filtered_contours:
        #rect = cv2.minAreaRect(contour)
        #box = cv2.boxPoints(rect)
        #box = box.astype(int)
        #cv2.drawContours(image_frame, [box], 0, (0, 255, 0), 2)

    return filtered_contours

def nothing(x):
    pass

def cube_solver():
    global cube, middle, gap, targets, is_recognized

    cv2.namedWindow("Trackbars")
    cv2.createTrackbar("L-H", "Trackbars", 0, 179, nothing)
    cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("L-V", "Trackbars", 0, 255, nothing)
    cv2.createTrackbar("H-H", "Trackbars", 179, 179, nothing)
    cv2.createTrackbar("H-S", "Trackbars", 255, 255, nothing)
    cv2.createTrackbar("H-V", "Trackbars", 115, 255, nothing)

    is_saved = [False] * 6
    last_wall = None
    wall_counter = 0
    counter = 0

    webcam = cv2.VideoCapture(0)

    while wall_counter < 6:
        ret, image_frame = webcam.read()
        if ret:
            middle = [int(image_frame.shape[1] / 2), int(image_frame.shape[0] / 2)]
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
            is_recognized = True

            squares = square_finder(image_frame, True)

            cell_counter = read_colors(image_frame, squares)

            last_wall = targets

            image_frame = cv2.flip(image_frame, 1)

            cv2.imshow("Color Detection", image_frame)

            #if cell_counter == 9 and is_same(last_wall):
                #counter += 1

            if cell_counter == 9 and not is_saved[targets[4][2]]:
                is_saved[targets[4][2]] = True
                cube[targets[4][2]][0][0] = targets[0][2]
                cube[targets[4][2]][0][1] = targets[1][2]
                cube[targets[4][2]][0][2] = targets[2][2]
                cube[targets[4][2]][1][0] = targets[3][2]
                cube[targets[4][2]][1][1] = targets[4][2]
                cube[targets[4][2]][1][2] = targets[5][2]
                cube[targets[4][2]][2][0] = targets[6][2]
                cube[targets[4][2]][2][1] = targets[7][2]
                cube[targets[4][2]][2][2] = targets[8][2]
                wall_counter += 1
                print("Wall " + str(wall_counter) + " saved!!!")
                counter = 0

        else:
            print("Image reading error!!!")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    generate_solution()
    webcam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()