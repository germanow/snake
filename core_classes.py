class Snake():
	"""Класс для змейки"""
	def __init__(self,canvas,canv_width,canv_height,head_x = None,head_y = None,
				length = 5,size = 10,speed = 5,course = 'right'):
		self.canv = canvas
		self.canv_width = canv_width
		self.canv_height = canv_height
		self.length = length #Количество сегментов
		self.size = size #Длина и ширина кусочка змейки в пикселях
		self.speed = speed #Коэффициент для вычисления скорости
		course = course.lower() #Направление движения змейки
		if course == 'up' or course == 'right' or course == 'down' or course == 'left':
			self.course = course 
		else:
			print('Wrong course!\nUse defaults!')
			self.course = 'right'
		self.build_body(head_x,head_y)
			
	def build_body(self,head_x,head_y):
		"""Построение тела змейки"""
	#Поумолчанию змейка отрисовывается с центра
		if not head_x and not head_y:
			head_x = self.canv_width/2
			head_y = self.canv_height/2
		x = head_x
		y = head_y
		#Тело змейки
		self.body = []
		#Расчет приращения координат
		#Для построения змейки в направлении self.course
		if self.course == 'right':
			offset_x = -self.size
			offset_y = 0
		elif self.course == 'left':
			offset_x = self.size
			offset_y = 0
		elif self.course == 'up':
			offset_x = 0
			offset_y = self.size
		elif self.course == 'down':
			offset_x = 0
			offset_y = -self.size
		for i in range(self.length):
			head = True if (i == 0) else False
			part = Snake_part(self.canv,x,y,self.size,head)
			self.body.append(part)
			x += offset_x
			y += offset_y
		
	def move(self):
		'''Движение всей змейки на шаг size в направление course'''
		#Выбор приращения координаты для головы
		if self.course == 'right':
			offset_x = self.size
			offset_y = 0
		elif self.course == 'left':
			offset_x = -self.size
			offset_y = 0
		elif self.course == 'down':
			offset_x = 0
			offset_y = self.size
		elif self.course == 'up':
			offset_x = 0
			offset_y = -self.size
		#Вычисление новых координат частей змейки
		for i in range(self.length):
			if i == 0:
				x = self.body[i].x
				y = self.body[i].y
				new_x = x + offset_x
				new_y = y + offset_y
				#Проверка выхода за поля
				if new_x >= self.canv_width:
					new_x = 0
				elif new_x < 0:
					new_x = self.canv_width - self.size
				elif new_y >= self.canv_height:
					new_y = 0
				elif new_y < 0:
					new_y = self.canv_height - self.size
				self.body[i].move(new_x,new_y)
				continue
			#Каждая часть змейки становятся на место части, 
			#которая была перед ней
			new_x = x
			new_y = y
			x = self.body[i].x
			y = self.body[i].y
			#В случае когда добавился новый сегмент
			#Оставить его на месте
			self.body[i].move(new_x,new_y)

	def change_course(self,course):
		'''Изменение направления движения змейки'''
		course = course.lower()
		previous_part = self.body[1]
		head = self.body[0]
		#Поиск направления куда нельзя повернуть
		#Чтоб не проходить сквозь себя
		if previous_part.x < head.x:
			wrong_course = 'left'
		elif previous_part.x > head.x:
			wrong_course = 'right'
		elif previous_part.y < head.y:
			wrong_course = 'up'
		elif previous_part.y > head.y:
			wrong_course = 'down'
		if course != wrong_course:
			self.course = course
		else:
			return None
	
	def add_part(self):
		'''Добавляет новый кусок змейки в последний кусок'''
		last_part = self.body[-1]
		new_part = Snake_part(self.canv,last_part.x,last_part.y,self.size)
		self.body.append(new_part)
		self.length += 1

	def delete_snake(self):
		'''Убирает с полотна змейку'''
		for part in self.body:
			part.delete_part()


class Snake_part():
	"""Кусок змейки"""
	def __init__(self,canvas,x,y,size,head = False):
		self.size = size
		self.canv = canvas
		self.head = head
		self.create_rectangle(x,y)

	def create_rectangle(self,x,y,head_color = 'orange',part_color = '#8b6508'):
		'''Отрисовка куска'''
		self.x = x
		self.y = y
		x1 = x+self.size
		y1 = y+self.size
		if self.head:
			color = head_color
		else:
			color = part_color
		self.id = self.canv.create_rectangle(x,y,x1,y1,fill = color)

	def move(self,x,y):
		'''Удаляет старый кусок и отрисовывает другой
			в новой координате'''
		self.canv.delete(self.id)
		self.create_rectangle(x,y)

	def delete_part(self):
		'''Убирает с полотна кусок змейки'''
		self.canv.delete(self.id)

		
class Snake_food():
	'''Еда для змейки'''
	def __init__(self,canvas,x,y,size,color = '#606060'):
		self.size = size
		self.canv = canvas
		self.x = x
		self.y = y
		x1 = x + size
		y1 = y + size
		self.id = self.canv.create_oval(x,y,x1,y1,fill = color)

	def delete_part(self):
		'''Убирает с полотна кусок змейки'''
		self.canv.delete(self.id)
