import pygame
import time
import random

width = 1280
height = 720
size = (width, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.init()
fps = 60
done = False
mode = "game"
score = [0, 0]
maxscore = 5
p1w = 30; p1h = 180; p1x = 50; p1y = height/2 - p1h/2; p1v = 0
p2w = 30; p2h = 180; p2x = width-50-p2w; p2y = (height/2) - (p2h/2); p2v = 0
pspeed = 1
ballx = width/2; bally = height/2; ballSize = 15; ballxv = 0; ballyv = 0
ballDirRight = True; ballSpeed = 8; ballMaxSpeed = 10
font = pygame.font.SysFont("gillsanusltracondensed", 65)
BLACK = (0, 0, 0); WHITE = (255, 255, 255); RED = (209, 41, 41)

def drawGame():
	# border
	pygame.draw.rect(screen, WHITE, [0, 0, width, height], 10)
	# divider
	pygame.draw.line(screen, WHITE, [width/2, 0], [width/2, height], 10)
	# player 1
	p1R = pygame.draw.rect(screen, WHITE, [p1x, p1y, p1w, p1h])
	# player 2
	p2R = pygame.draw.rect(screen, WHITE, [p2x, p2y, p2w, p2h])
	# score
	text = font.render(str(score[0]), True, WHITE)
	screen.blit(text, (width/2 - (text.get_rect().width+50), 20))
	screen.blit(font.render(str(score[1]), True, WHITE), ((width/2)+50, 20))

def tickPlayers(p1y, p2y, p1v, p2v):

	# player controls
	key = pygame.key.get_pressed()
	if key[pygame.K_w]:
		p1v -= pspeed
	elif key[pygame.K_s]:
		p1v += pspeed
	
	if key[pygame.K_UP]:
		p2v -= pspeed
	elif key[pygame.K_DOWN]:
		p2v += pspeed
	
	# update velocities
	p1v = 0.9*p1v
	p2v = 0.9*p2v

	# update players' positions
	p1y += p1v
	p2y += p2v
	if p1y < 0 or p1y+p1h > height:
		p1y -= p1v
		p1v = 0
	if p2y < 0 or p2y+p2h > height:
		p2y -= p2v
		p2v = 0
	
	return p1y, p2y, p1v, p2v


def tickBall(ballx, bally, ballxv, ballyv):

	ballx += ballxv
	bally += ballyv
	player1 = [p1x, p1y, p1w, p1h]
	player2 = [p2x, p2y, p2w, p2h]

	if ball.colliderect(player1) or ball.colliderect(player2):
		if ball.colliderect(player1):
			v = p1v
			ballx -= ballxv-10
		else:
			v = p2v
			ballx -= ballxv+10
		
		ballxv *= -1
		ballyv += random.choice([1,2])

	if bally <= ballSize:
		bally = ballSize+1
		ballyv *= -1
	if bally >= height-ballSize:
		bally = height-ballSize-1
		ballyv *= -1
	
	if abs(ballxv) > ballMaxSpeed:
		ballxv *= 0.9
		pygame.draw.circle(screen, RED, (ballx, bally), ballSize)
	if abs(ballyv) > ballMaxSpeed:
		ballyv *= 0.9
		pygame.draw.circle(screen, RED, (ballx, bally), ballSize)
	
	return ballx, bally, ballxv, ballyv

def resetBall():
	return width/2, height/2, ballSpeed if ballDirRight else -ballSpeed, 0, not ballDirRight, height/2 - p1h/2, height/2 - p2h/2

def checkScore():
	if ballx-ballSize > width: return 0
	elif ballx+ballSize < 0: return 1
	return -1

ballx, bally, ballxv, ballyv, ballDirRight, p1y, p2y = resetBall()

""" GAME LOOP """
while not done:

	screen.fill(BLACK)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	
	if mode == "game":
		if checkScore() != -1:
			mode = "scored"
			score[checkScore()] += 1
			timer = 0
			ballx, bally, ballxv, ballyv, ballDirRight, p1y, p2y = resetBall()

		drawGame()
		ball = pygame.draw.circle(screen, WHITE, (ballx, bally), ballSize)
		p1y, p2y, p1v, p2v = tickPlayers(p1y, p2y, p1v, p2v)
		ballx, bally, ballxv, ballyv = tickBall(ballx, bally, ballxv, ballyv)

		pygame.display.update()
	
	if mode == "scored":
		timer += 1
		if (timer >= 1.5*fps): # 1.5 seconds
			mode = "game"
		if score[0] >= maxscore or score[1] >= maxscore:
			mode = "game over"
	
	if mode == "game over":
		winner = "player 1" if score[0] > score[1] else "player 2"
		text = font.render(f"Congrats {winner}! You won the game by {abs(score[0]-score[1])} points.", True, WHITE)
		screen.blit(text, (width/2 - text.get_rect().width/2, height/2 - text.get_rect().height/2) )
		pygame.display.update()

	clock.tick(fps)