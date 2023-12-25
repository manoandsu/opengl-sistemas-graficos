import numpy as np

def translation_matrix(x, y, z):
    return np.array([
        [1, 0, 0, x],
        [0, 1, 0, y],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ], dtype=np.float32).T

def scale_matrix(scale_x, scale_y, scale_z):
    return np.array([
        [scale_x, 0, 0, 0],
        [0, scale_y, 0, 0],
        [0, 0, scale_z, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32)

def rotation_matrix(angle, axis):
    axis /= np.linalg.norm(axis)
    rad_angle = np.radians(angle)
    cos = np.cos(rad_angle)
    sin = np.sin(rad_angle)
    t = 1 - cos

    x, y, z = axis

    return np.array([
        [cos + x**2 * t, x * y * t - z * sin, x * z * t + y * sin, 0],
        [y * x * t + z * sin, cos + y**2 * t, y * z * t - x * sin, 0],
        [z * x * t - y * sin, z * y * t + x * sin, cos + z**2 * t, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32).T

def ortho_matrix(l, r, b, t, n, f):
    return  np.array([
        [2.0/(r-l), 0, 0, 0],
        [0, 2.0/(t-b), 0, 0],
        [(r+l)/(r-l), (t+b)/(t-b), -(f+n)/(f-n), -1],
        [0, 0, -(2)/(f-n), 0]
    ], dtype=np.float32)
