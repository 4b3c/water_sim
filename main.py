import pygame, math, numpy

pygame.init()

window = pygame.display.set_mode((1000, 800))
running = True
displacement = 0

def direction_amount(x):
	if x % 3 == 0:
		return -1
	else:
		return x % 2

def two_dim_graph_wave(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(1000):
		h = int(math.e**math.sin((x + position) / 100) * 30)
		h -= int(math.e**math.sin((x - (position * 2 / 7)) / 30) * 10)
		pixel_array[x, 400 - h] = (0, 0, 0)
	pixel_array.close()

def two_dim_flat_graph_wave(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(1000):
		h = int(math.e**math.sin((x + position) / 100) * 30)
		h -= int(math.e**math.sin((x - (position * 2 / 7)) / 30) * 10)
		pixel_array[x, 0:800] = (h + 100, h + 100, h + 100)
	pixel_array.close()

def two_dim_graph_wave_more_waves(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(1000):
		h = 0
		for y in range(1, 12):
			h -= math.e**math.sin(((x + (position * direction_amount(y) * (30/(y+1)))) * y) / 300) * 31 / (y + 0.1)

		clamp = min(max(-h, 0), 255)
		clamp2 = 255 - clamp

		pixel_array[x, 0:400 + int(h)] = (clamp2/3, clamp2/1.9, clamp2/1.4)
		pixel_array[x, 400 + int(h):800] = (clamp/3, clamp/1.9, clamp/1.4)

	pixel_array.close()

def more_waves_with_derivative(position):
	pixel_array = pygame.PixelArray(window)
	# total_dh = 0
	for x in range(1000):
		h = 0
		dh = 0
		for y in range(1, 8):
			position_mod = position * direction_amount(y) * (30 / (y + 1))
			x_mod = x * 1.2
			y_mod = 33 / (y + 0.1)

			c = math.e**math.sin((x_mod + position_mod) * (y / 300)) * y_mod
			h -= c
			dh -= c * y * y * math.cos((x_mod + position_mod) * (y / 300)) * y_mod

		derivative_clamp = min(max(dh / 60, -125), 100) + 155
		pixel_array[x, 250 + int(h):650 + int(h)] = (derivative_clamp*(35/255), derivative_clamp*(137/255), derivative_clamp*(218/255))


		#failed to make it look like it had a fixed length
		# total_dh += abs(dh / 10000)
		# if total_dh >= 70:
		# 	break

def vertical_banner(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(800):
		h = 0
		dh = 0
		for y in range(1, 8):
			position_mod = position * direction_amount(y) * (30 / (y + 1))
			x_mod = x * 1.2
			y_mod = 33 / (y + 0.1)
	
			c = math.e**math.sin((x_mod + position_mod) * (y / 300)) * y_mod
			h -= c
			dh -= c * y * y * math.cos((x_mod + position_mod) * (y / 300)) * y_mod

		derivative_clamp = min(max(dh / 60, -125), 100) + 155
		pixel_array[250 + int(h):850 + int(h), x] = (derivative_clamp*(35/255), derivative_clamp*(137/255), derivative_clamp*(218/255))


while running:
	window.fill((15, 45, 95));

	displacement += 0.3
	vertical_banner(displacement)

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()