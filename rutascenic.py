
# rutascenic.py
# Vidit Joy Manglani
# Contains main to run ruta scenica unpackaged
##  and has all the Qtwidgets and Graphopper API requests

import sys
import os
import atexit

import branca
from branca.element import *

import pickle

import folium
from folium import plugins

import urllib.request
import requests

import scenicRouteModel
import FlickrRoute

import polyline
import geocoder

from jinja2 import Template

from PyQt5.QtCore import Qt, QMetaObject, QUrl, pyqtSlot, QDir
from PyQt5 import QtWebEngineWidgets, QtCore, QtWidgets, QtWebChannel, QtNetwork
from PyQt5.QtWebEngineWidgets import QWebEngineSettings
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication, QWidget, QLineEdit, QLabel, QPushButton, QGridLayout, QDockWidget, QPlainTextEdit
from PyQt5.QtGui import QPainter, QPixmap

class rutascenic(QMainWindow):

    htmlPath = QDir.current()
    htmlPath.cd("html")

    def __init__(self):

        super().__init__()
        self.setObjectName('MainWindow')
        QtCore.QMetaObject.connectSlotsByName(self)

        self.home = ""
        self.work = ""
        self.viaRoutes = [] #list of scenic routes added to journey
        self.journey = [] #list of coordinates from Origin till last via point(end of scenicroutes)
        self.end = [] # tail end of route for loadState

        self.notes = {} # Annotation Dictionary


        self.true = scenicRouteModel.ScenicRoute_DB()
        self.loadJourney
        atexit.register(self.saveJourney)
        self.initUI()


    def initUI(self):

# MENUBAR
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')

        impMenu = QMenu('Export', self)
        impAct = QAction('Export to .gpx (:TODO)', self)
        impMenu.addAction(impAct)

        newAct = QAction('clear journey', self)
        saveAct = QAction('Save Journey', self)
        loadAct = QAction('Load Journey', self)

        newAct.triggered.connect(self.clearJourney)
        saveAct.triggered.connect(self.saveJourney)
        loadAct.triggered.connect(self.loadJourney)

        fileMenu.addAction(newAct)
        fileMenu.addAction(saveAct)
        fileMenu.addAction(loadAct)
        fileMenu.addMenu(impMenu)

        self.statusBar().showMessage('The Journey is the Destination')


