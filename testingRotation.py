import cv2
import numpy as np

# Load your image into a NumPy array
image = cv2.imread('C://whySpace//BrownPy.png')

# Define the rotation angle in degrees
angle_degrees = 5

# Get the image dimensions
height, width, _ = image.shape  # Assuming a 3-channel color image, use image.shape[:2] for grayscale

# Calculate the rotation matrix
rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle_degrees, 1)

# Apply the rotation to the image using warpAffine
rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

# Find the new bounding box after rotation
cos_theta = np.abs(rotation_matrix[0, 0])
sin_theta = np.abs(rotation_matrix[0, 1])
new_width = int(height * sin_theta + width * cos_theta)
new_height = int(height * cos_theta + width * sin_theta)

print(width, height)
print(new_width, new_height)

# Calculate the cropping coordinates
crop_x1 = (new_width - width) // 2
crop_x2 = width - crop_x1
crop_y1 = (new_height - height) // 2
crop_y2 = height - crop_y1

print(crop_x1, crop_x2)
print(crop_y1, crop_y2)

# Crop the rotated image to the new dimensions
cropped_rotated_image = rotated_image[crop_y1:crop_y2, crop_x1:crop_x2]

# cropped_rotated_image now contains the rotated and cropped image

# If you want to display the cropped and rotated image, you can use OpenCV:
cv2.imshow('Cropped and Rotated Image', cropped_rotated_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(rotation_matrix)