# Your Agent for solving Raven's Progressive Matrices. You MUST modify this file.
#
# You may also create and submit new files in addition to modifying this file.
#
# Make sure your file retains methods with the signatures:
# def __init__(self)
# def Solve(self,problem)
#
# These methods will be necessary for the project's main method to run.

# Install Pillow and uncomment this line to access image processing.
from PIL import Image
import numpy as np
import cv2


class Agent:
    # The default constructor for your Agent. Make sure to execute any
    # processing necessary before your Agent starts solving problems here.
    #
    # Do not add any variables to this signature; they will not be used by
    # main().
    def __init__(self):
        self.question_set = {}
        self.answer_set = {}
        self.methods2x2 = [self.method2x2_compare_same, self.method2x2_move, self.method2x2_add_pixel]
        self.methods3x3 = []
        self.score = 0
        self.answer = 1

    # The primary method for solving incoming Raven's Progressive Matrices.
    # For each problem, your Agent's Solve() method will be called. At the
    # conclusion of Solve(), your Agent should return an int representing its
    # answer to the question: 1, 2, 3, 4, 5, or 6. Strings of these ints 
    # are also the Names of the individual RavensFigures, obtained through
    # RavensFigure.getName(). Return a negative number to skip a problem.
    #
    # Make sure to return your answer *as an integer* at the end of Solve().
    # Returning your answer as a string may cause your program to crash.

    def Solve(self, problem):

        self.read_img(problem)

        if problem.problemType == '2x2':
            self.solve_2by2()
        elif problem.problemType == '3x3':
            self.solve_3by3()

        answer = self.answer
        print(self.answer)
        # print(self.score)
        self.__init__()
        return int(answer)

    def solve_2by2(self):
        for method in self.methods2x2:
            method()
            if self.score == 10:
                break

    def solve_3by3(self):
        pass

    def read_img(self, problem):

        for key in problem.figures:
            img = cv2.imread(problem.figures[key].visualFilename)

            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            _, threshold = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

            pixels = np.count_nonzero(threshold < 255)
            pixels = round(pixels, -2)

            contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            figure = {}
            circle = 5

            if len(contours) > 1:
                contours = contours[1:]

            for contour in contours:
                approx = cv2.approxPolyDP(
                    contour, 0.01 * cv2.arcLength(contour, True), True)

                c = cv2.moments(contour)
                if c['m00'] != 0.0:
                    x = round(int(c['m10'] / c['m00']), -1)
                    y = round(int(c['m01'] / c['m00']), -1)

                # check -----------------------------------
                if len(approx) < 10:
                    figure[len(approx)] = (x, y)
                else:
                    circle += 5
                    figure[circle] = (x, y)

            if ord(key) >= ord("A"):
                self.question_set[key] = {'figure': figure, 'pixel': pixels}
            else:
                self.answer_set[key] = {'figure': figure, 'pixel': pixels}

    def method2x2_compare_same(self):
        a_shapes = self.question_set['A']
        b_shapes = self.question_set['B']
        c_shapes = self.question_set['C']

        if a_shapes['figure'] == b_shapes['figure']:

            for key in self.answer_set:
                pixel_diff1 = abs(a_shapes['pixel'] - b_shapes['pixel'])
                pixel_diff2 = abs(c_shapes['pixel'] - self.answer_set[key]['pixel'])
                if c_shapes['figure'] == self.answer_set[key]['figure']:

                    if abs(pixel_diff1 - pixel_diff2) < 5000:
                        self.score = 10
                        self.answer = key
                        return
                    elif self.score < 5:
                        self.score = 5
                        self.answer = key

        if a_shapes['figure'] == c_shapes['figure']:

            for key in self.answer_set:
                pixel_diff1 = abs(a_shapes['pixel'] - c_shapes['pixel'])
                pixel_diff2 = abs(b_shapes['pixel'] - self.answer_set[key]['pixel'])

                if b_shapes['figure'] == self.answer_set[key]['figure']:
                    if abs(pixel_diff1 - pixel_diff2) < 5000:
                        self.score = 10
                        self.answer = key
                        return
                    elif self.score < 5:
                        self.score = 5
                        self.answer = key

    def method2x2_move(self):
        movement = []

        a_shapes = self.question_set['A']
        b_shapes = self.question_set['B']
        c_shapes = self.question_set['C']

        for key in a_shapes['figure']:
            if key in b_shapes['figure']:
                movement.append((a_shapes['figure'][key][0] - b_shapes['figure'][key][0],
                                 a_shapes['figure'][key][1] - b_shapes['figure'][key][1]))

        for key in c_shapes['figure']:

            for key2 in self.answer_set:
                movement2 = []

                pixel_diff1 = abs(a_shapes['pixel'] - b_shapes['pixel'])
                pixel_diff2 = abs(c_shapes['pixel'] - self.answer_set[key2]['pixel'])

                if key in self.answer_set[key2]['figure']:
                    movement2.append((c_shapes['figure'][key][0] - self.answer_set[key2]['figure'][key][0],
                                      c_shapes['figure'][key][1] - self.answer_set[key2]['figure'][key][1]))

                if movement2 == movement and len(movement) > 0:
                    if abs(pixel_diff1 - pixel_diff2) < 300:
                        self.score = 10
                        self.answer = key2
                        return
                    elif self.score < 5:
                        self.score = 5
                        self.answer = key

        movement = []
        for key in a_shapes['figure']:
            if key in c_shapes['figure']:
                movement.append((a_shapes['figure'][key][0] - c_shapes['figure'][key][0],
                                 a_shapes['figure'][key][1] - c_shapes['figure'][key][1]))

        for key in b_shapes['figure']:

            for key2 in self.answer_set:
                movement2 = []

                pixel_diff1 = abs(a_shapes['pixel'] - c_shapes['pixel'])
                pixel_diff2 = abs(b_shapes['pixel'] - self.answer_set[key2]['pixel'])

                if key in self.answer_set[key2]['figure']:
                    movement2.append((b_shapes['figure'][key][0] - self.answer_set[key2]['figure'][key][0],
                                      b_shapes['figure'][key][1] - self.answer_set[key2]['figure'][key][1]))

                if movement2 == movement and len(movement) > 0:
                    if abs(pixel_diff1 - pixel_diff2) < 300:
                        self.score = 10
                        self.answer = key2
                        return
                    elif self.score < 5:
                        self.score = 5
                        self.answer = key

    def method2x2_add_pixel(self):
        a_pixel = self.question_set['A']['pixel']
        b_pixel = self.question_set['B']['pixel']
        c_pixel = self.question_set['C']['pixel']

        pixel_diff1 = abs(a_pixel - b_pixel)

        for key in self.answer_set:
            pixel_diff = abs(c_pixel - self.answer_set[key]['pixel'])
            if abs(pixel_diff1 - pixel_diff) < 200 and self.score < 8:
                self.score = 8
                self.answer = key
            elif abs(pixel_diff1 - pixel_diff) < 2000 and self.score < 4:
                self.score = 4
                self.answer = key

        pixel_diff2 = abs(a_pixel - c_pixel)

        for key in self.answer_set:
            pixel_diff = abs(b_pixel - self.answer_set[key]['pixel'])

            if abs(pixel_diff2 - pixel_diff) < 200 and self.score < 8:
                self.score = 8
                self.answer = key
            elif abs(pixel_diff2 - pixel_diff) < 2000 and self.score < 4:
                self.score = 4
                self.answer = key