# QTWIDGETS
        self.og = QLineEdit(self)
        self.og.move (50, 150)
        self.og.setText("San Francisco")

        self.dt = QLineEdit(self)
        self.dt.move (50, 200)
        self.dt.setText("Los Angeles")

        self.goButton = QPushButton('Go', self)
        self.goButton.move(50, 250)
        self.goButton.clicked.connect(self.gcTags)

        self.view = QtWebEngineWidgets.QWebEngineView()
        self.view.settings().setAttribute(QWebEngineSettings.LocalStorageEnabled, True)
        self.view.setObjectName('MapWidget')


        self.channel = QtWebChannel.QWebChannel(self.view.page())
        self.view.page().setWebChannel(self.channel)
        self.channel.registerObject("jshelper", self)


        homepage = Figure()
        js = JavascriptLink(QUrl.fromLocalFile(self.htmlPath.absoluteFilePath("qwebchannel.js")).toString())
        homepage.header.add_child(Element(js.render()))

    ####  RUN THIS CODE TO MODIFY THE STARTUP FILE

    ## create a map showing all scenic routes with their description
    ## and a link to their annotations in a popup

    #     self.us = folium.Map(location=[36,-108], zoom_start=4, tiles='StamenWatercolor')
    #
    #     link = JavascriptLink(QUrl.fromLocalFile(self.htmlPath.absoluteFilePath("popup.js")).toString())
    #     for route in self.true.designatedScenicRoutes.values():

    #
    #         # GET SCENIC ROUTES W/ CENTER IN BOUNDS OF fastestRoute
    #         # ll = route['ll']
    #         # #print(float(ll[0]))
    #         # #print(float(ll[1]))
    #
    #             # explore = FlickrRoute.ImageByLatLong(ll[1], ll[0])
    #         paths = route['path']
    #         # rtcolor = int('B22222', base=16) ...Hex()
    #         # explore = FlickrRoute.ImageByLatLong(ll[1], ll[0])
    #         for path in paths:
    #             decodedPath = polyline.decode(path.strip('"'))
    #             desgScenicRoute = folium.PolyLine(decodedPath, weight=3,color='yellow').add_to(self.us)
    #
    #             f = Figure()
    #
    #             f.html.add_child(Element('<div id="startLat">'))
    #             # f.html.add_child(Element(str(decodedPath[0][0])))
    #             f.html.add_child(Element('</div>'))
    #             f.html.add_child(Element('<div id="startLong">'))
    #             # f.html.add_child(Element(str(decodedPath[0][1])))
    #             f.html.add_child(Element('</div>'))
    #             f.html.add_child(Element('<div id="endLat">'))
    #             # f.html.add_child(Element(str(decodedPath[len(decodedPath)-1][0])))
    #             f.html.add_child(Element('</div>'))
    #             f.html.add_child(Element('<div id="endLong">'))
    #             # f.html.add_child(Element(str(decodedPath[len(decodedPath)-1][1])))
    #             f.html.add_child(Element('</div>'))
    #             f.html.add_child(Element('<code id="encodedPath">'))
    #             f.html.add_child(Element('</code>'))
    #             f.html.add_child(Element('<div id="name">'))
    #             f.html.add_child(Element(route['name']))
    #             f.html.add_child(Element('</div>'))
    #             # f.html.add_child(Element('<iframe id = "stv" width="285" height="220" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/streetview?key=AIzaSyDiHmblGevCJUXCkuSmeOR2l9wNErlRTw4&location='))#46.414382,10.013988"></iframe>'))
    #             # f.html.add_child(Element(str(ll[1]).strip()))
    #             # f.html.add_child(Element(','))
    #             # f.html.add_child(Element(str(ll[0]).strip()))
    #             # f.html.add_child(Element('&fov=100"></iframe>'))
    #             f.html.add_child(Element('<button id="MyBtn" hidden="1">Journal Entry</button>'))
    #             f.html.add_child(Element(link.render()))
    #
    #             iframe = branca.element.IFrame(html=f.render(), width=150, height=50)
    #             popup = folium.Popup(iframe, max_width=300)
    #
    #             desgScenicRoute.add_child(popup)
    #
    #
    #     self.us.add_to(homepage)
    #     homepage.save(self.htmlPath.absoluteFilePath("full.html"))



        self.view.load(QtCore.QUrl().fromLocalFile(
            os.path.split(os.path.abspath(__file__))[0]+'/html/full.html'
        ))



        self.labelbox = QWidget()
        self.labelbox.setObjectName('Checkpoints')

        self.startpoint = QLabel(self.labelbox)
        self.endpoint = QLabel(self.labelbox)
        self.checkpoint_01 = QLabel(self.labelbox)
        self.checkpoint_01.setText('Take the scenic route')


        self.notepad = QLineEdit(self)
        self.notepad.setText('Welcome to ruta senika')
        self.notepad.editingFinished.connect(self.mischiefManaged)


        # // LAYOUT

        self.window  = QWidget()
        self.window.setObjectName('MainWidget')
        QtCore.QMetaObject.connectSlotsByName(self.window)

        self.layout = QGridLayout()
        self.window.setLayout(self.layout)

        self.layout.addWidget(self.startpoint)
        self.layout.addWidget(self.checkpoint_01)
        self.layout.addWidget(self.notepad)
        self.layout.addWidget(self.endpoint)

        self.layout.addWidget(self.view)

        self.layout.addWidget(self.og)
        self.layout.addWidget(self.dt)
        self.layout.addWidget(self.goButton)


    # Set QWidget as the central layout of the main window
        self.setCentralWidget(self.window);

        self.setGeometry(0,0,640,750)
        self.setWindowTitle('Submenu')

        self.show()


