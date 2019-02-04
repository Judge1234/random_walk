import warnings
warnings.filterwarnings('ignore')
import random
import math
import numpy as np
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import seaborn as sns


def gen_vectors(bound):
    coordinates = []
    for x in range(-bound, bound+1):
        for y in range(-bound, bound+1):
            for z in range(-bound, bound+1):
                coordinates.append([x, y, z])
    return np.array(coordinates)


def random_walk(*, steps, step_bound):
    walk = []
    x, y, z = (0, 0, 0)
    for _ in range(steps):
        dx, dy, dz = random.choice(gen_vectors(step_bound))
        x += dx; y += dy; z += dz
        walk.append([x, y, z])
    return np.array(walk)
    

def calc_dist(p1, p2):
    x1, y1, z1 = p1[0], p1[1], p1[2]
    x2, y2, z2 = p2[0], p2[1], p2[2]
    D = math.sqrt(((x2-x1)**2) + ((y2-y1)**2) + ((z2-z1)**2))
    return D


def brute_force_diameter(data_points):
    bank = []
    for pt in data_points:
        for cp in data_points:
            bank.append([calc_dist(pt, cp), pt, cp])
    for data in bank:
        if data[0] == max(data[0] for data in bank):
            diameter = (data[0], data[1], data[2])
            break
    return diameter


steps = 150
step_bound = 5
walk = random_walk(steps=steps, step_bound=step_bound)
coordinate_combinations = len(gen_vectors(step_bound))
total_distance = sum([calc_dist(walk[i], walk[i+1]) for i in range(len(walk)-1)])
dia_coordinates = np.vstack(brute_force_diameter(walk)[1:])
sf_distance = calc_dist(walk[0], walk[-1])
sf_coordinates = [walk[0, 0], walk[-1, 0]], [walk[0, 1], walk[-1, 1]], [walk[0, 2], walk[-1, 2]]
hull = ConvexHull(walk)

sns.set(palette='bright')
fig = plt.figure(figsize=(15, 12))

text = f' Steps: {steps} \n \
Total Distance Travelled: {round(total_distance, 4)}\n \
Distance Between Endpoints: {round(sf_distance, 4)}\n \
Max Diameter: {round(brute_force_diameter(walk)[0], 4)}\n \
Described Hull Volume: {round(hull.volume, 4)}\n \
Valid Coordinate Combinations: {coordinate_combinations}'

ax = fig.gca(projection='3d')
plt.title(text, loc='left', fontsize=9, fontname='mono', fontweight=600)
ax.plot(walk[:, 0], walk[:, 1], walk[:, 2])
ax.scatter(walk[:, 0], walk[:, 1], walk[:, 2], alpha=0.25)

convex_hull = [ax.scatter(walk[simplex, 0],
                          walk[simplex, 1],
                          walk[simplex, 2],
                          c='blue', s=15,
                          edgecolors='black',
                          alpha=1) for simplex in hull.simplices]

ax.plot(sf_coordinates[0], sf_coordinates[1], sf_coordinates[2], '--', linewidth=0.9)
ax.plot(dia_coordinates[:, 0], dia_coordinates[:, 1], dia_coordinates[:, 2], '--', linewidth=0.9)
ax.legend(['Walk', 'Endpoints', 'Max Diameter', 'Internal Vector', 'Hull Vector'])
plt.show()







