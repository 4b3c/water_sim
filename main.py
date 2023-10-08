import pygame, math, numpy

pygame.init()

window = pygame.display.set_mode((1000, 600))
running = True
displacement = 0

def two_dim_graph_wave(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(999):
		h = int(math.e**math.sin((x + position) / 100) * 30)
		h -= int(math.e**math.sin((x - (position * 2 / 7)) / 30) * 10)
		pixel_array[x][400 - h] = (0, 0, 0)
	pixel_array.close()

def two_dim_flat_graph_wave(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(999):
		h = int(math.e**math.sin((x + position) / 100) * 30)
		h -= int(math.e**math.sin((x - (position * 2 / 7)) / 30) * 10)
		pixel_array[x][0:600] = (h + 100, h + 100, h + 100)
	pixel_array.close()

def two_dim_graph_wave_more_waves(position):
	pixel_array = pygame.PixelArray(window)
	for x in range(999):
		h = 0
		for y in range(12):
			h -= math.e**math.sin(((x + (position * -(y % 2) * (30/(y+1)))) * y) / 300) * 30 / (y + 0.1)

		pixel_array[x][800 + int(h)] = (0, 0, 0)
		pixel_array[x][0:800 + int(h)] = (85, 125, 195)
	pixel_array.close()




while running:
	window.fill((15, 45, 95));

	displacement += 0.3
	two_dim_graph_wave_more_waves(displacement)

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()