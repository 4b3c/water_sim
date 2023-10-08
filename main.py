import pygame, math, numpy

pygame.init()

window = pygame.display.set_mode((1000, 600))
running = True
position = 0

while running:
	window.fill((15, 45, 95));

	pixel_array = pygame.PixelArray(window)
	for x in range(999):
		h = int(math.e**math.sin((x + position) / 100) * 30)
		h2 = int(math.e**math.sin((x - (position * 2 / 7)) / 30) * 10)
		pixel_array[x][400 - h - h2] = (0, 0, 0)
	pixel_array.close()

	position += 0.3

	pygame.display.update()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()