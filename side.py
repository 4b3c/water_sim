# import pygame, math
# import numpy as np

# pygame.init()

# window = pygame.display.set_mode((1000, 800))
# running = True
# displacement = 0

# def direction_amount(x):
# 	if x % 3 == 0:
# 		return -1
# 	else:
# 		return x % 2

# def more_waves_with_derivative(position):
# 	pixel_array = pygame.PixelArray(window)
# 	for x in range(100, 900):
# 		h = 0
# 		dh = 0
# 		for y in range(1, 8):
# 			position_mod = position * direction_amount(y) * (30 / (y + 1))
# 			x_mod = x * 1.2
# 			y_mod = 33 / (y + 0.1)

# 			c = math.e**math.sin((x_mod + position_mod) * (y / 300)) * y_mod
# 			h -= c
# 			dh -= c * y * y * math.cos((x_mod + position_mod) * (y / 300)) * y_mod

# 		derivative_clamp = min(max(dh / 60, -125), 100) + 155
# 		pixel_array[x, 200 + int(h / 5):600 - int(h / 5)] = (derivative_clamp*(35/255), derivative_clamp*(137/255), derivative_clamp*(218/255))

# def recreating(position):
# 	pixel_array = pygame.PixelArray(window)


# while running:
# 	window.fill((15, 45, 95));

# 	displacement += 0.3
# 	more_waves_with_derivative(displacement)

# 	pygame.display.update()
# 	for event in pygame.event.get():
# 		if event.type == pygame.QUIT:
# 			quit()




import numpy as np

# Define the input matrix (3x3)
matrix = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

# Specify the rotation angle in degrees
angle_degrees = 45

# Convert the angle to radians
angle_radians = np.deg2rad(angle_degrees)

# Define the rotation matrix (3x3 for a 2D rotation)
rotation_matrix = np.array([[np.cos(angle_radians), -np.sin(angle_radians), 0],
                            [np.sin(angle_radians), np.cos(angle_radians), 0],
                            [0, 0, 1]])

# Apply the rotation to the input matrix
rotated_matrix = np.dot(rotation_matrix, matrix)

print(rotated_matrix)
