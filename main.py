from tkinter import *
import time
import random
import pickle
from core_classes import Snake,Snake_food


root = Tk()
root.title('Snake')


class Snake_controller():
	def __init__(self, canvas, canv_width, canv_height, 
							size=20, start_length=2, start_course='right'):
		self.canv = canvas
		self.canv_width = canv_width
		self.canv_height = canv_height
		self.size = size
		self.start_length = start_length
		self.start_course = start_course
		self.score = StringVar(value='0')
		self.run = False #Статус игры
		self.snake = False #Змейка отсутствует на экране
		self.food = False #Еда тоже отсутствует на экране
		self.pause_status = False
		self.game_over_var = BooleanVar(value=False)
	
	def start(self, speed):
		'''Старт игры сначала'''
		self.snake = Snake(self.canv, self.canv_width, self.canv_height, 
											size=self.size, speed=speed, length=self.start_length, 
											course=self.start_course)
		self.score.set(0)
		self.run = True
		self.pause_status = False
		self.game_over_var.set(False)
		self.create_food()
		self.play()
	
	def play(self):
		'''Рекурсивная функция выполнения игры'''
		if not self.pause_status:
			self.snake.move()
			head = self.snake.body[0]
			#Проверка сьела ли змейку еду
			if (head.x, head.y) == (self.food.x, self.food.y):
				self.snake.add_part()
				self.add_score()
				self.create_food()
				#В случае когда змейка занимает все поле
				if self.game_over_var.get():
					return None
			#Проверка не сьела ли змейка саму себя
			#self.game_over_var.set(False)
			for part in self.snake.body[1:]:
				#Змейка не может себя сьесть при длинне до 4 включительно
				if ((head.x, head.y) == (part.x, part.y)) and (self.snake.length > 4):
					self.game_over_var.set(True)
					return None
		if not self.food:
			self.create_food()
		after_time = int(1000/self.snake.speed)
		self.after_id = self.canv.after(after_time, self.play)

	def add_score(self):
		new_score = int(self.score.get()) + self.snake.speed
		self.score.set(str(new_score))
		
	def change_course(self, course):
		if (not self.snake) or self.pause_status or (not self.run):
			return None
		self.snake.change_course(course)
		
	def pause(self):
		'''Приостановка змейки'''
		self.pause_status = not self.pause_status

	def stop(self):
		'''Остановка игры'''
		print('Stopped!')
		self.run = False
		self.canv.after_cancel(self.after_id)
		
	def reset(self):
		if self.snake:
			self.stop()
			self.snake.delete()
			self.food.delete()	
		
	def create_food(self):
		'''Генерация еды в случайном месте'''
		#Удалить старую еду
		if self.food:self.food.delete()
		while True:
			#Ширина и высота кратные размеру
			width = int(self.canv_width/self.snake.size)
			height = int(self.canv_height/self.snake.size)
			#Если змейка занимает все доступное поле
			if self.snake.length == (width * height):
				self.game_over_var.set(True)
				return None
			#Генерируется случайны координаты в пределах окна
			random_x = random.choice(range(width))
			random_y = random.choice(range(height))
			random_x *= self.snake.size
			random_y *= self.snake.size
			#Проверка занято ли это место змейкой
			engage = False
			for part in self.snake.body:
				if (random_x, random_y) == (part.x, part.y):
					engage = True
					break
			if not engage:break
		self.food = Snake_food(self.canv, random_x, random_y, self.snake.size)
		
		
