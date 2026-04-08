import numpy as np
import cv2
import kociemba
import datetime
import csv
from collections import Counter

results = [[[[] for _ in range(2)]] for _ in range(6)]
stats = [
    ['Kolor', 'Correct', 'Wrong', 'All', 'Highest_H', 'Highest_S','Highest_V', 'Lowest_H', 'Lowest_S', 'Lowest_V'],
    ['White', 0, 0, 0, -1, -1, -1, 256, 256, 256],
    ['Blue', 0, 0, 0, -1, -1, -1, 256, 256, 256],
    ['Red', 0, 0, 0, -1, -1, -1, 256, 256, 256],
    ['Yellow', 0, 0, 0, -1, -1, -1, 256, 256, 256],
    ['Green', 0, 0, 0, -1, -1, -1, 256, 256, 256],
    ['Orange', 0, 0, 0, -1, -1, -1, 256, 256, 256]
]
cube = [[[-1 for _ in range(3)] for _ in range(3)] for _ in range(6)]
limits = [[[0, 27, 17], [5, 225, 255]],
          [[114, 27, 17], [255, 225, 255]],
          [[30, 25, 14], [96, 255, 196]],
          [[106, 122, 25], [118, 255, 226]],
          [[0, 32, 35], [15, 255, 255]],
          [[21, 7, 37], [103, 255, 255]],
          [[0, 0, 16], [174, 145, 255]],
          [[125, 32, 35], [255, 225, 255]]]
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
    import os  # import os module

    directory = 'temp_photos'

    for frame in os.scandir(directory):
        if frame.is_file():
            img = cv2.imread(frame)
            middle = [int(img.shape[1] / 2), int(img.shape[0] / 2)]
            gap = 100

            hsv_frame = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

            red_lower = np.array([limits[0][0][0], limits[0][0][1], limits[0][0][2]], np.uint8)
            red_upper = np.array([limits[0][1][0], limits[0][1][1], limits[0][1][2]], np.uint8)
            red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)

            red_lower = np.array([limits[1][0][0], limits[1][0][1], limits[1][0][2]], np.uint8)
            red_upper = np.array([limits[1][1][0], limits[1][1][1], limits[1][1][2]], np.uint8)
            red_mask_2 = cv2.inRange(hsv_frame, red_lower, red_upper)

            green_lower = np.array([limits[2][0][0], limits[2][0][1], limits[2][0][2]], np.uint8)
            green_upper = np.array([limits[2][1][0], limits[2][1][1], limits[2][1][2]], np.uint8)
            green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

            blue_lower = np.array([limits[3][0][0], limits[3][0][1], limits[3][0][2]], np.uint8)
            blue_upper = np.array([limits[3][1][0], limits[3][1][1], limits[3][1][2]], np.uint8)
            blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

            orange_lower = np.array([limits[4][0][0], limits[4][0][1], limits[4][0][2]], np.uint8)
            orange_upper = np.array([limits[4][1][0], limits[4][1][1], limits[4][1][2]], np.uint8)
            orange_mask = cv2.inRange(hsv_frame, orange_lower, orange_upper)

            yellow_lower = np.array([limits[5][0][0], limits[5][0][1], limits[5][0][2]], np.uint8)
            yellow_upper = np.array([limits[5][1][0], limits[5][1][1], limits[5][1][2]], np.uint8)
            yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)

            white_lower = np.array([limits[6][0][0], limits[6][0][1], limits[6][0][2]], np.uint8)
            white_upper = np.array([limits[6][1][0], limits[6][1][1], limits[6][1][2]], np.uint8)
            white_mask = cv2.inRange(hsv_frame, white_lower, white_upper)

            orange_lower = np.array([limits[7][0][0], limits[7][0][1], limits[7][0][2]], np.uint8)
            orange_upper = np.array([limits[7][1][0], limits[7][1][1], limits[7][1][2]], np.uint8)
            orange_mask_2 = cv2.inRange(hsv_frame, orange_lower, orange_upper)

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
                scale_up = 2
                img = cv2.circle(img, [target[0], target[1]], 10, (0, 0, 0), 8)

                x_start, y_start, x_end, y_end = target[0] - int(gap), target[1] - int(gap), target[0] + int(gap), target[1] + int(gap)
                print(x_start, y_start, x_end, y_end)
                cropped_img = img[y_start:y_end, x_start:x_end]

                cropped_img = cv2.resize(cropped_img, None, fx=scale_up, fy=scale_up, interpolation=cv2.INTER_LINEAR)

                cv2.imshow("Cropped Image", cropped_img)

                key = cv2.waitKey(0) & 0xFF

                if key == ord('w'):
                    stats[1][3] += 1
                    if hsv_frame[target[1], target[0]][0] > stats[1][4]:
                        stats[1][4] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] > stats[1][5]:
                        stats[1][5] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] > stats[1][6]:
                        stats[1][6] = hsv_frame[target[1], target[0]][2]
                    if hsv_frame[target[1], target[0]][0] < stats[1][7]:
                        stats[1][7] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] < stats[1][8]:
                        stats[1][8] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] < stats[1][9]:
                        stats[1][9] = hsv_frame[target[1], target[0]][2]
                    if white_mask[target[1], target[0]] > 0:
                        print("Poprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[0].append([True, hsv_frame[target[1], target[0]]])
                        stats[1][1] += 1
                    else:
                        print("Nieoprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[0].append([False, hsv_frame[target[1], target[0]]])
                        stats[1][2] += 1
                elif key == ord('b'):
                    if hsv_frame[target[1], target[0]][0] > stats[2][4]:
                        stats[2][4] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] > stats[2][5]:
                        stats[2][5] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] > stats[2][6]:
                        stats[2][6] = hsv_frame[target[1], target[0]][2]
                    if hsv_frame[target[1], target[0]][0] < stats[2][7]:
                        stats[2][7] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] < stats[2][8]:
                        stats[2][8] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] < stats[2][9]:
                        stats[2][9] = hsv_frame[target[1], target[0]][2]
                    stats[2][3] += 1
                    if blue_mask[target[1], target[0]] > 0:
                        print("Poprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[1].append([True, hsv_frame[target[1], target[0]]])
                        stats[2][1] += 1
                    else:
                        print("Nieoprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[1].append([False, hsv_frame[target[1], target[0]]])
                        stats[2][2] += 1
                elif key == ord('r'):
                    if hsv_frame[target[1], target[0]][0] > stats[3][4]:
                        stats[3][4] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] > stats[3][5]:
                        stats[3][5] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] > stats[3][6]:
                        stats[3][6] = hsv_frame[target[1], target[0]][2]
                    if hsv_frame[target[1], target[0]][0] < stats[3][7]:
                        stats[3][7] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] < stats[3][8]:
                        stats[3][8] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] < stats[3][9]:
                        stats[3][9] = hsv_frame[target[1], target[0]][2]
                    stats[3][3] += 1
                    if red_mask[target[1], target[0]] > 0 or red_mask_2[target[1], target[0]] > 0:
                        print("Poprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[2].append([True, hsv_frame[target[1], target[0]]])
                        stats[3][1] += 1
                    else:
                        print("Nieoprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[2].append([False, hsv_frame[target[1], target[0]]])
                        stats[3][2] += 1
                elif key == ord('y'):
                    if hsv_frame[target[1], target[0]][0] > stats[4][4]:
                        stats[4][4] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] > stats[4][5]:
                        stats[4][5] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] > stats[4][6]:
                        stats[4][6] = hsv_frame[target[1], target[0]][2]
                    if hsv_frame[target[1], target[0]][0] < stats[4][7]:
                        stats[4][7] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] < stats[4][8]:
                        stats[4][8] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] < stats[4][9]:
                        stats[4][9] = hsv_frame[target[1], target[0]][2]
                    stats[4][3] += 1
                    if yellow_mask[target[1], target[0]] > 0:
                        print("Poprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[3].append([True, hsv_frame[target[1], target[0]]])
                        stats[4][1] += 1
                    else:
                        print("Nieoprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[3].append([False, hsv_frame[target[1], target[0]]])
                        stats[4][2] += 1
                elif key == ord('g'):
                    if hsv_frame[target[1], target[0]][0] > stats[5][4]:
                        stats[5][4] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] > stats[5][5]:
                        stats[5][5] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] > stats[5][6]:
                        stats[5][6] = hsv_frame[target[1], target[0]][2]
                    if hsv_frame[target[1], target[0]][0] < stats[5][7]:
                        stats[5][7] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] < stats[5][8]:
                        stats[5][8] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] < stats[5][9]:
                        stats[5][9] = hsv_frame[target[1], target[0]][2]
                    stats[5][3] += 1
                    if green_mask[target[1], target[0]] > 0:
                        print("Poprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[4].append([True, hsv_frame[target[1], target[0]]])
                        stats[5][1] += 1
                    else:
                        print("Nieoprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[4].append([False, hsv_frame[target[1], target[0]]])
                        stats[5][2] += 1
                elif key == ord('o'):
                    if hsv_frame[target[1], target[0]][0] > stats[6][4]:
                        stats[6][4] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] > stats[6][5]:
                        stats[6][5] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] > stats[6][6]:
                        stats[6][6] = hsv_frame[target[1], target[0]][2]
                    if hsv_frame[target[1], target[0]][0] < stats[6][7]:
                        stats[6][7] = hsv_frame[target[1], target[0]][0]
                    if hsv_frame[target[1], target[0]][1] < stats[6][8]:
                        stats[6][8] = hsv_frame[target[1], target[0]][1]
                    if hsv_frame[target[1], target[0]][2] < stats[6][9]:
                        stats[6][9] = hsv_frame[target[1], target[0]][2]
                    stats[6][3] += 1
                    if orange_mask[target[1], target[0]] > 0 or orange_mask[target[1], target[0]] > 0:
                        print("Poprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[5].append([True, hsv_frame[target[1], target[0]]])
                        stats[6][1] += 1
                    else:
                        print("Nieoprawny odczyt: " + str(hsv_frame[target[1], target[0]]))
                        results[5].append([False, hsv_frame[target[1], target[0]]])
                        stats[6][2] += 1

                cv2.destroyAllWindows()

    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    with open(f"results/{filename}_results.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(results)
    with open(f"stats/{filename}_stats.csv", 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(stats)

def read_colors(image_frame):
    global targets, is_recognized

    hsv_frame = cv2.cvtColor(image_frame, cv2.COLOR_BGR2HSV)

    red_lower = np.array([limits[0][0][0], limits[0][0][1], limits[0][0][2]], np.uint8)
    red_upper = np.array([limits[0][1][0], limits[0][1][1], limits[0][1][2]], np.uint8)
    red_mask = cv2.inRange(hsv_frame, red_lower, red_upper)

    red_lower = np.array([limits[1][0][0], limits[1][0][1], limits[1][0][2]], np.uint8)
    red_upper = np.array([limits[1][1][0], limits[1][1][1], limits[1][1][2]], np.uint8)
    red_mask_2 = cv2.inRange(hsv_frame, red_lower, red_upper)

    green_lower = np.array([limits[2][0][0], limits[2][0][1], limits[2][0][2]], np.uint8)
    green_upper = np.array([limits[2][1][0], limits[2][1][1], limits[2][1][2]], np.uint8)
    green_mask = cv2.inRange(hsv_frame, green_lower, green_upper)

    blue_lower = np.array([limits[3][0][0], limits[3][0][1], limits[3][0][2]], np.uint8)
    blue_upper = np.array([limits[3][1][0], limits[3][1][1], limits[3][1][2]], np.uint8)
    blue_mask = cv2.inRange(hsv_frame, blue_lower, blue_upper)

    orange_lower = np.array([limits[4][0][0], limits[4][0][1], limits[4][0][2]], np.uint8)
    orange_upper = np.array([limits[4][1][0], limits[4][1][1], limits[4][1][2]], np.uint8)
    orange_mask = cv2.inRange(hsv_frame, orange_lower, orange_upper)

    yellow_lower = np.array([limits[5][0][0], limits[5][0][1], limits[5][0][2]], np.uint8)
    yellow_upper = np.array([limits[5][1][0], limits[5][1][1], limits[5][1][2]], np.uint8)
    yellow_mask = cv2.inRange(hsv_frame, yellow_lower, yellow_upper)

    white_lower = np.array([limits[6][0][0], limits[6][0][1], limits[6][0][2]], np.uint8)
    white_upper = np.array([limits[6][1][0], limits[6][1][1], limits[6][1][2]], np.uint8)
    white_mask = cv2.inRange(hsv_frame, white_lower, white_upper)

    orange_lower = np.array([limits[7][0][0], limits[7][0][1], limits[7][0][2]], np.uint8)
    orange_upper = np.array([limits[7][1][0], limits[7][1][1], limits[7][1][2]], np.uint8)
    orange_mask_2 = cv2.inRange(hsv_frame, orange_lower, orange_upper)

    #print(hsv_frame[targets[4][1], targets[4][0]])

    for target in targets:
        if red_mask[target[1], target[0]] > 0 or red_mask_2[target[1], target[0]] > 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 0, 255), 8)
            target[2] = 2
        elif green_mask[target[1], target[0]] > 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 255, 0), 8)
            target[2] = 4
        elif blue_mask[target[1], target[0]] > 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (255, 0, 0), 8)
            target[2] = 1
        elif orange_mask[target[1], target[0]] > 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 122, 255), 8)
            target[2] = 5
        elif yellow_mask[target[1], target[0]] > 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (0, 255, 255), 8)
            target[2] = 3
        elif white_mask[target[1], target[0]] > 0:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 5, (255, 255, 255), 8)
            target[2] = 0
        else:
            image_frame = cv2.circle(image_frame, [target[0], target[1]], 10, (0, 0, 0), 8)
            is_recognized = False

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

    print(cube_string)
    print(Counter(cube_string))

    try:
        cube_solution = kociemba.solve(cube_string)
    except:
        cube_solution = "Invalid cube!!!"

    print(cube_solution)

def cube_solver():
    global cube, middle, gap, targets, is_recognized

    counter = 0
    is_saved = [False] * 6
    wall_counter = 0

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

            read_colors(image_frame)

            image_frame = cv2.flip(image_frame, 1)

            cv2.imshow("Color Detection", image_frame)

            if is_recognized and not is_saved[targets[4][2]]:
                counter += 1
            else:
                counter = 0

            if counter == 25:
                #print(targets[0][2], targets[1][2], targets[2][2])
                #print(targets[3][2], targets[4][2], targets[5][2])
                #print(targets[6][2], targets[7][2], targets[8][2])
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

            cv2.imshow("Color Detection", image_frame)

        else:
            print("Image reading error!!!")

        if cv2.waitKey(10) & 0xFF == ord('q'):
            webcam.release()
            cv2.destroyAllWindows()
            break

    generate_solution()

if __name__ == '__main__':
    main()