# GEOCODER
    def gcTags(self):
        try:
            g = geocoder.google(self.og.text())
            dg = geocoder.google(self.dt.text())

            self.startpoint.setText(self.og.text())
            self.startpoint.adjustSize()
            self.endpoint.setText(self.dt.text())
            self.endpoint.adjustSize()

            self.home = g
            self.work = dg

            self.searchQuickestRoute(str(self.home.latlng[0]),str(self.home.latlng[1]),
             str(dg.latlng[0]),str(dg.latlng[1]))

        except: # PRINTS DEFAULT SCREEN WHEN LINEEDIT BUGS
            self.view.load(QtCore.QUrl().fromLocalFile(
                os.path.split(os.path.abspath(__file__))[0]+'/html/full.html'
            ))

    def addPathToRoute(self, startLat, startLong, endLat, endLong):

        request = "https://graphhopper.com/api/1/route?"

        # point=51.131%2C12.414&point=48.224%2C3.867

        request += "point="
        request += str(startLat)
        request += "%2C"
        request += str(startLong)
        request += "&point="
        request += str(endLat).strip()
        request += "%2C"
        request += str(endLong).strip()


        request += "&vehicle=car&elevation=false&points_encoded=false&locale=en&key=2bbc7dfa-dc4e-4150-82e9-b75cb8fa088c"

        jsonRespDict = requests.get(request).json()

        for c in jsonRespDict['paths']:

            self.coords = (c['points'])

        self.coords = self.coords['coordinates']

        swap = [tuple(reversed(x)) for x in self.coords]



        return swap



    def addScPathToRoute(self, startLat, startLong, endLat, endLong, name, encodedPath):

        if ( len(self.viaRoutes) == 0 ):

            self.addScRtetoPathFromList(self.home.latlng[0],self.home.latlng[1],
                str(self.work.latlng[0]).strip(), str(self.work.latlng[1]).strip(),
                startLat, startLong, endLat, endLong, encodedPath)
        else:

            self.addScRtetoPathFromList(self.viaRoutes[len(self.viaRoutes)-1][-1][0], self.viaRoutes[len(self.viaRoutes)-1][-1][1],
                str(self.work.latlng[0]).strip(), str(self.work.latlng[1]).strip(),
                startLat, startLong, endLat, endLong, encodedPath)