class Main_window(Frame):
	'''Main class for my game'''
	def __init__(self, parent, canv_width=800, canv_height=600, **options):
		Frame.__init__(self, parent, **options)
		self.top_bar = Frame()
		self.top_bar.pack(side=TOP, padx=1, pady=1, fill=X)
		Button(self.top_bar, text='New game',
					command=self.new_game_window).pack(side=LEFT, padx=2)
		pause_btn = Button(self.top_bar, text='Pause')
		pause_btn.pack(side=LEFT, padx=2)
		Button(self.top_bar, text='Scores',
					command=self.scores_window).pack(side=LEFT, padx=2)
		self.score_lbl = Label(self.top_bar, font=('bold'))
		self.score_lbl.pack(side=RIGHT)
		Label(self.top_bar, text='Score: ', font=('bold')).pack(side=RIGHT)
		self.canv_width = canv_width
		self.canv_height = canv_height
		self.canv = Canvas(width=canv_width, height=canv_height, bg='white')
		self.canv.pack(side=TOP)
		self.game = Snake_controller(self.canv, self.canv_width, canv_height)
		self.score_lbl.config(textvariable=self.game.score)
		pause_btn.config(command=self.game.pause)
		self.in_ready = False #Переменная выполения метода self.ready
		#Установка клавиш управления
		root.bind('<Up>',lambda event:self.game.change_course('up'))
		root.bind('<Down>',lambda event:self.game.change_course('down'))
		root.bind('<Left>',lambda event:self.game.change_course('left'))
		root.bind('<Right>',lambda event:self.game.change_course('right'))
		root.bind('<KeyPress>',self.on_key_press)
		#Вывод справочной информации по управлению
		self.control_info()
		self.load_scores() #Загрузка статистики в self.scores
		
	
	def new_game_window(self):
		'''Окно для стартовых настроек'''
		def start():
			start_win.destroy()
			self.game_run(speed.get())
		self.canv.config(bg='white')
		#Предотвращение повторного запуска
		#Во время выполнения self.ready
		if self.in_ready:return None
		#Убрать стартовую информацию в начале игры
		if self.start_control_info:
			self.canv.delete(self.start_control_info)
		self.game.reset()
		self.game.score.set(0)
		start_win = Toplevel()
		start_win.title('Start settings')
		#Ассоциированая переменная для выбора скорости
		speed = IntVar(value=10)
		frm = Frame(start_win)
		frm.pack(side=TOP, expand=YES, fill=BOTH)
		start_win_lbl = Label(frm, text="Выберите стартовые настройки")
		start_win_lbl.config(font=('times', 15, 'bold'))
		start_win_lbl.pack(side=TOP, expand=YES, fill=BOTH)
		speed_lbl = Label(frm, text='Сложность')
		speed_lbl.config(font=('times', 12))
		speed_lbl.pack(side=TOP, expand=YES, fill=BOTH)
		radio_bar = Frame(frm)
		radio_bar.pack(side=TOP, expand=YES, fill=X)
		Radiobutton(radio_bar, text='Easy',
								variable=speed, value=5).pack(side=LEFT)
		Radiobutton(radio_bar, text='Normal',
								variable=speed, value=10).pack(side=LEFT)
		Radiobutton(radio_bar, text='Hard',
								variable=speed, value=15).pack(side=LEFT)
		Radiobutton(radio_bar, text='Extreme',
								variable=speed, value=20).pack(side=LEFT)
		ok_btn = Button(frm, text='Start', command=start)
		ok_btn.pack(side=TOP, fill=X)
		self.wait_for_window(start_win)
		
	def scores_window(self):
		'''Окно статистики'''
		if not self.game.pause_status:
			self.game.pause()
		scores_win = Toplevel()
		scores_win.title('Scores')
		frm = Frame(scores_win)
		frm.pack(side=TOP, expand=YES, fill=BOTH)
		scores_win_lbl = Label(frm, text="TOP 10")
		scores_win_lbl.config(font=('times', 16, 'bold'))
		scores_win_lbl.grid(columnspan=3)
		#Сортировка по очкам
		self.scores.sort(reverse=True, key=lambda tuple:tuple[1])
		for (position, (name, score)) in enumerate(self.scores):
			position += 1
			position_lbl = Label(frm, text=str(position) + '.', font=('times', '13'))
			position_lbl.grid(row=position, column=0)
			name_lbl = Label(frm, text=name, font=('times', '13'))
			name_lbl.grid(row=position, column=1)
			score_lbl = Label(frm, text=str(score), font=('times', '13'))
			score_lbl.grid(row=position, column=2)
		self.wait_for_window(scores_win)
	
	def wait_for_window(self,win):
		'''Сделать окно модальным'''
		win.focus_set() 
		win.grab_set() #Запрещает доступ к другим окнам
		win.wait_window() #Ожидает закрытия окна
		
	def control_info(self):
		'''Вывод информации о управлении'''
		x = self.canv_width/2
		y = self.canv_height/10
		text = 'Используйте стрелки для управления змейкой\n'
		text += 'Кнопка P ставит паузу'
		self.start_control_info = self.canv.create_text(x, y, text=text,
																										fill='#778899',
																										font=('normal', '20'))
	
	def on_key_press(self, event):
		'''Обработка прочих нажатий на клавиатуру'''
		key = event.char
		#Для русской и английской раскладки
		if key == 'p' or 'з':
			self.game.pause()

	def ready(self, wait_time=2):
		'''Даёт время на подготовку'''
		tmp_snake = Snake(self.canv, self.canv_width, self.canv_height, 
								size=self.game.size, speed=1, length=self.game.start_length, 
								course=self.game.start_course)
		#Флаг выполнения функции
		self.in_ready = True
		x = self.canv_width/2
		y = self.canv_height/2
		text = self.canv.create_text(x, y, text="Ready?",
																fill='black', font=('bold', '40'))
		for i in range(1, wait_time*10):
			time.sleep(0.1)
			self.update()
		self.canv.delete(text)
		text = self.canv.create_text(x, y, text="Go!",
																fill='black', font=('bold', '45'))
		for i in range(1, 7):
			time.sleep(0.1)
			self.update()
		self.canv.delete(text)
		tmp_snake.delete()
		self.in_ready = False

	def game_run(self, speed):
		self.ready()
		self.game.start(speed)
		self.wait_variable(self.game.game_over_var)
		self.game.stop()
		self.game_over_window()

	def game_over_window(self, game_over_color='#FA8072'):
		self.canv.config(bg=game_over_color)
		game_over_win = Toplevel()
		game_over_win.title('Game over')
		frm = Frame(game_over_win)
		frm.pack(side=TOP, expand=YES, fill=BOTH)
		#Проверяем вошли мы в топ или нет
		congratulate = False
		game_score = int(self.game.score.get())
		for (name, top_score) in self.scores:
			if game_score > top_score:
				congratulate = True
				position = self.scores.index((name, top_score))
				break
		if congratulate:
			game_over_lbl = Label(frm, text="CONGRATULATE!")
			game_over_lbl.config(font=('times', 20, 'bold'))
			game_over_lbl.pack(side=TOP, padx=3, expand=YES, fill=BOTH)
			position_lbl_text = "Position in TOP - " + str(position + 1)
			position_lbl = Label(frm, text=position_lbl_text)
			position_lbl.config(font=('times', 14, 'bold'))
			position_lbl.pack(side=TOP, padx=3, expand=YES, fill=BOTH)			
		else:
			game_over_lbl = Label(frm, text="GAME OVER")
			game_over_lbl.config(font=('times', 20, 'bold'))
			game_over_lbl.pack(side=TOP, padx=3, expand=YES, fill=BOTH)
		score_lbl_txt = 'Your score: ' + str(game_score)
		score_lbl = Label(game_over_win,text = score_lbl_txt)
		score_lbl.config(font=('times', 13, 'bold'))
		score_lbl.pack(side=TOP, expand=YES, fill=BOTH)
		#Ввод имени игрока
		if congratulate:
			enter_frm = Frame(game_over_win)
			enter_frm.pack(side = TOP,expand = YES, fill = BOTH)
			Label(enter_frm,text = "Name:").pack(side = LEFT)
			entr_var = StringVar()
			entr = Entry(enter_frm, textvariable=entr_var)
			entr.pack(side=LEFT, padx=2, expand=YES, fill=X)
			entr.insert(0, 'NoName')
		ok_btn = Button(game_over_win, text='Ok', command=game_over_win.destroy)
		ok_btn.pack(side=TOP, fill=BOTH)
		self.wait_for_window(game_over_win)
		if congratulate:
			#Обновляем переменную статистики
			name = entr_var.get()
			self.scores.insert(position, (name, game_score))
			self.scores = self.scores[:-1]
			self.dump_scores()

	def load_scores(self):
		'''Загрузка статистики из файла'''
		try:
			file_scores = open('scores.pkl', 'rb')
			scores = pickle.load(file_scores)
		except FileNotFoundError:
			file_scores = open('scores.pkl', 'wb')
			#Значения поумолчанию
			scores = [('NoName', 0) for i in range(10)]
			pickle.dump(scores, file_scores)
		finally:
			file_scores.close()
		self.scores = scores
		
	def dump_scores(self):
		'''Сохранения счета в файл'''
		with open('scores.pkl', 'wb') as file_scores:
			pickle.dump(self.scores, file_scores)
		
if __name__ == '__main__':
	Main_window(root).mainloop()