import serial, sys, os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QComboBox, QDialog, QGroupBox, QGridLayout, QLineEdit, QPushButton, QVBoxLayout

###------------------------------------------------------------------------- 
# initialize a serial connection with the BeagleBone
#
def init_serial() :
    global device
    
    print('Initializing serial connection...')

    # TODO try identification by device ID, instead of hardcoding a port
    # FIXME Change this line to the correct device
    #device = serial.Serial('/dev/ttyACM0')
    # Test using the command 'socat -d -d pty,rawer pty,rawer'
    device = serial.Serial('/dev/pts/3')

	
    print(device.name)
    print('Serial device is open? ' + str(device.is_open))

###-------------------------------------------------------------------------

###--------------------------------------------------------------------------
class windowGallery(QDialog) :
###--------------------------------------------------------------------------
	def __init__(self, parent=None) :
		super(windowGallery, self).__init__(parent)
		self.setMinimumSize(640, 480)

		self.createTopGroupBox()
		self.createMiddleGroupBox()
		self.createBottomGroupBox()
  
		layout = QVBoxLayout()
		layout.addWidget(self.topGroupBox)
		layout.addWidget(self.middleGroupBox)
		layout.addWidget(self.bottomGroupBox)
		self.setLayout(layout)
  
		self.setWindowTitle("Instant IoT Companion")
###--------------------------------------------------------------------------  
  
###--------------------------------------------------------------------------
# Create group for Top section (Internet connection)
#
	def createTopGroupBox(self) :
		self.topGroupBox = QGroupBox("Internet")
		
		###------------------------------------------------------------------
		# Create a single-line text field, limited to 32 max characters,
		# that only accepts alphanumeric characters.
		# Used to take in the SSID to be sent to the BeagleBone
		#
		self.ssidBox = QLineEdit()
		self.ssidBox.setPlaceholderText("SSID")
		self.ssidBox.setMaxLength(32)
		self.ssidBox.setInputMask("NNnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn")
		###------------------------------------------------------------------
  
		###------------------------------------------------------------------
		# Create a single-line text field, that only accepts alphanumeric
		# characters.
		# Used to take in the password to be sent to the BeagleBone
		#
		self.passwordBox = QLineEdit()
		self.passwordBox.setPlaceholderText("Password")
		self.passwordBox.setEchoMode(QLineEdit.Password)
		###------------------------------------------------------------------
  
		###------------------------------------------------------------------
		# Create a button labelled "Connect"
		# Used to tell the application to send the input data to the
		# BeagleBone
		#
		connectButton = QPushButton()
		connectButton.setText("Connect")
		connectButton.setAutoDefault(True)
		connectButton.clicked.connect(self.connectButtonPressed)
		###------------------------------------------------------------------
  
		layout = QVBoxLayout()
		layout.addWidget(self.ssidBox)
		layout.addWidget(self.passwordBox)
		layout.addWidget(connectButton)
		self.topGroupBox.setLayout(layout)
  
	###----------------------------------------------------------------------
	# On 'Connect' button press, echo the entered SSID and Password to the
	# terminal
	#
	def connectButtonPressed(self) :
		global device
     
		self.ssid = self.ssidBox.text()
		self.password = self.passwordBox.text()
		print("SSID: " + self.ssid + ", Password: " + self.password)
		print("Sending to device to connect...")
		device.write(bytes(self.ssid, 'utf-8') + b'\r\n')
		device.write(bytes(self.password, 'utf-8') + b'\r\n')
		
  	###----------------------------------------------------------------------
###--------------------------------------------------------------------------  
 
 
  
###--------------------------------------------------------------------------  
	def createMiddleGroupBox(self) :
		self.middleGroupBox = QGroupBox("Stream")
  
		###------------------------------------------------------------------
		# Create a drop-down menu with multiple options
		# Used to tell FFMPEG which streaming service to connect to
		#
		self.serviceBox = QComboBox()
		self.serviceBox.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.serviceBox.addItems(["Youtube", "Twitch"])
		###------------------------------------------------------------------
  
  		###------------------------------------------------------------------
		# Create a single-line text field, limited to 32 max characters,
		# that only accepts alphanumeric characters.
		# Used to take in the SSID to be sent to the BeagleBone
		#
		self.streamKeyBox = QLineEdit()
		self.streamKeyBox.setPlaceholderText("Stream Key")
		###------------------------------------------------------------------
  
		###------------------------------------------------------------------
		# Create a button labelled "Connect Stream"
		# Used to tell the aself.streamKeyBox.editingFinished.connect( self.streamKeyReady application to send the input data to the
		# BeagleBone
		#
		connectStreamButton = QPushButton()
		connectStreamButton.setText("Connect Stream")
		connectStreamButton.setAutoDefault(True)
		connectStreamButton.clicked.connect(self.connectStreamButtonPressed)
		###------------------------------------------------------------------
  
		layout = QVBoxLayout()
		layout.addWidget(self.serviceBox)
		layout.addWidget(self.streamKeyBox)
		layout.addWidget(connectStreamButton)
		self.middleGroupBox.setLayout(layout)
	###----------------------------------------------------------------------
	# On 'Connect Stream' button press, echo the entered Stream Key and
	# service to the terminal
	#
	def connectStreamButtonPressed(self) :
		global device

		self.service = self.serviceBox.currentText()
		self.key = self.streamKeyBox.text()
		print("Sending key" + self.key + " for " +  self.service)
		device.write(bytes(self.service, 'utf-8') + b'\r\n')
		device.write(bytes(self.key, 'utf-8') + b'\r\n')
    ###----------------------------------------------------------------------
