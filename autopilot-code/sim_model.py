import os
import numpy as np
from keras.models import load_model
import cv2

import matplotlib.pyplot as plt

def detect_line_segments(image):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # distance precision in pixel, i.e. 1 pixel
    angle = 0.5 * np.pi / 180  # angular precision in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv2.HoughLinesP(image, rho, angle, min_threshold,
                                    np.array([]), minLineLength=8, maxLineGap=4)

    return line_segments

def make_points(image, line):
    height, width = image.shape
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = 0  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def average_slope_intercept(image, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    lane_lines = []
    if line_segments is None:
        return lane_lines

    height, width = image.shape
    left_fit = []
    right_fit = []
    ver_lines = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if (x1 == x2):
                continue

            if (y1 - y2 < 10) and (y1 - y2 > -10):
                continue
            ver_lines.append(line_segment)

            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]



            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))
    image_x = display_lines(image, ver_lines)
    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 1:
        lane_lines.append(make_points(image, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 1:
        lane_lines.append(make_points(image, right_fit_average))
    return lane_lines

def display_lines(image, lines, line_color=(255, 255, 255), line_width=3):
    line_image = np.zeros_like(image)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(image, 1, line_image, 0.5, 1)
    return line_image

def img_preprocess(image):
    height, _, _ = image.shape
    image = image[int(height / 2):, :, :]  # remove top half of the image, as it is not relevant for lane following
    image = cv2.cvtColor(image, cv2.COLOR_RGB2YUV)  # Nvidia model said it is best to use YUV color space
    image = cv2.GaussianBlur(image, (3, 3), 0)  # Blurs image
    #cv2.imshow('image', image)
    image_grey = np.uint8(image)
    #cv2.imshow('image_grey', image_grey)
    image_edge = cv2.Canny(image_grey, 200, 400)  # detects line edges (lanes)
    #cv2.imshow('canny', image_edge)
    line_segments = detect_line_segments(image_edge)  # detects line segemnts (combines edge pixels into a cohesive line)
    lane_lines = average_slope_intercept(image_edge, line_segments)
    image = display_lines(image, lane_lines)
    #cv2.imshow('final', image)
    image = cv2.resize(image, (200, 66))  # input image size (200,66) Nvidia model
    # image = image / 255  # normalizing
    return image

def main():
    model = load_model('lane_navigation_check_pre.h5')
    model.summary()
    image = plt.imread(os.path.join('data', 'LiveSteamOutput.png'))

    preprocessed = img_preprocess(image)
    X = np.asarray([preprocessed]) # adds batch dimensions
    prediction = model.predict(X)
    print(prediction)
    angle = prediction.item(0)
    speed = prediction.item(1)

if __name__ == '__main__':
    main()