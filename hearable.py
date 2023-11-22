import numpy as np
import angled_waves as aw
import cv2
import pygame
import random
import sounddevice as sd

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

sample_rate = 44100
duration = 1/25
volume = 0.1
t = np.arange(int(sample_rate * duration))




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

def fill_waves_list(color=np.array([0.2, 0.3, 0.3]), randColor=np.random.rand((3))):
	return [aw.wave(random.randint(0, 360), (800, 600), random.randint(10, 20), random.uniform(0.05, 3.05), color) for _ in range(6)]

# waves = fill_waves_list()

waves = [aw.wave(12, wave_window, 90, 3, np.array([0.5, 0.2, 0.5])),
		 aw.wave(89, wave_window, 90, 5, np.array([0.5, 0.2, 0.1])),
		 aw.wave(236, wave_window, 90, 2, np.array([0.5, 0.2, 0.5])),
		 aw.wave(32, wave_window, 90, 7, np.array([0.5, 0.2, 0.5]))
		]


while running:
	window.fill((15, 45, 95));

	displacement += 0.07

	deriv_arrays = np.zeros((wave_window[0], wave_window[1], 3), dtype=np.uint8)
	for wave in waves:
		wave.generate_wave(displacement)
		deriv_arrays += wave.deriv_array

	# deriv_arrays = replace_pixels(deriv_arrays, int(min(borderThing * 50, 255)), True, 0, np.array([70, 190, 195]))
	# deriv_arrays = replace_pixels(deriv_arrays, int(min(borderThing * 50, 255)), True, 1, np.array([70, 190, 195]))
	# deriv_arrays = replace_pixels(deriv_arrays, int(min(borderThing * 50, 255)), True, 2, np.array([70, 190, 195]))

	image = pygame.surfarray.make_surface(deriv_arrays)
	images.append(cv2.cvtColor(deriv_arrays, cv2.COLOR_BGR2RGB))
	window.blit(image, (100, 100))

	frequency = 200
	col_input = 2 * np.pi * t * frequency / sample_rate
	raw_data = np.sin(col_input) * volume
	sd.play(raw_data, sample_rate)




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


# frequencies = np.array([np.sum(images[-1][0]) for image in images])
# frequencies1 = np.array([np.sum(image[15][0]) for image in images])
# frequencies2 = np.array([np.sum(image[25][0]) for image in images])
# # each frequency should last the time duration of a frame


# sample_rate = 44100
# duration = 1/25
# volume = 0.1

# t = np.arange(int(sample_rate * duration))

# col_input = 2 * np.pi * t * frequencies[0] / sample_rate
# col_input += 2 * np.pi * t * frequencies1[0] / sample_rate
# col_input += 2 * np.pi * t * frequencies2[0] / sample_rate

# for i in range(1, len(frequencies) - 1):
# 	plus = 2 * np.pi * t * frequencies[i] / sample_rate
# 	plus += 2 * np.pi * t * frequencies1[i] / sample_rate
# 	plus += 2 * np.pi * t * frequencies2[i] / sample_rate

# 	col_input = np.append(col_input, plus)

# raw_data = np.sin(col_input) * volume

# print(len(col_input))
# print(len(frequencies))

# sd.play(raw_data, sample_rate)
# sd.wait()


# # video_writer = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 25, (images[0].shape[1], images[0].shape[0]))

# # for image in images:
# # 	video_writer.write(image)

# # video_writer.release()