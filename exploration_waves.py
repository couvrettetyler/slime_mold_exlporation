import random
import matplotlib.pyplot as plt
import math
import time
import numpy as np
import pylab as pl
from matplotlib import collections  as mc

'''
plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)
xs = []
ys = []
line1, = ax.plot(xs, ys, c = 'blue')
'''

#define initial points
#define rays (direction and not magnitude) from each point
#look for intersection of rays
#define node and new initial point (with rays)
#continue run until all rays hit the top line
#need to provide nodes and network between them
#stop when you get a certain number of nodes along the top

#need to stop looking at ray once it intersects another
#need to make sure that rays are not crossing "extinct" rays to make new nodes

#concerned about splitting veins

class ray():
	def __init__(self, x, y, direction):
		self.x = x
		self.y = y
		self.direction = direction

	def find_intersection(self, ray2):
		#self equation: y = math.tan(self.direction*math.pi/180)*(x - self.x) + self.y
		#ray2 equation: y = math.tan(ray2.direction*math.pi/180)*(x - ray2.x) + ray2.y
		#solve for x where y = y
		#math.tan(self.direction*math.pi/180)*(x - self.x) + self.y = math.tan(ray2.direction*math.pi/180)*(x - ray2.x) + ray2.y
		#math.tan(self.direction*math.pi/180)*x - math.tan(ray2.direction*math.pi/180)*x = math.tan(ray2.direction*math.pi/180)*ray2.x + ray2.y - math.tan(self.direction*math.pi/180)*self.x - self.y
		x = (math.tan(self.direction*math.pi/180)*self.x + ray2.y - math.tan(ray2.direction*math.pi/180)*ray2.x - self.y)/(math.tan(self.direction*math.pi/180) - math.tan(ray2.direction*math.pi/180))
		y = math.tan(self.direction*math.pi/180)*(x - self.x) + self.y
		return x, y

	def find_distance(self, x, y):
		return math.sqrt((self.x - x)**2 + (self.y - y)**2)

class node():
	def __init__(self, x, y, initial_length, num_rays, ray_margin = None):
		self.x = x
		self.y = y
		self.initial_length = initial_length
		self.num_rays = num_rays
		if ray_margin == None:
			self.ray_margin = 18
		else:
			self.ray_margin = ray_margin
		self.rays = []
		self.assign_rays()

	def assign_rays(self):
		for i in range(self.num_rays):
			new_direction = True
			while new_direction:
				direction = random.random()*180
				new_direction = False
				for ray_i in self.rays:
					if ray_i.direction - self.ray_margin < direction < ray_i.direction + self.ray_margin:
						new_direction = True
						break
			self.rays.append(ray(self.x, self.y, direction))


#initialize setup
height = 1
width = 1
point_margin = width*0.1
min_length = 0.1

num_nodes = 5
num_rays = 5
nodes = []

#initialize outputs
D = [[0]*num_nodes for i in range(num_nodes)]

removed_rays = []	#ray, x1, x2

#generate initial nodes
for i in range(num_nodes):
	new_x = True
	while new_x:
		x = random.random()*width
		new_x = False
		for point in nodes:
			if x > point.x - point_margin and x < point.x + point_margin:
				new_x = True
				break
	y = 0
	nodes.append(node(x, y, 0, num_rays))


