import requests
import ui
import console

def set_msg(sender):
	payload = {'text': 'set_msg', 'msg': sender.text}
	r = requests.post('http://192.168.10.110/', data=payload)
	console.alert('Message:' + sender.text)
	
view = ui.View()                                      
view.name = 'Set Message'                                    
view.background_color = 'white'
view.bounds = (0,0,450,600)

msg_field = ui.TextField(frame=(view.width * 0.1, view.height * 0.3, 350, 100), title='input message')
msg_field.action = set_msg

view.add_subview(msg_field)
view.present('sheet')
