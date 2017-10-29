import ui
import cb
import sound
import struct

TM_SERVICE_UUID = '00FF'
TM_CHAR_UUID = 'FF01'

class MyCentralManagerDelegate (object):
	def __init__(self):
		self.peripheral = None
		self.temp = 0

	def did_discover_peripheral(self, p):
		global text_state
		print('+++ Discovered peripheral: %s (%s)' % (p.name, p.uuid))
		if p.name and 'ESP_THERMOMETER' in p.name and not self.peripheral:
			# Keep a reference to the peripheral, so it doesn't get garbage-collected:
			self.peripheral = p
			cb.connect_peripheral(self.peripheral)
			text_state.text = 'Detected'

	def did_connect_peripheral(self, p):
		print('*** Connected: %s' % p.name)
		print('Discovering services...')
		p.discover_services()

	def did_fail_to_connect_peripheral(self, p, error):
		print('Failed to connect')

	def did_disconnect_peripheral(self, p, error):
		print('Disconnected, error: %s' % (error,))
		self.peripheral = None

	def did_discover_services(self, p, error):
		for s in p.services:
			if TM_SERVICE_UUID in s.uuid:
				print('+++ Thermometer found')
				p.discover_characteristics(s)

	def did_discover_characteristics(self, s, error):
		if TM_SERVICE_UUID in s.uuid:
			for c in s.characteristics:
				if TM_CHAR_UUID in c.uuid:
					print('read temperature sensor...')
					self.peripheral.read_characteristic_value(c)

	def did_write_value(self, c, error):
		# The temperature sensor has been activated (see did_discover_characteristic)
		print('Did enable temperature sensor')

	def did_update_value(self, c, error):
		global text_temp
		if TM_CHAR_UUID == c.uuid:
			# 
			self.temp = (c.value[0] + (c.value[1]*256))/16
			print(self.temp)
			text_temp.text=(str(self.temp) + '℃')

view = ui.View()                                      
view.name = 'THERMOMETER'                                    
view.background_color = 'white'

text_state = ui.TextView()
text_state.frame = (view.width * 0.5, view.height * 0.2, view.width, view.height*0.3)
text_state.flex = 'LRTB'
text_state.font = ('<system>', 18)
text_state.text_color = 'grey'
 
text_temp = ui.TextView()
text_temp.frame = (view.width * 0.25, view.height * 0.4, view.width, view.height)
text_temp.flex = 'WHLRTB'
text_temp.font = ('<system-bold>', 50)                                                    

view.add_subview(text_state)
view.add_subview(text_temp)
view.present('sheet')

delegate = MyCentralManagerDelegate()
print('Scanning for peripherals...')
text_state.text = 'Scanning'
cb.set_central_delegate(delegate)
cb.scan_for_peripherals()

# Keep the connection alive until the 'Stop' button is pressed:
try:
	while True: pass
except KeyboardInterrupt:
	# Disconnect everything:
	cb.reset()
