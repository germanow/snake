from tkinter import *
import time,random
from core_classes import Snake,Snake_food

ROOT = Tk()
ROOT.title('Snake')


class Main_window(Frame):
	"""Main class for my game"""
	def __init__(self,parent,canv_width = 800,canv_height = 600,**options):
		Frame.__init__(self,parent,**options)
		self.top_bar = Frame()
		self.top_bar.pack(side = TOP,fill = X)
		Button(self.top_bar,text = 'New game',
					command = self.new_game_window).pack(side = LEFT)
		Button(self.top_bar,text = 'Pause',
					command = self.pause).pack(side = LEFT)
		self.score_lbl = Label(self.top_bar,text = 'Score: 0')
		self.score_lbl.pack(side = RIGHT)
		self.canv_width = canv_width
		self.canv_height = canv_height
		self.canv = Canvas(width = canv_width,height = canv_height,bg = 'white')
		self.canv.pack(side = TOP)
		#Установка клавиш управления
		ROOT.bind('<Up>',lambda event:self.on_change_course('up'))
		ROOT.bind('<Down>',lambda event:self.on_change_course('down'))
		ROOT.bind('<Left>',lambda event:self.on_change_course('left'))
		ROOT.bind('<Right>',lambda event:self.on_change_course('right'))
		ROOT.bind('<KeyPress>',self.on_key_press)
		#Вывод справочной информации
		self.control_info()
		#Переменные поумолчанию
		self.score = 0
		self.run = False #Статус игры
		self.snake = False #Змейка отсутствует на экране
		self.food = False #Еда тоже отсутствует на экране
		self.in_ready = False #Переменная выполения метода self.ready
		self.pause_status = False
	
	def new_game_window(self):
		"""Окно для стартовых настроек"""
		def start():
			start_win.destroy()
			self.start(speed.get())
		#Предотвращение повторного запуска
		#Во время выполнения self.ready
		if self.in_ready:return None
		#Убрать стартовую информацию в начале игры
		if self.start_control_info:
			self.canv.delete(self.start_control_info)
		#Проверка есть ли уже змейка на поле
		if self.snake:
			self.stop()
			self.snake.delete_snake()
			self.food.delete_part()	
		self.change_score(set_value = 0)
		#ПОстроение интерфейса
		start_win = Toplevel()
		start_win.title('Start settings')
		#Ассоциированая переменная для выбора скорости
		speed = IntVar()
		frm = Frame(start_win,width = 300,height = 200)
		frm.pack(side = TOP,expand = YES,fill = BOTH)
		start_win_lbl = Label(frm,text = "Выберите стартовые настройки")
		start_win_lbl.config(font=('times',15,'bold'))
		start_win_lbl.pack(side = TOP,expand = YES, fill = BOTH)
		speed_lbl = Label(frm,text = 'Сложность')
		speed_lbl.config(font=('times',12))
		speed_lbl.pack(side = TOP,expand = YES, fill = BOTH)
		radio_bar = Frame(frm)
		radio_bar.pack(side = TOP,expand = YES, fill = X)
		Radiobutton(radio_bar,text = 'Easy',
								variable = speed,value = 5).pack(side = LEFT)
		Radiobutton(radio_bar,text = 'Normal',
								variable = speed,value = 10).pack(side = LEFT)
		Radiobutton(radio_bar,text = 'Hard',
								variable = speed,value = 15).pack(side = LEFT)
		Radiobutton(radio_bar,text = 'Extreme',
								variable = speed,value = 20).pack(side = LEFT)
		ok_btn = Button(frm,text = 'Start', command = start)
		ok_btn.pack(side = TOP,fill = X)
		#Сделать окно модальным
		start_win.focus_set() 
		start_win.grab_set() #Запрещает доступ к другим окнам
		start_win.wait_window() #Ожидает закрытия окна
		
	def control_info(self):
		"""Вывод информации о управлении"""
		x = self.canv_width/2
		y = self.canv_height/10
		text = 'Используйте стрелки для управления змейкой\n'
		text += 'Кнопка P ставит паузу'
		self.start_control_info = self.canv.create_text(x,y,text = text,
															fill = '#778899', font=('normal','20'))
	
	def change_score(self,set_value = None):
		'''Изменяет счет'''
		if set_value or set_value == 0:
			self.score = set_value
		else:
			self.score += self.snake.speed
		text = self.score_lbl.cget('text')
		text = text.split(' ')[0] + ' ' + str(self.score)
		print(text)
		self.score_lbl.config(text = text)

	def on_change_course(self,course):
		'''Изменение движения змейки'''
		#Не менять курс, когда нету змеи или стоит пауза
		if not self.snake or self.pause_status or not self.run:
			return None
		else:
			course = course.lower()
			if course == 'up':		
				self.snake.change_course('up')
			elif course == 'down':
				self.snake.change_course('down')
			elif course == 'left':
				self.snake.change_course('left')
			elif course == 'right':
				self.snake.change_course('right')

	def on_key_press(self,event):
		"""Обработка прочих нажатий на клавиатуру"""
		key = event.char
		#Для русской и английской раскладки
		if key == 'p' or 'з':
			self.pause()

	def start(self,speed):
		'''Старт игры сначала'''
		self.snake = Snake(self.canv,self.canv_width,
						self.canv_height,size = 20,speed = speed,length = 2,course = 'right')
		self.ready()
		self.create_food()
		self.canv.focus_set()
		self.run = True
		self.pause_status = False
		self.game_over_var = False
		self.play()

	def ready(self):
		"""Даёт время на подготовку"""
		#Переменная выполнения этой функции
		self.in_ready = True
		x = self.canv_width/2
		y = self.canv_height/2
		text = self.canv.create_text(x,y,text = "Ready?",
																fill = 'black', font=('bold','40'))
		for i in range(1,20):
			time.sleep(0.1)
			self.update()
		self.canv.delete(text)
		text = self.canv.create_text(x,y,text = "Go!",
																fill = 'black', font=('bold','45'))
		for i in range(1,8):
			time.sleep(0.1)
			self.update()
		self.canv.delete(text)
		self.in_ready = False
		
	def play(self):
		"""Рекурсивная функция выполнения игры"""
		if not self.pause_status:
			self.snake.move()
			head = self.snake.body[0]
			#Проверка сьела ли змейку еду
			if (head.x,head.y) == (self.food.x,self.food.y):
				self.snake.add_part()
				self.change_score()
				self.create_food()
				#В случае когда змейка занимает все поле
				if self.game_over_var:
					self.game_over()
					return None
			#Проверка не сьела ли змейка саму себя
			self.game_over_var = False
			for part in self.snake.body[1:]:
				#Змейка не может себя сьесть при длинне до 4 включительно
				if (head.x,head.y) == (part.x,part.y) and self.snake.length > 4:
					self.game_over_var = True
					self.game_over()
					return None
		if not self.food:
			self.create_food()
		after_time = int(1000/self.snake.speed)
		self.after_id = self.after(after_time,self.play)

	def pause(self):
		"""Приостановка змейки"""
		self.pause_status = not self.pause_status

	def stop(self):
		"""Остановка игры"""
		print('Stopped!')
		self.run = False
		self.after_cancel(self.after_id)

	def game_over(self,game_over_color = 'red'):
		self.stop()
		self.canv.config(bg = game_over_color)
		game_over_win = Toplevel()
		game_over_win.title('Game over')

		frm = Frame(game_over_win,width = 300,height = 200)
		frm.pack(side = TOP,expand = YES,fill = BOTH)

		game_over_lbl = Label(frm,text = "GAME OVER")
		game_over_lbl.config(font=('times',20,'bold'))
		game_over_lbl.pack(side = TOP,expand = YES, fill = BOTH)

		score_txt = 'Your length ' + str(self.snake.length)
		score_lbl = Label(game_over_win,text = score_txt)
		score_lbl.config(font=('times',13,'bold'))
		score_lbl.pack(side = TOP,expand = YES, fill = BOTH)

		ok_btn = Button(game_over_win,text = 'Ok', command = game_over_win.destroy)
		ok_btn.pack(side = TOP,fill = BOTH)
		#Сделать окно модальным
		game_over_win.focus_set() 
		game_over_win.grab_set() #Запрещает доступ к другим окнам
		game_over_win.wait_window() #Ожидает закрытия окна
		self.canv.config(bg = 'white')
	
	def create_food(self):
		'''Генерация еды в случайном месте'''
		#Удалить старую еду
		if self.food:self.food.delete_part()
		while True:
			#Ширина и высота кратные размеру
			width = int(self.canv_width/self.snake.size)
			height = int(self.canv_height/self.snake.size)
			#Если змейка занимает все доступное поле
			if  self.snake.length == (width*height):
				self.game_over_var = True
				return None
			#Генерируется случайны координаты в пределах окна
			random_x = random.choice(range(width))
			random_y = random.choice(range(height))
			random_x *= self.snake.size
			random_y *= self.snake.size
			#Проверка занято ли это место змейкой
			engage = False
			for part in self.snake.body:
				if (random_x,random_y) == (part.x,part.y):
					engage = True
					break
			if not engage:break
		self.food = Snake_food(self.canv,random_x,random_y,self.snake.size)


if __name__ == '__main__':
	Main_window(ROOT).mainloop()
