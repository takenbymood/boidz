import pygame
import random
import numpy as np

W = 500
H = 500


def rotateVector(v,theta):
	s = np.sin(theta)
	c = np.cos(theta)
	return[c*v[0]-s*v[1],s*v[0]+c*v[1]]

def mult(v,m):
	return [m*v[0],m*v[1]]

def rotatePoints(points,theta):
	s = np.sin(theta)
	c = np.cos(theta)
	rPoints = []
	for i in points:
		rPoints.append([c*i[0]-s*i[1],s*i[0]+c*i[1]])
	return rPoints

def separation(v1,v2):
	return [v1[0]-v2[0],v1[1]-v2[1]]

def magsq(v):
	return v[0]*v[0]+v[1]*v[1]

def mag(v):
	return np.sqrt(magsq(v))

def add(v1,v2):
	return [v1[0]+v2[0],v1[1]+v2[1]]

def normalise(v):
	r = 1.0/np.sqrt(magsq(v))
	return [v[0]*r,v[1]*r]

def dotProd(v1,v2):
	return v1[0]*v2[0] + v1[1]*v2[1]

def angleDiff(v1,v2):
	a = np.arctan2(v2[1],v2[0]) - np.arctan2(v1[1],v1[0])
	return a

def updateBoids(bs):
	maxSpeed = 3
	for i in range(len(bs)):
		ix = bs[i][0]
		iy = bs[i][1]
		vA = [0,0]
		vC = [0,0]
		vS = [0,0]
		vW = [0,0]
		NNs = 0
		for j in range(len(bs)):
			jx = bs[j][0]
			jy = bs[j][1]
			if j <= i:
				continue
			s = separation(bs[i],bs[j])
			ms = magsq(s)
			if ms < 50**2:
				vA[0]+=bs[j][3]
				vA[1]+=bs[j][4]
				vC[0]+=jx
				vC[1]+=jy
				vS[0]+=jx - ix
				vS[1]+=jy - iy
				NNs += 1
				if ms<10**2:
					vS[0]+=(jx - ix)*100
					vS[1]+=(jx - ix)*100

		if NNs > 0:
			vA[0] = vA[0]/NNs
			vA[1] = vA[1]/NNs
			vC[0] = (vC[0]-ix)/NNs
			vC[1] = (vC[1]-iy)/NNs
			vC = normalise(vC)
			vS = normalise(vS)

		if W - ix < 100 and W - ix > 0.1:
			vW[0] -= 250.0/(W-ix)
		elif ix < 100 and ix > 0.1:
			vW[0] += 250.0/ix
		if H - iy < 100 and H - iy > 0.1:
			vW[1] -= 250.0/(H-iy)
		elif iy < 100 and iy > 0.1:
			vW[1] += 250.0/iy


		v = [0,0]
		v[0] = 2.0*vA[0]+2.0*vC[0]-2.0*vS[0]+3*bs[i][3]+random.uniform(0,0.01)+vW[0]
		v[1] = 2.0*vA[1]+2.0*vC[1]-2.0*vS[1]+3*bs[i][4]+random.uniform(0,0.01)+vW[1]

		v = normalise(v)

		bs[i][3] = maxSpeed*v[0]
		bs[i][4] = maxSpeed*v[1]

		bs[i][0] += bs[i][3]
		bs[i][1] += bs[i][4]

		bs[i][2] = np.arctan2(bs[i][4],bs[i][3])+np.pi*0.5

		if bs[i][0] > W + 20:
			bs[i][0] = 0
		if bs[i][0] < -20:
			bs[i][0] = W
		if bs[i][1] > H + 20:
			bs[i][1] = 0
		if bs[i][1] < -20:
			bs[i][1] = H

	return bs



(width, height) = (W, H)
screen = pygame.display.set_mode((width, height))


BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

BOID = [[6, 0], [0, 12], [12, 12]]
CVEC = [[i[0]*0.5,i[1]*0.5] for i in BOID]
for i in range(len(BOID)):
	BOID[i][0] -= CVEC[i][0]
	BOID[i][1] -= CVEC[i][1]

BSPEED = 1

BOIDS = []

for i in range(150):
	a = random.uniform(0,2*np.pi)
	v = rotateVector([0,-1],a)
	BOIDS.append([random.randint(10,W-10),random.randint(10,H-10),a,BSPEED*v[0],BSPEED*v[1]])



pygame.display.set_caption('Boids')



background_colour = (255,255,255)
screen.fill(background_colour)
pygame.display.flip()

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
  BOIDS = updateBoids(BOIDS)
  screen.fill(WHITE)
  for b in BOIDS:
  	thisBoid = []
  	thisBoid = rotatePoints(BOID,b[2])
  	for i in thisBoid:
  		i[0]+=b[0]
  		i[1]+=b[1]
  	pygame.draw.polygon(screen,BLACK,thisBoid,3)
  pygame.display.update()