# GRAPH-HOPPER MATRIX API

    def addScRtetoPathFromList(self, startLat, startLong, endLat, endLong, scRt_startLat,scRt_startLong,
                                                    scRt_endLat,scRt_endLong, encodedPath):


       #curl "https://graphhopper.com/api/1/matrix?point=49.932707%2C11.588051&point=50.241935%2C10.747375&point=50.118817%2C11.983337&type=json&vehicle=car&debug=true&out_array=weights&out_array=times&out_array=distances&key=[YOUR_KEY]"

        request = "https://graphhopper.com/api/1/matrix?"


        request += "from_point="
        request += str(startLat)
        request += "%2C"
        request += str(startLong)

        request += "&from_point="
        request += str(endLat)
        request += "%2C"
        request += str(endLong)


        request += "&to_point="
        request += str(scRt_startLat)
        request += "%2C"
        request += str(scRt_startLong)

        request += "&to_point="
        request += str(scRt_endLat)
        request += "%2C"
        request += str(scRt_endLong)

        request += "&type=json&vehicle=car&out_array=weights&key=2bbc7dfa-dc4e-4150-82e9-b75cb8fa088c"

        jsonRespDict = requests.get(request).json()

        matrix = []
        for c in jsonRespDict['weights']:
            for weight in c:
                matrix.append(weight)


        scRt = polyline.decode(encodedPath.replace('\\\\', '\\'))

        if (matrix[0] + matrix[3]) > (matrix[1] + matrix[2]):
            scRt.reverse()


        self.viaRoutes.append(scRt)
        self.appendScenicRoute(scRt)



    def appendScenicRoute(self, scRt):

        if len(self.viaRoutes) > 1:
            before = self.addPathToRoute(self.journey[len(self.journey)-1][0], self.journey[len(self.journey)-1][1], scRt[0][0], scRt[0][1])
        else:
            before = self.addPathToRoute(str(self.home.latlng[0]), str(self.home.latlng[1]), scRt[0][0], scRt[0][1])
        after = self.addPathToRoute(scRt[len(scRt)-1][0], scRt[len(scRt)-1][1], str(self.work.latlng[0]).strip(), str(self.work.latlng[1]).strip())
        userpath = []

        for points in before:

            self.journey.append(points)

        for points in scRt:

            self.journey.append(points)


            self.end = []
        for points in after:
            userpath.append(points)
            self.end.append(points)

        self.showPathAndNearbyRoutes(self.journey + userpath)




    def searchQuickestRoute(self, olat, olong, dlat, dlong):

        # """
        # Routing API Requests
        #     from online resource
        # """

        request = "https://graphhopper.com/api/1/route?"

        # point=51.131%2C12.414&point=48.224%2C3.867
        request += "point="#%2C12.414
        request += olat
        request += "%2C"
        request += olong
        request += "&point="
        request += dlat
        request += "%2C"
        request += dlong

        request += "&vehicle=car&elevation=false&points_encoded=false&locale=en&key=2bbc7dfa-dc4e-4150-82e9-b75cb8fa088c"


        self.statusBar().showMessage('The end of meaningless travel')


        jsonRespDict = requests.get(request).json()

        for c in jsonRespDict['paths']:
            self.bbox = (c['bbox'])
            self.coords = (c['points'])

        self.coords = self.coords['coordinates']

        swap = [tuple(reversed(x)) for x in self.coords]
        self.journey.append([self.home.latlng[0],self.home.latlng[1]])
        self.showPathAndNearbyRoutes(swap)


    def showPathAndNearbyRoutes(self, coordinate_list):
    # HEADER FOR EVERY MAP
        principal = Figure()
        js = JavascriptLink(QUrl.fromLocalFile(self.htmlPath.absoluteFilePath("qwebchannel.js")).toString())
        principal.header.add_child(Element(js.render()))

        midpoint = len(coordinate_list)/2

        try:
            self.uk = folium.Map(#max_bounds=False,
            location=coordinate_list[midpoint],
            zoom_start=5,
            # min_lat=self.bbox[1],
            # max_lat=self.bbox[3],
            # min_lon=self.bbox[2],
            # max_lon=self.bbox[0],
            # max_bounds=True,
            tiles='StamenTerrain' )
        except:
            self.uk = folium.Map(#max_bounds=False,
            # location=[37,-109],
            zoom_start=5,
            min_lat=self.bbox[1],
            max_lat=self.bbox[3],
            min_lon=self.bbox[2],
            max_lon=self.bbox[0],
            # max_bounds=True,
            tiles='StamenTerrain' )

        self.uk.add_to(principal)


        fastestRoute = folium.PolyLine(coordinate_list, weight=4,color='#0095DD').add_to(self.uk)



        link = JavascriptLink(QUrl.fromLocalFile(self.htmlPath.absoluteFilePath("popup.js")).toString())
        self.statusBar().showMessage('Getting nearby scenic routes')
        for route in self.true.designatedScenicRoutes.values():



            # GET SCENIC ROUTES W/ CENTER IN BOUNDS OF fastestRoute
            ll = route['ll']

            if ( (float(ll[0]) > float(self.bbox[0])) and (float(ll[0]) < float(self.bbox[2]))
            and (float(ll[1]) > float(self.bbox[1])) and (float(ll[1]) < float(self.bbox[3])) ):

                paths = route['path']

                for path in paths:
                    decodedPath = polyline.decode(path.strip('"'))
                    scenicRoute = folium.PolyLine(decodedPath, weight=3,color='yellow').add_to(self.uk)

                    f = Figure()
                    # f.html.add_child(Element())
                    f.html.add_child(Element('<div id="startLat">'))
                    f.html.add_child(Element(str(decodedPath[0][0])))
                    f.html.add_child(Element('</div>'))
                    f.html.add_child(Element('<div id="startLong">'))
                    f.html.add_child(Element(str(decodedPath[0][1])))
                    f.html.add_child(Element('</div>'))
                    f.html.add_child(Element('<div id="endLat">'))
                    f.html.add_child(Element(str(decodedPath[len(decodedPath)-1][0])))
                    f.html.add_child(Element('</div>'))
                    f.html.add_child(Element('<div id="endLong">'))
                    f.html.add_child(Element(str(decodedPath[len(decodedPath)-1][1])))
                    f.html.add_child(Element('</div>'))
                    f.html.add_child(Element('<code id="encodedPath">'))

                    try:
                        f.html.add_child(Element(path))
                    except:
                        lat = float(ll[1])
                        lon = float(ll[0])
                        sp = []
                        sp.append(lat)
                        sp.append(lon)
                        sillypoint = str(polyline.encode(tuple(sp)))

                        f.html.add_child(Element(sillypoint))

                    f.html.add_child(Element('</code>'))
                    f.html.add_child(Element('<div id="name">'))
                    f.html.add_child(Element(route['name']))
                    f.html.add_child(Element('</div>'))
                    f.html.add_child(Element('<iframe id = "stv" width="285" height="220" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/streetview?key=AIzaSyDiHmblGevCJUXCkuSmeOR2l9wNErlRTw4&location='))#46.414382,10.013988"></iframe>'))
                    f.html.add_child(Element(str(ll[1]).strip()))
                    f.html.add_child(Element(','))
                    f.html.add_child(Element(str(ll[0]).strip()))
                    f.html.add_child(Element('&fov=100"></iframe>'))

                    f.html.add_child(Element('<button id="MyBtn">Add to Journey</button>'))

                    f.html.add_child(Element(link.render()))

                    iframe = branca.element.IFrame(html=f.render(), width=300, height=300)
                    popup = folium.Popup(iframe, max_width=300)

                    scenicRoute.add_child(popup)

        principal.save(self.htmlPath.absoluteFilePath("test.html"))
        self.view.load(QUrl().fromLocalFile(self.htmlPath.absoluteFilePath("test.html")))
        self.statusBar().showMessage('The Means are the End')

        self.update()
        self.show()

