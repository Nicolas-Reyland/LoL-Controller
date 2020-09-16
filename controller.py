# Play League with a controller
import winmm # Joystick
import win32api, win32con, win32gui # control mouse & co.
import autoit # send keyboard events
import time, random

key_dict = {
	'x' : 'q',
	'a' : 'w',
	'b' : 'e',
	'y' : 'r',

	'tl' : 'd',
	'tr' : 'f',

	'dpad_left' : '1',
	'dpad_up' : '2',
	'dpad_right' : '3',
	'dpad_down' : '4',

	'back' : 'b',
	'start': 'z'
}

key_dict_keys = list(key_dict.keys())

base_x, base_y = 738, 408


def left_mouse_click(pos):
	x, y = pos
	win32api.SetCursorPos((x,y)) # win32api.SetCursorPos((x,y)) is better to be replaced by win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, int(x/SCREEN_WIDTH*65535.0), int(y/SCREEN_HEIGHT*65535.0))
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def right_mouse_click(pos):
	x, y = pos
	win32api.SetCursorPos((x,y))
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN,x,y,0,0)
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP,x,y,0,0)


def loop():
	global base_x, base_y
	last_move_action = time.perf_counter()
	#last_key_action = dict([key, 0] for key in list(key_dict.keys()))

	while winmm.joyGetPosEx(0, winmm.p_info) == 0:

		data = winmm.get_joystick_info() # (x, y), (rx, ry), (lt, rt), pressed_buttons
		flags, hcursor, (cx, cy) = win32gui.GetCursorInfo() # cx, cy = cursor-x, cursor-y

		# somehoy rx and sy are swapped out ?
		(x, y), (ry, rx), (lt, rt), pressed_buttons = data

		if rt > 0: # ctrl+key
			autoit.send('{CTRLDOWN}')
			for button in pressed_buttons:
				if button in key_dict_keys: # thumbl and thumbr not done yet !
					#if last_key_action[button] - time.perf_counter() > .2:
					autoit.send(key_dict[button])
					#last_key_action[button] = time.perf_counter()
					#print('ctrl')
			autoit.send('{CTRLUP}')
		else: # only key
			for button in pressed_buttons:
				if button in key_dict_keys: # thumbl and thumbr not done yet !
					#if last_key_action[button] - time.perf_counter() > .1:
					autoit.send(key_dict[button])
					#last_key_action[button] = time.perf_counter()
					#print('raw')

		if 'thumbr' in pressed_buttons:
			if time.perf_counter() - last_move_action > .1:
				# time.sleep(random.random() / 20)
				right_mouse_click((cx, cy)) # autoit.send('c') # 
				last_move_action = time.perf_counter()

		if 'thumbl' in pressed_buttons:
			if time.perf_counter() - last_move_action > .1:
				# time.sleep(random.random() / 20)
				left_mouse_click((cx, cy)) # autoit.send('c') # 
				last_move_action = time.perf_counter()


		if lt > 0:
			if abs(rx) > .01 or abs(ry) > .01:
				sx = cx + int(rx * 12)
				sy = cy + int(ry * 12)
				win32api.SetCursorPos((sx, sy))

			if abs(x) > .01 or abs(y) > .01:
				base_x += int(x * 5)
				base_y += int(y * 5)
				win32api.SetCursorPos((base_x, base_y))

		else:

			if abs(x) > .01 or abs(y) > .01:
				sx = int(x * 200) + base_x
				sy = int(y * 200) + base_y
				#win32api.SetCursorPos((sx, sy))

				if abs(rx) > .01 or abs(ry) > .01:
					sx += int(rx * 40)
					sy += int(ry * 40)

				win32api.SetCursorPos((sx, sy))


		time.sleep(.01)


loop()







