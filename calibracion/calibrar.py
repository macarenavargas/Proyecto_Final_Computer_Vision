import cv2
print("OpenCV should be 4.8.0.76 Current version:", cv2.__version__)
from typing import List
import numpy as np
import imageio.v2 as imageio
import cv2
import copy
import glob
import os


def load_images(filenames: List[str]) -> List[np.ndarray]:
    return [imageio.imread(filename) for filename in filenames]

imgs_path = []
for i in range(1,24):
    if i < 10:
        nombre = f"img_chess_0{i}.png"
    else:
        nombre = f"img_chess_{i}.png"

    path = f".\data\{nombre}"
    imgs_path.append(path)

imgs = load_images(imgs_path)
# TODO Find corners with cv2.findChessboardCorners()

# Hemos comprobado que el patrón está formado por 8 filas y 6 columnas de esquinas
size = (9, 6)

# Pasamos las imágenes a escala de grises para poder usar la función cv2.cornerSubPix()
imgs_gray = imgs# [cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) for img in imgs]

# Buscamos el patrón de calibración en cada imagen en escala de grises
corners = [cv2.findChessboardCorners(img, size) for img in imgs_gray]

corners_copy = copy.deepcopy(corners)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.01)

# TODO To refine corner detections with cv2.cornerSubPix() you need to input grayscale images. Build a list containing grayscale images.
corners_refined = [cv2.cornerSubPix(i, cor[1], (9, 6), (-1, -1), criteria) if cor[0] else None 
                   for i, cor in zip(imgs_gray, corners_copy)]


# Hacemos una copia para no perder las imágenes originales con la función cv2.drawChessboardCorners()
imgs_copy = copy.deepcopy(imgs)

# TODO Use cv2.drawChessboardCorners() to draw the cornes
drawed_corners = [cv2.drawChessboardCorners(img, size, corner, True) for img, corner in zip(imgs_copy, corners_refined) if corner is not None]

# TODO Show images and save when needed
def show_image(img, img_name = "imagen"):
    cv2.imshow(img_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
def write_image(img, output_folder, i):
    os.makedirs(output_folder, exist_ok=True) 
    img_name = f"{output_folder}/corners_{i}.jpg"
    cv2.imwrite(img_name, img)

'''
output_folder = "../data/output_left_corners"
os.makedirs(output_folder, exist_ok=True)
for i, img in enumerate(drawed_corners):
    show_image(img)
    write_image(img, output_folder, i)
'''

# TODO Design the method. It should return a np.array with np.float32 elements
def get_chessboard_points(chessboard_shape, dx, dy):
    cols, rows = chessboard_shape
    matrix = [(i*dx, j*dy, 0) for j in range(rows) for i in range(cols)]
    return np.array(matrix, np.float32)

# TODO You need the points for every image, not just one (consider a list comprehension)
chessboard_points = [get_chessboard_points((9, 6), 30, 30) for _ in range(len(imgs_gray))]


# Filter data and get only those with adequate detections
valid_corners = [cor[1] for cor in corners if cor[0]]
# Convert list to numpy array
valid_corners = np.asarray(valid_corners, dtype=np.float32)

# TODO
img_size = (np.array(imgs_gray)[0].shape[1], np.array(imgs_gray)[0].shape[0])
rms, intrinsics, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(chessboard_points, valid_corners, img_size, None, None)
# Obtain extrinsics
extrinsics = list(map(lambda rvec, tvec: np.hstack((cv2.Rodrigues(rvec)[0], tvec)), rvecs, tvecs))

# Print outputs
print("Intrinsics:\n", intrinsics)
print("Distortion coefficients:\n", dist_coeffs)
print("Root mean squared reprojection error:\n", rms)


np.savez('calibracion/parametros.npz', intrinsics=intrinsics, dist_coeffs=dist_coeffs)