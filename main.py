from tkinter import *
import time,random
from core_classes import Snake,Snake_part,Snake_food

ROOT = Tk()
ROOT.title('Snake')


class Main_window(Frame):
	"""Main class for my game"""
	def __init__(self,parent,width = 800,height = 600,**options):
		Frame.__init__(self,parent,**options)
		self.top_bar = Frame()
		self.top_bar.pack(side = TOP,fill = X)
		Button(self.top_bar,text = 'Start',command = self.start).pack(side = LEFT)
		Button(self.top_bar,text = 'Pause',command = self.pause).pack(side = LEFT)
		#Button(self.top_bar,text = 'Quit',command = self.quit).pack(side = LEFT)
		self.canv_width = width
		self.canv_height = height
		self.canv = Canvas(width = width,height = height,bg = 'white')
		self.canv.pack(side = TOP)
		ROOT.bind('<Up>',lambda event:self.onChangeCourse('up'))
		ROOT.bind('<Down>',lambda event:self.onChangeCourse('down'))
		ROOT.bind('<Left>',lambda event:self.onChangeCourse('left'))
		ROOT.bind('<Right>',lambda event:self.onChangeCourse('right'))
		ROOT.bind('<KeyPress>',self.onKeyPress)
		#Переменные поумолчанию
		self.run = False #Статус игры
		self.snake = False #Змейка отсутствует на экране
		self.food = False #Еда тоже отсутствует на экране
		self.pause_status = False

	def onChangeCourse(self,course):
		#Не менять курс, когда нету змеи или стоит пауза
		if not self.snake or self.pause_status:
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

	def onKeyPress(self,event):
		key = event.char
		#Для русской и английской раскладки
		if key == 'p' or 'з':
			self.pause()

	def start(self):
		'''Старт игры сначала'''
		#Проверка есть ли уже змейка на поле
		if self.snake:
			self.stop()
			self.snake.delete_snake()
			self.food.delete_part()
		self.snake = Snake(self.canv,self.canv_width,
						self.canv_height,size = 20,speed = 7,length = 2)
		self.create_food()
		self.canv.focus_set()
		self.run = True
		self.pause_status = False
		self.play()

	def play(self):
		"""Рекурсивная функция выполнения игры"""
		if not self.pause_status:
			self.snake.move()
			head = self.snake.body[0]
			#Проверка сьела ли змейку еду
			if (head.x,head.y) == (self.food.x,self.food.y):
				self.snake.add_part()
				self.create_food()
			#Проверка не сьела ли змейка саму себя
			game_over = False
			for part in self.snake.body[1:]:
				if (head.x,head.y) == (part.x,part.y):
					game_over = True
					break
			if game_over:
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
		"""Завершение игры"""
		print('Stopped!')
		self.run = False
		self.after_cancel(self.after_id)

	def game_over(self,game_over_color = 'red'):
		self.canv.config(bg = game_over_color)
		self.game_over_win = Toplevel()
		self.game_over_win.title('Game over')
		frm = Frame(self.game_over_win,width = 300,height = 200)
		frm.pack(side = TOP,expand = YES,fill = BOTH)
		game_over_lbl = Label(frm,text = "GAME OVER")
		game_over_lbl.config(font=('times',20,'bold'))
		game_over_lbl.pack(side = TOP,expand = YES, fill = BOTH)
		lbl_txt = 'Your length ' + str(self.snake.length)
		score_lbl = Label(self.game_over_win,text = lbl_txt)
		score_lbl.config(font=('times',13,'bold'))
		score_lbl.pack(side = TOP,expand = YES, fill = BOTH)
		ok_btn = Button(self.game_over_win,text = 'Ok', command = self.game_over_win.destroy)
		ok_btn.pack(side = TOP,fill = BOTH)
		#Сделать окно модальным
		self.game_over_win.focus_set() 
		self.game_over_win.grab_set() #Запрещает доступ к другим окнам
		self.game_over_win.wait_window() #Ожидает закрытия окна
		self.canv.config(bg = 'white')

	def create_food(self):
		'''Генерация еды в случайном месте'''
		#Удалить старую еду
		if self.food:self.food.delete_part()
		while True:
			#Генерируется случайны координаты кратные размеру
			random_x = random.choice(range(int(self.canv_width/self.snake.size)))
			random_y = random.choice(range(int(self.canv_height/self.snake.size)))
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