timea = time.time()
timeb = time.time()
top_connections = []
#initial points have rays. Find first intersection of all rays (find the shortest of the longer of the 2 distances)
#add a node
#for count in range(100):
while (timeb-timea < 30) and len(top_connections) < 10:
	min_distance = (height + width)*10
	new_x = 0
	new_y = 0
	new_i = 0
	new_j = 0
	new_k = 0
	new_l = 0
	i_min = len(nodes)-50 if len(nodes) > 50 else 0
	for i in range(i_min, len(nodes)):
		for j in range(len(nodes[i].rays)):
			for k in range(i+1, len(nodes)):
				for l in range(len(nodes[k].rays)):
					x, y = nodes[i].rays[j].find_intersection(nodes[k].rays[l])
					if y < max([nodes[i].y, nodes[k].y]):
						continue
					blocked = False
					for segment in removed_rays:
						x_int1, y_int1 = segment[0].find_intersection(nodes[i].rays[j])
						x_int2, y_int2 = segment[0].find_intersection(nodes[k].rays[l])
						if (segment[1] <= x_int1 <= segment[2] or segment[2] <= x_int1 <= segment[1]) and y_int1 > nodes[i].y:
							blocked = True
							break
						if (segment[1] <= x_int2 <= segment[2] or segment[2] <= x_int2 <= segment[1]) and y_int2 > nodes[k].y:
							blocked = True
							break
					if blocked:
						continue
					length_i = nodes[i].rays[j].find_distance(x, y)
					length_k = nodes[k].rays[l].find_distance(x, y)
					length = max([length_i + nodes[i].initial_length, length_k + nodes[k].initial_length])
					
					if length < min_distance and length_i > min_length and length_k > min_length:
						temp = False
						min_distance = length
						new_x = x
						new_y = y
						new_i = i
						new_j = j
						new_k = k
						new_l = l
						continue
					if length < min_distance:
						temp = True
						temp_x = x
						temp_y = y
						temp_i = i
						temp_j = j
						temp_k = k
						temp_l = l

	if temp:
		new_x = temp_x
		new_y = temp_y
		new_i = temp_i
		new_j = temp_j
		new_k = temp_k
		new_l = temp_l

	if new_y > height:
		new_y = height
		nodes.append(node(new_x, new_y, min_distance, num_rays))
		top_connections.append(nodes[-1])
	else:
		nodes.append(node(new_x, new_y, min_distance, num_rays))
	for node_list in D:
		node_list.append(0)
	D.append([0]*len(nodes))
	D[new_i][len(nodes)-1] = 1
	D[new_k][len(nodes)-1] = 1
	D[len(nodes)-1][new_i] = 1
	D[len(nodes)-1][new_k] = 1
	#add something to keep track of what rays exist/block other rays

	#remove the two rays that intercepted and add them to a list to check against later
	removed_rays += [[nodes[new_i].rays[new_j], new_x, nodes[new_i].x, new_y], [nodes[new_k].rays[new_l], new_x, nodes[new_k].x, new_y]]
	nodes[new_i].rays = nodes[new_i].rays[:new_j] + nodes[new_i].rays[new_j+1:]
	nodes[new_k].rays = nodes[new_k].rays[:new_l] + nodes[new_k].rays[new_l+1:]

	timeb = time.time()

	'''
	xs = []
	ys = []
	for el in nodes:
		xs.append(el.x)
		ys.append(el.y)
	line1.set_xdata(xs)
	line1.set_ydata(ys)
	fig.canvas.draw()
	fig.canvas.flush_events()
	'''
	'''
	xs = []
	ys = []
	for el in nodes:
		xs.append(el.x)
		ys.append(el.y)
	plt.scatter(xs, ys, c='blue')
	plt.show()
	'''



print(timeb - timea)
print(len(nodes))
print(len(top_connections))


xs = []
ys = []
for el in nodes:
	xs.append(el.x)
	ys.append(el.y)
#plt.scatter(xs, ys, c='blue')
#plt.show()

lines = [[(0, 1), (1, 1)], [(2, 3), (3, 3)], [(1, 2), (1, 3)]]

lines = []
for segment in removed_rays:
	lines.append([(segment[0].x, segment[0].y),(segment[1], segment[3])])

c = np.array([(0, 0, 1, 1)]*len(lines))

lc = mc.LineCollection(lines, colors=c, linewidths=2)
fig, ax = pl.subplots()
ax.add_collection(lc)
ax.scatter(xs, ys, c='blue')
ax.autoscale()
ax.margins(0.1)
plt.show()