###--------------------------------------------------------------------------



###--------------------------------------------------------------------------	
	def createBottomGroupBox(self) :
		self.bottomGroupBox = QGroupBox("LED Configuration")	
  
		###------------------------------------------------------------------
		# Create 6 drop-down menus with multiple options
		# Used to tell LEDs what they should be monitoring
		#
		options = ["Off", "Internet Status", "Stream Status", "Mic Connection", "Camera Connection"]
  
		self.ledConfigBox1 = QComboBox()
		self.ledConfigBox1.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.ledConfigBox1.addItems(options)
  
		self.ledConfigBox2 = QComboBox()
		self.ledConfigBox2.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.ledConfigBox2.addItems(options)
  
		self.ledConfigBox3 = QComboBox()
		self.ledConfigBox3.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.ledConfigBox3.addItems(options)
  
		self.ledConfigBox4 = QComboBox()
		self.ledConfigBox4.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.ledConfigBox4.addItems(options)
  
		self.ledConfigBox5 = QComboBox()
		self.ledConfigBox5.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.ledConfigBox5.addItems(options)
  
		self.ledConfigBox6 = QComboBox()
		self.ledConfigBox6.SizeAdjustPolicy(QComboBox.AdjustToContents)
		self.ledConfigBox6.addItems(options)
		###------------------------------------------------------------------
  
		###------------------------------------------------------------------
		# Create a button labelled "Confirm"
		# Used to tell the application to send the input data to the
		# BeagleBone
		#
		confirmButton = QPushButton()
		confirmButton.setText("Confirm")
		confirmButton.setAutoDefault(True)
		confirmButton.clicked.connect(self.confirmButtonPressed)
		###------------------------------------------------------------------
  
  
		layout = QGridLayout()
		layout.addWidget(self.ledConfigBox1, 0, 0)
		layout.addWidget(self.ledConfigBox2, 0, 1)
		layout.addWidget(self.ledConfigBox3, 0, 2)
		layout.addWidget(self.ledConfigBox4, 1, 0)
		layout.addWidget(self.ledConfigBox5, 1, 1)
		layout.addWidget(self.ledConfigBox6, 1, 2)
		layout.addWidget(confirmButton, 2, 2)
		self.bottomGroupBox.setLayout(layout)
	###----------------------------------------------------------------------
	# Converts the text entry to a number entry to allow for easier implementation of serial commands
	#
	def nameToNumber(self, numLED) : 
		match numLED:
			case 'Off':
				return '0'
			case 'Internet Status':
				return '1'			
			case 'Stream Status':
				return '2'
			case 'Mic Connection':
				return '3'
			case 'Camera Connection':
				return '4'
			case _:
				return '-1' # Failure state
    ###----------------------------------------------------------------------
 
	###----------------------------------------------------------------------
	# On 'Connect' button press, echo the entered SSID and Password to the
	# terminal
	#
	def confirmButtonPressed(self) :
		self.LED1 = self.ledConfigBox1.currentText()
		self.LED2 = self.ledConfigBox2.currentText()
		self.LED3 = self.ledConfigBox3.currentText()
		self.LED4 = self.ledConfigBox4.currentText()
		self.LED5 = self.ledConfigBox5.currentText()
		self.LED6 = self.ledConfigBox6.currentText()
  
		funcLED1 = bytes(self.nameToNumber(self.LED1), 'utf-8')
		funcLED2 = bytes(self.nameToNumber(self.LED2), 'utf-8')
		funcLED3 = bytes(self.nameToNumber(self.LED3), 'utf-8')
		funcLED4 = bytes(self.nameToNumber(self.LED4), 'utf-8')
		funcLED5 = bytes(self.nameToNumber(self.LED5), 'utf-8')
		funcLED6 = bytes(self.nameToNumber(self.LED6), 'utf-8')

		print("Sending configuration as follows: " + self.LED1 + ", " + self.LED2 + ", " + self.LED3 + ", " + self.LED4 + ", " + self.LED5 + ", " + self.LED6 + "...")
		device.write(funcLED1 + b',' + funcLED2 + b',' + funcLED3 + b',' + funcLED4 + b',' + funcLED5 + b',' + funcLED6 + b'\r\n')
    ###----------------------------------------------------------------------
      
###--------------------------------------------------------------------------



###-------------------------------------------------------------------------  
if __name__ == '__main__' :
	now = datetime.now() # used to establish a time-stamp for the log file
	device = None
	init_serial() # open a port with the BeagleBone
    
	app = QApplication(sys.argv)
	gallery = windowGallery()
	gallery.show()
	app.exec_()

	device.close()
 
###--------------------------------------------------------------------------
