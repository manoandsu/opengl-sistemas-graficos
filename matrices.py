import numpy as np

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
    cos_a = np.cos(rad_angle)
    sin_a = np.sin(rad_angle)
    t = 1 - cos_a

    x, y, z = axis

    return np.array([
        [cos_a + x**2 * t, x * y * t - z * sin_a, x * z * t + y * sin_a, 0],
        [y * x * t + z * sin_a, cos_a + y**2 * t, y * z * t - x * sin_a, 0],
        [z * x * t - y * sin_a, z * y * t + x * sin_a, cos_a + z**2 * t, 0],
        [0, 0, 0, 1]
    ], dtype=np.float32).T

def translation_matrix(translation):
    return np.array([
        [1, 0, 0, translation[0]],
        [0, 1, 0, translation[1]],
        [0, 0, 1, translation[2]],
        [0, 0, 0, 1]
    ], dtype=np.float32).T
