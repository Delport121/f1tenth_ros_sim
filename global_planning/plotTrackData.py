import trajectory_planning_helpers as tph
import numpy as np
import matplotlib.pyplot as plt
import os
import yaml
from centerline import getCentreLine
from minimumCurvature import generateMinCurvaturePath
from shortestPath import generateShortestPath
import scipy

class Track:
	'''
		Generates:
		- centreline: maps/{map_name}_centreline.csv
		- shortest path: maps/{map_name}_short.csv
		- minimum curvature path: maps/{map_name}_minCurve.csv

		Plots:
		- all paths
		- curvature vs distance
		- heading vs distance
	'''
	def __init__(self, map_name):

		# Ensure the directory exists
		output_dir = f"/home/chris/sim_ws/src/global_planning/data"
		os.makedirs(output_dir, exist_ok=True)

		# getCentreLine(map_name)
		# generateShortestPath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv")
		# generateMinCurvaturePath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_short.csv")

		if not os.path.exists(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv"):
			getCentreLine(map_name)
			generateShortestPath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv")
			generateMinCurvaturePath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv")

		if not os.path.exists(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_short.csv"):
			generateShortestPath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv")
			# generateMinCurvaturePath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv")

		if not os.path.exists(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_minCurve.csv"):
			generateMinCurvaturePath(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv")



		map_yaml_path = f"/home/chris/sim_ws/src/global_planning/maps/{map_name}.yaml"
		map_img = plt.imread(f'/home/chris/sim_ws/src/global_planning/maps/{map_name}.png')

		centreline = np.loadtxt(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_centreline.csv", delimiter=',')
		short = np.loadtxt(f"/home/chris/sim_ws/src/global_planning/maps/{map_name}_short.csv", delimiter=',')
		minCurve = np.loadtxt(f"maps/{map_name}_minCurve.csv", delimiter=',')


		# flip the image around x axis
		map_img = np.flipud(map_img)
		map_img = scipy.ndimage.distance_transform_edt(map_img)
		map_img = np.abs(map_img - 1)
		map_img[map_img!=0]=1
		
		with open(map_yaml_path, 'r') as yaml_stream:
			try:
				map_metadata = yaml.safe_load(yaml_stream)
				self.map_resolution = map_metadata['resolution']
				origin = map_metadata['origin']
			except yaml.YAMLError as ex:
				print(ex)

		self.orig_x = origin[0]
		self.orig_y = origin[1]

		startX = int((0-self.orig_x)/self.map_resolution)
		startY = int((0-self.orig_y)/self.map_resolution)
		centrelineX, centrelineY, centrelineS = self.processTrack(centreline)
		shortX, shortY, shortS = self.processTrack(short)
		minCurveX, minCurveY, minCurveS = self.processTrack(minCurve)

		fig = plt.figure( num=f'{map_name}_racelines')
		plt.title(map_name)
		plt.imshow(map_img, cmap="gray", origin="lower")
		plt.plot(startX, startY, 'ro', label='Start')
		plt.plot(centrelineX,centrelineY, '--', label=f'Centreline ({centreline[-1, -1]:.2f}s)')
		plt.plot(shortX, shortY, label=f'Shortest Path ({short[-1, -1]:.2f}s)')
		plt.plot(minCurveX, minCurveY, label=f'Minimum Curvature ({minCurve[-1, -1]:.2f}s)')
		plt.legend(loc='upper right')
		plt.savefig(f"{output_dir}/{map_name}_racelines.png")
		plt.show()

		plt.figure( num=f'{map_name}_curvature')
		plt.title(f'Curvature vs Distance {map_name}')
		plt.plot(centrelineS, centreline[:, 5], label='Centreline')
		plt.plot(shortS, short[:, 5], label='Shortest Path')
		plt.plot(minCurveS, minCurve[:, 5], label='Minimum Curvature')
		plt.legend(loc='upper right')
		plt.savefig(f"{output_dir}/{map_name}_curvature.png")
		plt.show()

		plt.figure( num=f'{map_name}_heading')
		plt.title(f'Heading vs Distance {map_name}')
		plt.plot(centrelineS, centreline[:, 4], label='Centreline')
		plt.plot(shortS, short[:, 4], label='Shortest Path')
		plt.plot(minCurveS, minCurve[:, 4], label='Minimum Curvature')
		plt.legend(loc='upper right')
		plt.savefig(f"{output_dir}/{map_name}_heading.png")
		plt.show()

		plt.figure( num=f'{map_name}_velocity')
		plt.title(f'Velocity vs Distance {map_name}')
		plt.plot(centrelineS, centreline[:, 7], label='Centreline')
		plt.plot(shortS, short[:, 7], label='Shortest Path')
		plt.plot(minCurveS, minCurve[:, 7], label='Minimum Curvature')
		plt.legend(loc='upper right')
		plt.savefig(f"{output_dir}/{map_name}_velocity.png")
		plt.show()



	def processTrack(self, track):
		x = track[:, 0]
		y = track[:, 1]
		s = track[:, 6]
		x -= self.orig_x
		y -= self.orig_y
		x /= self.map_resolution
		y /= self.map_resolution
		normS = (s-s[0])/(s[-1]-s[0])
		return x, y, normS

	

def main():
	for file in os.listdir('/home/chris/sim_ws/src/global_planning/maps/'):
		# if file.endswith('.pgm'):
		# 	map_name = file.split('.')[0]
		# 	print(f"Extracting data for: {map_name}")
		# 	track = Track(map_name)
		if file.endswith('.png'):
			map_name = file.split('.')[0]
			print(f"Extracting data for: {map_name}")
			track = Track(map_name)
if __name__ == '__main__':
	main()
			

