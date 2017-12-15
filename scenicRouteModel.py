# Manipulates the db from scenic-routes

import os
from collections import defaultdict
import csv
import json
import polyline

class ScenicRoute_DB:

    def __init__(self):

        self.routeIdPath_Dict = {}

        self.designatedScenicRoutes = {} # String, Dict
        #
        # Route
            # name
        #



        self.path = 'byways-master/contents/byway/'

        for filename in os.listdir(self.path):

            # self.scenicRoute = {}
            # id, name, distance, duration, description, path[],

            with open (self.path+filename, 'r') as route:
                scenicRoute = {}
                scenicRoute['bounds'] = [-124, 24, -66, 49]
                scenicRoute['ll'] = []
                # #print (yaml.dump(yaml.load(route)))
                line = route.readline()

                route_ID = ""
                route_PATH = """"""
                route_path = []

                route_bounds =[]
                while line:

                    if ('id: ') in line:
                        route_ID= line.split(':')[1]
                        line = route.readline()
                        if ('name: ') in line:
                            # #print(line)
                            # if ('-') not in line:
                                scenicRoute['name'] = line.split(':')[1]
                                line = route.readline()
                                scenicRoute['distance'] = line.split(':')[1]
                                line = route.readline()
                                scenicRoute['duration'] = line.split(':')[1]
                                line = route.readline()
                                scenicRoute['description'] = line.split(':')[1]
                                line = route.readline()
                                # scenicRoute['contact'] = line.split(':')[1]
                                line = route.readline()
                                if ('path: ') in line:
                                    route_PATH = line.split(':')[1].strip()
                                    if ('"') in route_PATH:
                                        route_path.append(route_PATH.replace('\\\\', '\\'))
                                    else:
                                        line = route.readline()
                                        while ('-') in line:
                                            route_path.append(line.split('-')[1].strip().replace('\\\\', '\\'))
                                            line = route.readline()


                                # if ('websites: ') in line:
                                #     pass
                                    # #print (line.split(':')[1])
                                    # #print (line)
                    if ('ll: ') in line:
                        line = route.readline()
                        scenicRoute['ll'].append(line.split('-', 1)[1].strip())
                        line = route.readline()
                        scenicRoute['ll'].append(line.split('-',1)[1].strip())

                    if ('bounds: ') in line:
                        line = route.readline()
                        route_bounds.append(line.split('-', 2)[2].strip())
                        line = route.readline()
                        route_bounds.append(line.split('-',2)[1].strip())
                        line = route.readline()
                        route_bounds.append(line.split('-',2)[2].strip())
                        line = route.readline()
                        route_bounds.append(line.split('-',1)[1].strip())
                        scenicRoute['bounds'] = route_bounds

                        # line
                    line = route.readline()

                # routeIdPath_Dict[route_ID] = route_path

                # designatedScenicRoutes[route_ID] = scenicRoute
                # for keys in scenicRoute.values():
                #     ##print(keys)

                self.routeIdPath_Dict[route_ID] = route_path
                scenicRoute['path'] = route_path
                # print(route_path)
                scenicRoute['ll'].append('-118')
                scenicRoute['ll'].append('35')

                self.designatedScenicRoutes[route_ID] = scenicRoute
