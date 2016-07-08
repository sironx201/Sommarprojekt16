import sys, socket
from PyQt4 import QtCore, QtGui, QtNetwork
import numpy as np
import struct

UDP_IP = '172.24.1.62' # The PC's IP address! (maybe not?)
UDP_PORT = 5005
camera_x = 200
camera_y = 200

class Window(QtGui.QMainWindow):    # Klassen "Window" ärver från Qt.Gui.QMainWindow
    
    def __init__(self): # Metod som alltid kommer köras direkt när en instans av "Window" skapas (här läggs det som alltid ska köras direkt vid uppstart)
        
        super(Window, self).__init__()  # super: ger föräldern. Dvs, kör init-metoden för klassen (QMainWindow) vi ärver ifrån
        
        self.UDP_socket = QtNetwork.QUdpSocket(self)    # Skapa UDP-socket
        self.UDP_socket.bind(QtNetwork.QHostAddress(UDP_IP), UDP_PORT)  # Bind den till PC:s IP-adress och en port
        self.UDP_socket.readyRead.connect(self.receive_data)    # Ange vad som ska hända när det finns data att läsa tillgänglig (jo, anropa "receive_data")
        
        self.setGeometry(50, 50, 1000, 1000)  # self: det egna objektet, instansen av klassen som skapats
        self.setWindowTitle("Test-namn")
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        
        self.video_frame = QtGui.QLabel("test", self)
        self.video_frame.move(400, 400)
        self.video_frame.resize(200, 200)    
        
        statusBar = self.statusBar()    # Skapa/visa status-bar:en (bar:en längst ner på fönstret)
        
        # Lägg till huvudmeny-rad
        extractAction = QtGui.QAction("&GET TO THE CHOPPAH!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave the App') # Ange vad status-bar:en ska visa 
        extractAction.triggered.connect(self.close_application) # Ange vad som ska hända när den triggas
        mainMenu = self.menuBar()   # Skapa meny-bar:en
        fileMenu = mainMenu.addMenu('&File')    # Lägg till "File"-dropdown
        fileMenu.addAction(extractAction)   # Lägg till rad i "File"-dropdown:en
        
        # Lägg till komponent i huvudmenyn (editor)
        openEditor = QtGui.QAction("&Editor", self)
        openEditor.setShortcut("Ctrl+E")
        openEditor.setStatusTip('Open Editor')
        openEditor.triggered.connect(self.editor)
        editorMenu = mainMenu.addMenu("&Editor")
        editorMenu.addAction(openEditor)
        
        # Lägg till komponent i huvudmenyn (file-picker, open file)
        openFile = QtGui.QAction("&Open file", self)
        openFile.setShortcut("Ctrl+O")
        openFile.setStatusTip('Open File')
        openFile.triggered.connect(self.open_file)
        fileMenu.addAction(openFile)
        
        # Lägg till komponent i huvudmenyn (save file)
        saveFile = QtGui.QAction("&Save file", self)
        saveFile.setShortcut("Ctrl+S")
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.save_file)
        fileMenu.addAction(saveFile)
        
        self.home() # home(): egendef. funktion, se nedan
        
    def home(self):
        
        # Lägg till knapp
        button = QtGui.QPushButton("Quit", self)    # Skapa en knapp (med texten "Quit")
        button.clicked.connect(self.close_application)  # Ange vad som ska hända när knappen klickas på (stänga ner programmet i det här fallet)
        button.resize(75, 30)   # Ge knappen storlek 100x100
        button.move(0, 75)  # Flytta knappen
        
        # Lägg till tool-bar
        extractAction2 = QtGui.QAction(QtGui.QIcon('logo.png'), 'Testelitest', self)
        extractAction2.triggered.connect(self.close_application)
        self.toolBar = self.addToolBar("Extraction")
        self.toolBar.addAction(extractAction2)
        
        # Lägg till komponent i tool-baren för font-val
        fontChoice = QtGui.QAction('Font', self)
        fontChoice.triggered.connect(self.font_choice)
        self.toolBar.addAction(fontChoice)
        
        # Lägg till komponent i tool-baren (Color picker)
        color = QtGui.QColor(0, 0 ,0)   # Väljer svart som default
        fontColor = QtGui.QAction('Font bg Color', self)
        fontColor.triggered.connect(self.color_picker)
        self.toolBar.addAction(fontColor)
        
        # Lägg till check-box
        checkBox = QtGui.QCheckBox('Enlarge Window', self)
        checkBox.move(300, 200)
        checkBox.stateChanged.connect(self.enlarge_window)  # Ange vad som ska hända på check-boxen klickas i
        
        # Lägg till progress bar
        self.progress = QtGui.QProgressBar(self)
        self.progress.setGeometry(200, 80, 250, 20)
        self.button = QtGui.QPushButton("Download", self)
        self.button.move(200, 120)
        self.button.clicked.connect(self.download)
        
        # Lägg till drop-down
        self.styleChoice = QtGui.QLabel(self.style().objectName(), self)
        comboBox = QtGui.QComboBox(self)
        comboBox.addItem("motif")
        comboBox.addItem("Windows")
        comboBox.addItem("cde")
        comboBox.addItem("Plastique")
        comboBox.addItem("Cleanlooks")
        comboBox.addItem("windowsvista")
        comboBox.move(50, 250)
        self.styleChoice.move(50, 150)
        comboBox.activated[str].connect(self.style_choice)  # Ange vad som ska hända då en entry i dropdown:en markeras, texten i entryn skickas vidare
        
        # Lägg till kalender
        cal = QtGui.QCalendarWidget(self)
        cal.move(500, 200)
        cal.resize(200, 200)
        
        self.show()

    def receive_data(self):
        print("Message ready!")
        image = QtCore.QByteArray()
        counter = 0
        #received_data = self.UDP_socket.readDatagram(4) # Läs in 4 bytes data, erhåller även information om sändaren (och typ något mer, lite oklart)
        #interesting_data_byte = received_data[0]
        #interesting_data_int = int.from_bytes(interesting_data_byte, byteorder = "big")
        #trans_size = interesting_data_int
        #print(trans_size)
        while counter < 3*camera_x*camera_y:
            #print("New loop")
            received_data = self.UDP_socket.readDatagram(1) # Läs in en byte data, erhåller även information om sändaren (och typ något mer, lite oklart)
            interesting_data_byte = received_data[0]
            if not interesting_data_byte:
                #print("Pass")
                pass
            else:   
                interesting_data_int = int.from_bytes(interesting_data_byte, byteorder = "big")
                image.append(str(interesting_data_int))
                counter += 1
        #self.styleChoice.setText(str(image[0]))
        img = QtGui.QImage(image, camera_x, camera_y, 3*camera_x, QtGui.QImage.Format_RGB888)
        pix = QtGui.QPixmap.fromImage(img)
        self.video_frame.setPixmap(pix)
        #pix_map = QtGui.QPixmap("test.jpg")
        #self.video_frame.setPixmap(pix_map) 
        #print(image)
        print("Klar!")
    
    def save_file(self):
        
        name = QtGui.QFileDialog.getSaveFileName(self, 'Save File')
        file = open(name, "w")
        text = self.textEdit.toPlainText()
        file.write(text)
        file.close()
        
    def open_file(self):
        
        name = QtGui.QFileDialog.getOpenFileName(self, 'Open File') # Öppna filer-picker-verktyget, returnera nammet på vald fil
        file = open(name, "r")
        self.editor()   # Kör igång text-editorn
        with file:
            text = file.read()
            self.textEdit.setText(text) # Läs in filens innehål och mata in det i editorn
        
    def editor(self):
        
        self.textEdit = QtGui.QTextEdit()
        self.setCentralWidget(self.textEdit)
        
    def color_picker(self):
        
        color = QtGui.QColorDialog.getColor()   # Öpnna färg-verktyget, returnera val då den stängs
        self.styleChoice.setStyleSheet("QWidget { background-color: %s}" % color.name())
        
    def font_choice(self):
        
        font, valid = QtGui.QFontDialog.getFont()   # Öppna font-verktyget, returnera val då den stängs
        if valid:
            self.styleChoice.setFont(font)
        
    def style_choice(self, entry_text):
        
        self.styleChoice.setText(entry_text)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create(entry_text))
        
    def enlarge_window(self, state):
        
        if state == QtCore.Qt.Checked:
            self.setGeometry(50, 50, 1000, 600)
        else:
            self.setGeometry(50, 50, 500, 300)
        
    def close_application(self):
        
        choice = QtGui.QMessageBox.question(self, 'Warning', "Do you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)
        if choice == QtGui.QMessageBox.Yes:
            print("Applications is closed")
            sys.exit()
        else:
            pass
            
    def download(self):
        
        self.completed = 0
        while self.completed < 100:
            self.completed += 0.0001
            self.progress.setValue(self.completed)
        
def run():      
    
    app = QtGui.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())   # 1: Kör app.excec_() (kör app, visa GUI:t osv). 2: (när app_exec_() är klar) kör sys.exit() med app.exec_():s returvärde som inargument, då stängs python-programmet ner och returvärdet skickas till operativsystemet (för att möjliggöra felsök om app avslutades oväntat)

run()