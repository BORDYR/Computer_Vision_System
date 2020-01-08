import serial as serial
from tkinter import *
import ObjectRecognizer


class RobotConnection(serial.Serial):
	def __init__(self):
		super().__init__()
		self.name = "COM3"
		self.timeout = 100
		self.rtscts = 1
		self.parity = 'E'
		self.status = False

	def open_conection(self):
		self.open()

	def reset_robot(self):
		#self.write('RS')
		self.status = not self.status

	def move_to_point(self, x, y, z):
		self.write(f'DW {x},{y},{z}')

	def move_to_absolute_point(self, x, y, z=353.36, a=0, b=90):
		self.write(f'MP {x},{y},{z},{a},{b}')

	def hand_open(self):
		try:
			self.write('GO')
		except serial.SerialException as ex:
			print(ex.errno)

	def hand_close(self):
		self.write('GC')

	def move(self, p):
		self.write(f'MO {p}')


class RobotGui():
	def __init__(self, master):
		self.objects = False
		self.robot = RobotConnection()
		self.frame = master
		self.frame.title('Robot Contol Unit')
		#self.frame.geometry('300x250')
		self.frame.iconbitmap('pepe.ico')
		self.set_labels()
		self.set_buttons()
		self.e = Entry(self.frame, width=25, borderwidth=5)
		self.e.grid(row=2, column=0)

	def set_labels(self):
		Label(self.frame, text=f'''
Using robot spec:
port name: {self.robot.name}
timeout: {self.robot.timeout}
rtscts: {self.robot.rtscts}
parity: {self.robot.parity}
baudrate: {self.robot.baudrate}
stopbits: {self.robot.stopbits}''').grid(row=0, column=0)
		Label(self.frame, text=f'Status: {self.robot.status}').grid(row=0, column=1)
		Label(self.frame, text=f'Objects availability: {self.objects}').grid(row=2, column=2)

	def set_buttons(self):
		Button(self.frame, text='Close', command=self.frame.destroy, padx=50).grid(row=5, column=2)
		Button(self.frame, text='Reset robot', command=self.reset).grid(row=0, column=2)
		Button(self.frame, text='Move', command=self.move).grid(row=2, column=1)
		Button(self.frame, text='Open Hand', command=self.open_hand).grid(row=4, column=0)
		Button(self.frame, text='Close Hand', command=self.close_hand).grid(row=5, column=0)
		Button(self.frame, text='Grab object', command=self.grab_first_object).grid(row=1, column=2)


	def reset(self):
		self.robot.reset_robot()
		Label(self.frame, text=f'Status: {self.robot.status}').grid(row=0, column=1)

	def open_hand(self):
		self.robot.hand_open()

	def close_hand(self):
		self.robot.hand_close()

	def move(self):
		point = self.e.get()
		if point.isdigit():
			self.robot.move(int(point))
		else:
			print("Enter the correct point")

	def start_recognition_process(self):
		self.objects = ObjectRecognizer.get_objects_coordinates()

	def grab_first_object(self):
		if not self.objects:
			self.start_recognition_process()
		Label(self.frame, text=f'Objects availability: {self.objects}').grid(row=2, column=2)
		x, y = self.objects[0]
		self.robot.hand_open()
		self.robot.move_to_absolute_point(x=x, y=y, z=RobotPositions.upperZ)
		self.robot.move_to_absolute_point(x=x, y=y, z=RobotPositions.lowerZ)
		self.robot.hand_close()
		self.robot.move_to_absolute_point(x=x, y=y, z=RobotPositions.upperZ)



class RobotPositions():
	lowerZ = 306.98
	upperZ = 353.36


if '__main__' == __name__:
	root = Tk()
	app = RobotGui(root)
	root.mainloop()


