#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 17:21:55 2018

@author: muratkacmaz
"""

#Murat Kaçmaz 150140052

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, \
    QPushButton, QGroupBox, QAction, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QGridLayout,QHBoxLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np 
import cv2
import random

##########################################
## Do not forget to delete "return NotImplementedError"
## while implementing a function
########################################

class App(QMainWindow):
       # Check if a point is inside a rectangle


    def __init__(self):
        super(App, self).__init__()
        self.showFullScreen()
        self.LoadedTarget=None
        self.LoadedInput =None
        self.window = QWidget(self)
        self.setCentralWidget(self.window)
        self.title = 'Detection'
        self.toolbar= self.addToolBar('Gauss Filter')
 
        
        EqAction = QAction("Gauss Filter and Corner Detection",self)
        EqAction.triggered.connect(self.gaussFilter)
        self.toolbar.addAction(EqAction)
        
        EqAction = QAction("Segmentation",self)
        EqAction.triggered.connect(self.segmentation)
        self.toolbar.addAction(EqAction)
        
       # EqAction = QAction("Morph",self)
        #EqAction.triggered.connect(self.morphButton)
        #elf.toolbar.addAction(EqAction)
        
        action = QAction ("&Open Blocks",self)
        action.triggered.connect(self.openInputImage)
        
        action2 = QAction ("&Open Brain",self)
        action2.triggered.connect(self.openTargetImage)
        
        action3 = QAction ("&EX1IT",self)
        action3.triggered.connect(self.closeApp)
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("&File")
        fileMenu.addAction(action)
        fileMenu.addAction(action2)
        fileMenu.addAction(action3)
        
        
        self.initUI()

    def openInputImage(self):
        self.inputLabel = QLabel('input')
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
       
 
        self.InputImage = cv2.imread(imagePath,0)
        
       # self.InputImage  = cv2.cvtColor(self.InputImage , cv2.COLOR_BGR2RGB)
        
       # cv2.fillConvexPoly(self.InputImage, np.asarray([[0, 0], [100, 100], [0, 100]]), (255, 10, 10), 16, 0);
        
        
 
        row,column= self.InputImage.shape  #shapeler aynı
    #    bytesPerLine = 3 * column
       
        
        self.inputPixmap = QImage(self.InputImage.data,column,row,QImage.Format_Grayscale8)
        self.inputLabel.setPixmap(QPixmap.fromImage(self.inputPixmap))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(self.inputLabel)
 
        self.canvasInput.draw()
        


    
    def openTargetImage(self):
        self.targetLabel= QLabel('target')
        filename = QFileDialog.getOpenFileName()
        imagePath1 = filename[0]
       
 
        self.targetImage = cv2.imread(imagePath1,cv2.IMREAD_ANYCOLOR)
        
        self.targetImage =cv2.cvtColor(self.targetImage,cv2.COLOR_BGR2RGB)
      
        row,column,channel= self.targetImage.shape  #shapeler
        
        bytesPerLine = 3 * column
        self.targetPixmap = QImage(self.targetImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.targetLabel.setPixmap(QPixmap.fromImage(self.targetPixmap))
        self.targetLabel.setAlignment(Qt.AlignCenter)
        self.targetGridBox.layout().addWidget(self.targetLabel)
        self.canvasTarget.draw()
        
        return NotImplementedError
    
    def closeApp(self):
        exit()
        app.quit()
        return NotImplementedError
  
    
    

        
        
        
    def initUI(self):
         
        self.gLayout = QGridLayout()
        
        self.figureInput = Figure()
        self.canvasInput =FigureCanvas(self.figureInput)
        self.figureTarget = Figure()
        self.canvasTarget =FigureCanvas(self.figureTarget)
        self.figureResult = Figure()
        self.canvasResult =FigureCanvas(self.figureResult)
        
        self.inputGridBox = QGroupBox('Input')
        inputLayout = QVBoxLayout()
        self.inputGridBox.setLayout(inputLayout)
        
        self.targetGridBox = QGroupBox('Target')
        targetLayout = QVBoxLayout()
        self.targetGridBox.setLayout(targetLayout)
        
        self.resultGridBox = QGroupBox('Result')
        resultLayout = QVBoxLayout()
        self.resultGridBox.setLayout(resultLayout)
        
        self.gLayout.addWidget(self.inputGridBox, 0, 0)
        self.gLayout.addWidget(self.targetGridBox, 0, 1)
        self.gLayout.addWidget(self.resultGridBox, 0, 2)
        
        self.window.setLayout(self.gLayout)
        self.setWindowTitle(self.title)
        self.show()





    def gaussFilter(self):
        row,column= self.InputImage.shape  #shapeler aynı
         
        self.InputImage = cv2.GaussianBlur(self.InputImage,(3,3),1)
        self.inputPixmap = QImage(self.InputImage.data,column,row,QImage.Format_Grayscale8)
        self.inputLabel.setPixmap(QPixmap.fromImage(self.inputPixmap))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(self.inputLabel)
 
        self.canvasInput.draw()
        self.cornerDetection()
        
        return NotImplementedError

        
    def cornerDetection(self):
        
        row,column= self.InputImage.shape  #shapeler aynı,
        I_x = np.zeros((row,column),dtype=np.float64)
        I_y = np.zeros((row,column),dtype=np.float64)
        bytesPerLine = 3 * column
        
        self.InputImage = self.InputImage.astype(np.float64)
        for i in range(0, row-1):
            for j in range(1, column-1):
               I_x [i,j]= (self.InputImage[i+1,j] - self.InputImage[i-1,j]) / 2
        for i in range (0,row-1):
            I_x[i,0]= I_x[i,1]
            I_x[i,column-1]=I_x[i,column-2]
    
        
        for i in range(1, row-1):
            for j in range(0, column-1):
               I_y [i,j]= (self.InputImage[i,j+1] - self.InputImage[i,j-1]) / 2
               
        for i in range (0,column-1):
            I_y[0,i]= I_x[1,i]
            I_y[column-1,i]=I_x[column-2,i]
        
        I_x2 = I_x**2
        I_x_y = I_y*I_x
        I_y2 = I_y**2
        size = 3
        self.InputImage = self.InputImage.astype(np.uint8)
        corneredImage = cv2.cvtColor(self.InputImage, cv2.COLOR_GRAY2RGB)
        
        
        for y in range(size, row-size):
            for x in range(size, column-size):
                
                boxIx2 = np.sum(I_x2[y-1:y+size-1, x-1:x+size-1],dtype = np.float64)
                 
                boxIxy = np.sum(I_x_y[y-1:y+size-1, x-1:x+size-1],dtype = np.float64)
                 
                boxIy2 = np.sum(I_y2[y-1:y+size-1, x-1:x+size-1],dtype = np.float64)
                
    
                 
                det = (boxIx2 * boxIy2 ) - (boxIxy**2)
                trace = boxIx2 + boxIy2 
                finalValue = det - .04*(trace**2)
    
               
                if finalValue > 250000:
                     
                    corneredImage.itemset((y, x, 0), 0)
                    corneredImage.itemset((y, x, 1), 255)
                    corneredImage.itemset((y, x, 2), 0)
                    
        self.inputPixmap = QImage(corneredImage.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.inputLabel.setPixmap(QPixmap.fromImage(self.inputPixmap))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(self.inputLabel)
 
        self.canvasInput.draw()

 
    def segmentation(self):
        resultLabel= QLabel('result')
        self.inputLabel = QLabel('input')
        row,column,channel= self.targetImage.shape  #shapeler
        bytesPerLine = column*3
        brainCopy =self.targetImage.copy()
        brainCopy = cv2.cvtColor(brainCopy, cv2.COLOR_RGB2GRAY)
        thresh = 85

        for i in range(row):
            for j in range(column):
                if(brainCopy[i][j] < thresh):
                    brainCopy[i][j] = 0
                else:
                    brainCopy[i][j] = 255
        
        brainCopy = cv2.cvtColor(brainCopy, cv2.COLOR_GRAY2RGB)
        self.inputPixmap = QImage(brainCopy.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.inputLabel.setPixmap(QPixmap.fromImage(self.inputPixmap))
        self.inputLabel.setAlignment(Qt.AlignCenter)
        self.inputGridBox.layout().addWidget(self.inputLabel)
        
        brainCopy = cv2.cvtColor(brainCopy, cv2.COLOR_RGB2GRAY)
        kernel = np.ones((12,12),np.uint8)
        brainCopy_erode = cv2.erode(brainCopy,kernel,iterations = 1)
        brainCopy_erode = np.array(brainCopy_erode, dtype=np.uint8)
        brainCopy_erode = cv2.cvtColor(brainCopy_erode, cv2.COLOR_GRAY2RGB)

        self.targetPixmap = QImage(brainCopy_erode.data,column,row,bytesPerLine,QImage.Format_RGB888)
        self.targetLabel.setPixmap(QPixmap.fromImage(self.targetPixmap))
        self.targetLabel.setAlignment(Qt.AlignCenter)
        self.targetGridBox.layout().addWidget(self.targetLabel)
  
        thresh_skull = 220
        skull =self.targetImage.copy()
        skull = cv2.cvtColor(skull, cv2.COLOR_RGB2GRAY)
        for i in range(row):
            for j in range(column):
                if(skull[i][j] < thresh):
                    skull[i][j] = 0
                elif(skull[i][j] > thresh and skull[i][j] < thresh_skull):
                    skull[i][j] = 127
                else:
                    skull[i][j] = 255
        
                if(skull[i][j] > brainCopy[i][j]):
                    skull[i][j] = 0

        skull = cv2.cvtColor(skull, cv2.COLOR_GRAY2RGB)
        skull = np.array(skull, dtype=np.uint8)
        self.resultPixmap = QImage(skull.data,column,row,bytesPerLine,QImage.Format_RGB888)
        resultLabel.setPixmap(QPixmap.fromImage(self.resultPixmap))
        resultLabel.setAlignment(Qt.AlignCenter)
        self.resultGridBox.layout().addWidget(resultLabel)
        self.canvasResult.draw()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    def rect_contains(rect, point) :
        if point[0] < rect[0] :
            return False
        elif point[1] < rect[1] :
            return False
        elif point[0] > rect[2] :
            return False
        elif point[1] > rect[3] :
            return False
        return True

 
   
        
    
    ex = App()
    sys.exit(app.exec_())