## ANNOTATION SAVE ON FOCUSOUT EVENT
    def mischiefManaged(self):

        name = self.checkpoint_01.text()
        self.notes[name] = self.notepad.text()


    @pyqtSlot(str)
    def pathClicked(self, pathname):

        self.checkpoint_01.setText(pathname.strip())
        self.checkpoint_01.adjustSize()

        note = self.notes.get(pathname.strip(),
        "Annotate this route. Add tags like #coastal, #mountains, #forests, #etc & rate the route 1*, 2*...10*" )

        self.notepad.setText(note)


    @pyqtSlot(str, str, str, str, str, str)
    def pathSelected(self, startLat, startLong, endLat, endLong, name, pathEncoded):
        self.statusBar().showMessage('Loading your route')
        startLat=startLat.replace("\n", "")
        startLong=startLong.replace("\n", "")
        endLat=endLat.replace("\n", "")
        endLong=endLong.replace("\n", "")
        startLat=startLat.strip()
        startLong=startLong.strip()
        endLat=endLat.strip()
        endLong=endLong.strip()

        name = name.strip()

        path = pathEncoded
        path = path.strip()
        path = path.strip('"')

        self.addScPathToRoute(startLat, startLong, endLat, endLong, name, path)


        self.checkpoint_01.adjustSize()


    def clearJourney(self):
        self.journey = []


    def saveJourney(self):

        with open("routetags.text", "w+") as mdFile:
            [mdFile.write('{0},{1}\n'.format(key, value)) for key, value in self.notes.items()]


        with open("journeytest.txt", "wb") as fp:
            pickle.dump(self.journey+self.end, fp)


    def loadJourney(self):

        with open("journeytest.txt", "rb") as fp:
            self.journey = pickle.load(fp)
            self.showPathAndNearbyRoutes(self.journey)

        with open("routetags.text", "r+") as mdFile:
            for line in mdFile:
                (key, value) = line.split(',')
                self.notes[key] = value


if __name__ == '__main__':
    sys.argv.append("--remote-debugging-port=8000")
    sys.argv.append("--disable-web-security")
    app = QApplication(sys.argv)
    ex = rutascenic()
    sys.exit(app.exec_())
