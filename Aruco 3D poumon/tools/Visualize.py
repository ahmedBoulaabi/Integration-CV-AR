import cv2
import numpy as np

axis_axis = np.float32([[0,0,0], [0.03,0,0],[0,0.03,0],[0,0,0.03]]).reshape(-1,3)
def draw_axis(img, rvecs, tvecs, mtx, dist):
    imgpts, jac = cv2.projectPoints(axis_axis, rvecs, tvecs, mtx, dist)
    imgpts = np.int32(imgpts).reshape(-1, 2)  # Reshape and convert to integer

    img = cv2.line(img, tuple(imgpts[0]), tuple(imgpts[1]), (255, 0, 0), 5)  # X-axis in red
    img = cv2.line(img, tuple(imgpts[0]), tuple(imgpts[2]), (0, 255, 0), 5)  # Y-axis in green
    img = cv2.line(img, tuple(imgpts[0]), tuple(imgpts[3]), (0, 0, 255), 5)  # Z-axis in blue

    return img