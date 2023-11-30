import cv2
import numpy as np
from pptx.util import Inches

from picture import get_image_resolution


def get_largest_white_region(image_path):
    image = cv2.imread(image_path)  # 图片转换
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)  # 彩色转换为灰度图像

    # 调整白色颜色范围
    lower_white = np.array([0, 0, 230])
    upper_white = np.array([10, 10, 255])

    mask = cv2.inRange(hsv, lower_white, upper_white)
    result = cv2.bitwise_and(image, image, mask=mask)

    gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    max_area = 0
    max_contour = None

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_contour = contour

    if max_contour is not None:
        x, y, w, h = cv2.boundingRect(max_contour)
        largest_white_region = (x, y, w, h)
    else:
        largest_white_region = None

    return largest_white_region


slide_w = Inches(10)

slide_h = Inches(7.5)


def get_largest_white_region_in_slide(image_path):
    largest_white_region = get_largest_white_region(image_path)
    if largest_white_region == None:
        return None
    width, height = get_image_resolution(image_path)
    box_x = (largest_white_region[0] / width) * slide_w.inches
    box_y = (largest_white_region[1] / height) * slide_h.inches
    box_w = (largest_white_region[2] / width) * slide_w.inches
    box_h = (largest_white_region[3] / height) * slide_h.inches
    return box_x, box_y, box_w, box_h


def draw_rectangles(image_path, regions):
    image = cv2.imread(image_path)

    if regions is not None:
        for region in regions:
            x, y, w, h = region
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Image with white regions", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    image_path = "pptx_static/static/bg/pencil/1_191224140551_1-1.jpg"
    largest_white_region = get_largest_white_region(image_path)
    box_x, box_y, box_w, box_h = get_largest_white_region_in_slide(image_path)
    print(box_x, box_y, box_w, box_h)
    if largest_white_region is not None:
        draw_rectangles(image_path, [largest_white_region])
    else:
        print("No white region found.")
