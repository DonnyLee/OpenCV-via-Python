#   computer graphics
import numpy as np  # needed for OpenCV
import cv2 as cv    # this is OpenCV

#   auxiliary functions
import sys          # for standard output and exit.


class Webcam:
    def __init__(self, webcam_id=0):
        self.window_name = "Donny's Webcam App via OpenCV"
        self.wc = cv.VideoCapture(webcam_id)
        self.frame = None
        self.mode = 0
        self.b_mode_changed = False

        cv.namedWindow(self.window_name)

    def load_gui_elements(self):
        if self.mode is 1 or 2:
            cv.createTrackbar("canny_min_threshold", self.window_name, 0, 255, self.alter_canny)
            cv.createTrackbar("canny_max_threshold", self.window_name, 0, 255, self.alter_canny)
            cv.setTrackbarPos("canny_min_threshold", self.window_name, 50)
            cv.setTrackbarPos("canny_max_threshold", self.window_name, 150)
        else:
            # delete all elements
            self.reset_window()
            pass

    def reset_window(self):
        cv.destroyWindow(self.window_name)
        cv.namedWindow(self.window_name)

    def stream_on_window(self):
        while True:
            self.apply_mode()
            if self.b_mode_changed:
                self.load_gui_elements()
                self.b_mode_changed = False

            self.key_command()
            cv.imshow(self.window_name, self.frame)

    def apply_mode(self):
        ret, self.frame = self.wc.read()
        if self.mode is 1:
            self.frame = self.alter_canny(cv.getTrackbarPos("canny_min_threshold", self.window_name), cv.getTrackbarPos("canny_max_threshold", self.window_name))
        elif self.mode is 2:

            self.find_lines()
        else:
            # if mode = 0 or not configured key input, then just show original frame
            pass

    def key_command(self):
        key = cv.waitKey(1)
        if key == 27:  # esc
            self.wc.release()
            cv.destroyAllWindows()
            print("good bye")
            sys.exit(0)

        elif key == 32:     # space bar
            self.save_frame()
        elif key == 48:     # number 0 key
            self.b_mode_changed = True
            self.mode = 0
            print("original")
        elif key == 49:     # number 1 key
            self.b_mode_changed = True
            self.mode = 1
            print("mode 1")

        elif key == 50:     # number 2 key
            self.b_mode_changed = True
            self.mode = 2
            print("mode 2")

        elif key == 51:     # number 3 key
            self.b_mode_changed = True
            self.mode = 3
            print("mode 3")

        elif key is not -1:
            print("pressed Key number = " + str(key))
        return False

    def save_frame(self, filename="photo_shot.jpg"):
        cv.imwrite(filename, self.frame)
        print("Picture saved as " + filename)

    def alter_gray(self):
        return cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

    def alter_canny(self, threshold_min=50, threshold_max=150):
        return cv.Canny(self.frame, threshold_min, threshold_max, apertureSize=3)

    def find_lines(self):
        img = self.alter_canny()
        lines = cv.HoughLines(img, 1, np.pi / 180, 200)
        if lines is not None :
            for rho, theta in lines[0]:
                a = np.cos(theta)
                b = np.sin(theta)
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                cv.line(self.frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        else :
            print ("","scanning for line \r")




