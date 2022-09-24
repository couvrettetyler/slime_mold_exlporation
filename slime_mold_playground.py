'''
We're just gonna see how this works out. Slime Mold Playground
'''
import random

#equations from the paper
def q(i,j,d,p,l):
	return d[i][j]*(p[i]-p[j])/l[i][j]

def e1(i,j,q,p):
	return q[i][j]*(p[i]-p[j])/(p[0]-p[-1])

def e2(i,j,d,l):
	return d[i][j]*l[i][j]

def e3(i,j,q,p,d,l):
	return e1(i,j,q,p) - e2(i,j,d,l)

def h(i,j,q,p,d,l):
	return e3(i,j,q,p,d,l)/l[i][j]

def delta_d(i,j,q,p,d,l):
	return h(i,j,q,p,d,l)


def stress_function(x, start = 0, end = 1):
	length = end - start
	#stress = (1-x)/(length/2)
	stress = 1/length
	return stress

height = 1
width = 1

#initially 2 nodes that define a lenght up the middle
nodes = [[width/2, 0], [width/2, height]]
d = {0:{0: 0, 1: 1}, 1:{0: 1, 1: 0}}	#pretty much the width of the length
l = {0:{0: 0, 1: height}, 1:{0: height, 1: 0}}
p = [0,stress_function(width/2)]
q = {0:{0: 0, 1: q(0,1,d,p,l)}, 1:{0: q(1,0,d,p,l), 1: 0}}
v = [[0,1]]

#big outer loop that has some stop parameter
max_runs = 10
for k in len(max_runs):
	#generate new model(s)
	number_of_new_branches = random.randrange(1,5,1)
	for b in range(number_of_new_branches):
		#pick a new node along one of the existing branches
		split_branch_index = random.randrange(0, len(v))		#pick a branch
		split_branch = v[split_branch_index]

		if 0 in nodes[split_branch[0]]+nodes[split_branch[1]] or height in nodes[split_branch[0]]+nodes[split_branch[1]]:
			#

		#only get a new node if it's connected to the top or bottom
		new_node_y = random.randrange(nodes[split_branch[0]][1], nodes[split_branch[1]][1])	#pick a random y value along the branch for the node
		new_node_x = ((nodes[split_branch[1]][0] - nodes[split_branch[0]][0])*(new_node_y - nodes[split_branch[0]][1])/(nodes[split_branch[1]][1] - nodes[split_branch[0]][1])) + nodes[split_branch[0]][0]
		#update lists
		up_down = random.choice([0,1])	#select if the two new branches are the top or bottom half of the original
		if up_down:
			#split is between new_node and second node
			nodes.append([new_node_x, new_node_y])
			v = v[:split_branch_index] + v[split_branch_index+1:] + [split_branch[0],len(nodes)-1]
		else:
			#split is between first node and new_node

