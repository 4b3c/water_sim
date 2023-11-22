import numpy as np
import angled_waves as aw
import cv2
import pygame
import random

pygame.init()
clock = pygame.time.Clock()

seed = [random.randint(1, 10000000)]
curr_seed_index = 0
print(curr_seed_index, ":", seed[curr_seed_index])
random.seed(seed[curr_seed_index])

window = pygame.display.set_mode((1000, 800))
wave_window = (800, 600)
running = True
unclicked = True
displacement = 1
images = []
x = 0


def replace_pixels(image_array, threshold, greater, channel_to_check, replacement_color):
    r_channel = image_array[:, :, channel_to_check]
    
    if greater:
	    pixels_to_replace = r_channel > threshold
    else:
	    pixels_to_replace = r_channel < threshold

    image_array[pixels_to_replace, 0] = replacement_color[0]
    image_array[pixels_to_replace, 1] = replacement_color[1]
    image_array[pixels_to_replace, 2] = replacement_color[2]
    
    return image_array

def fill_waves_list():
	return [aw.wave(random.randint(0, 360), (800, 600), random.randint(10, 20), random.uniform(0.05, 3.05), np.array([0.2, 0.3, 0.3])) for _ in range(6)]
	# return [aw.wave(random.randint(0, 360), (800, 600), random.randint(10, 350), random.uniform(0.05, 3.05), np.random.rand((3))) for _ in range(6)]

# waves = fill_waves_list()

waves = [aw.wave(12, wave_window, 90, 3, np.array([0.5, 0.2, 0.5])),
		 aw.wave(89, wave_window, 90, 5, np.array([0.5, 0.2, 0.1])),
		 aw.wave(236, wave_window, 90, 2, np.array([0.5, 0.2, 0.5])),
		 aw.wave(32, wave_window, 90, 7, np.array([0.5, 0.2, 0.5]))
		]

increasing = True
borderThing = 2

while running:
	window.fill((15, 45, 95));

	displacement += 0.07

	if increasing:
		borderThing += 0.09
	else:
		borderThing -= 0.09
	if borderThing * 50 > 295 or borderThing * 50 < 50:
		increasing = not increasing

	deriv_arrays = np.zeros((wave_window[0], wave_window[1], 3), dtype=np.uint8)
	for wave in waves:
		wave.generate_wave(displacement)
		deriv_arrays += wave.deriv_array

	deriv_arrays = replace_pixels(deriv_arrays, int(min(borderThing * 50, 255)), True, 0, np.array([70, 190, 195]))
	deriv_arrays = replace_pixels(deriv_arrays, int(min(borderThing * 50, 255)), True, 1, np.array([70, 190, 195]))
	deriv_arrays = replace_pixels(deriv_arrays, int(min(borderThing * 50, 255)), True, 2, np.array([70, 190, 195]))

	# deriv_arrays = replace_pixels(deriv_arrays, 43, False, 0, np.array([190, 30, 40]))
	# deriv_arrays = replace_pixels(deriv_arrays, 53, False, 1, np.array([190, 30, 40]))
	# deriv_arrays = replace_pixels(deriv_arrays, 65, False, 2, np.array([190, 30, 40]))

	# deriv_arrays = np.where(np.logical_and(deriv_arrays > 200, deriv_arrays < 255), 75, deriv_arrays)
	# deriv_arrays = np.where(np.logical_and(deriv_arrays > 150, deriv_arrays < 200), 215, deriv_arrays)
	# deriv_arrays = np.where(np.logical_and(deriv_arrays > 100, deriv_arrays < 150), 75, deriv_arrays)
	# deriv_arrays = np.where(np.logical_and(deriv_arrays > 50, deriv_arrays < 100), 0, deriv_arrays)
	# deriv_arrays = np.where(np.logical_and(deriv_arrays > 0, deriv_arrays < 50), 75, deriv_arrays)
	
	image = pygame.surfarray.make_surface(deriv_arrays)
	images.append(cv2.cvtColor(deriv_arrays, cv2.COLOR_BGR2RGB))
	window.blit(image, (100, 100))

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	keys_pressed = pygame.key.get_pressed()

	# x += 1
	if (keys_pressed[pygame.K_RIGHT] and unclicked) or x == 5:
		x = 0
		unclicked = False
		images = []
		curr_seed_index += 1
		if curr_seed_index > len(seed) - 1:
			seed.append(random.randint(1, 10000000))
		print(curr_seed_index, ":", seed[curr_seed_index])
		random.seed(seed[curr_seed_index])
		waves = fill_waves_list()

	elif keys_pressed[pygame.K_LEFT] and unclicked:
		unclicked = False
		images = []
		curr_seed_index -= 1
		print(curr_seed_index, ":", seed[curr_seed_index])
		random.seed(seed[curr_seed_index])
		waves = fill_waves_list()

	else:
		unclicked = True

	# clock.tick()
	# print("FPS:", int(clock.get_fps()))


video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (images[0].shape[1], images[0].shape[0]))

for image in images:
	video_writer.write(image)

video_writer.release()