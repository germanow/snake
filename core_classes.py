import random

class Snake():
  '''Класс для змейки'''
  def __init__(self, canvas, canv_width, canv_height, head_x=None, head_y=None,
              length=5, size=20, speed=5, course='right', head_color='orange',
              part_color='#8b6508'):
    self.canv = canvas
    self.canv_width = canv_width
    self.canv_height = canv_height
    self.length = length #Количество сегментов
    self.size = size #Длина и ширина кусочка змейки в пикселях
    self.speed = speed #Коэффициент для вычисления скорости
    self.head_color = head_color
    self.part_color = part_color
    course = course.lower() #Направление движения змейки
    if course == 'up' or course == 'right' or \
      course == 'down' or course == 'left':
      self.course = course 
    else:
      print('Wrong course!\nUse defaults!')
      self.course = 'right'
    self.build_body(head_x, head_y)
      
  def build_body(self, head_x, head_y):
    '''Построение тела змейки'''
    #Поумолчанию змейка отрисовывается с центра
    if not head_x:
      head_x = self.canv_width/2
    if not head_y: 
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
      part = Snake_part(self.canv, x, y, self.size, head, 
                        head_color=self.head_color, part_color=self.part_color)
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
        self.body[i].move(new_x, new_y)
        continue
      #Каждая часть змейки становятся на место части, 
      #которая была перед ней
      new_x = x
      new_y = y
      x = self.body[i].x
      y = self.body[i].y
      #В случае когда добавился новый сегмент
      #Оставить его на месте
      self.body[i].move(new_x, new_y)

  def change_course(self, course):
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
    new_part = Snake_part(self.canv, last_part.x, last_part.y, self.size, 
                          head=False, head_color=self.head_color, 
                          part_color=self.part_color)
    self.body.append(new_part)
    self.length += 1

  def delete(self):
    '''Убирает с полотна змейку'''
    for part in self.body:
      part.delete()


class Snake_bot(Snake):
  '''Ai змейка'''
  def __init__(self, player_snake, *args, **kargs):
    Snake.__init__(self, *args, head_color='red', 
                  part_color='#D2691E',**kargs)
    self.player_snake = player_snake

    
  def change_course(self, food_x, food_y):
    all_courses = {'left', 'right', 'up', 'down'}
    head = self.body[0]
    courses = set()
    offset_x = abs(food_x - head.x)
    offset_y = abs(food_y - head.y)
    if food_x < head.x:
      #Расстояние до еды через края
      offset_x_throw_border = food_x + (self.canv_width - head.x)
      if offset_x < offset_x_throw_border:
        courses.add('left')
      else:
        courses.add('right')
    elif food_x > head.x:
      offset_x_throw_border = head.x + (self.canv_width - food_x)
      if offset_x < offset_x_throw_border:
        courses.add('right')
      else:
        courses.add('left')
    if food_y < head.y:
      offset_y_throw_border = food_y + (self.canv_height - head.y)
      if offset_y < offset_y_throw_border:
        courses.add('up')
      else:
        courses.add('down')
    elif food_y > head.y:
      offset_y_throw_border = head.y + (self.canv_height - food_y)
      if offset_y < offset_y_throw_border:
        courses.add('down')
      else:
        courses.add('up')
    dangerous_courses = self.dangerous_courses()
    if not courses.difference(dangerous_courses):
      correct_courses = list(all_courses.difference(dangerous_courses))
      if not correct_courses:
        return None
    else:
      correct_courses = list(courses.difference(dangerous_courses))
    print(correct_courses)############debug
    Snake.change_course(self, random.choice(correct_courses))
    
    
  def dangerous_courses(self):
    '''Вычисляем опасные направления, чтобы не сьесть себя'''
    head = self.body[0]
    courses = []
    for part in self.body[1:-1] + self.player_snake.body:
      offset_x = part.x - head.x
      offset_y = part.y - head.y
      #Запретить опасные переходы через края
      if part.y == head.y and \
        (part.x - head.x) == (self.canv_width - self.size):
        courses.append('left')
      elif part.y == head.y and \
        (head.x - part.x) == (self.canv_width - self.size):
        courses.append('right')
      elif part.x == head.x and \
        (part.y - head.y) == (self.canv_height - self.size):
        courses.append("up")
      elif part.x == head.x and \
        (head.y - part.y) == (self.canv_height - self.size):
        courses.append('down')
      if (abs(offset_x) > self.size) or (abs(offset_y) > self.size):
        continue
      if offset_x < 0 and offset_y == 0:
        courses.append('left')
      elif offset_x > 0 and offset_y == 0:
        courses.append('right')
      elif offset_y < 0 and offset_x == 0:
        courses.append('up')
      elif offset_y > 0 and offset_x == 0:
        courses.append('down')
      
    return set(courses)
        
    
    
    
class Snake_part():
  '''Кусок змейки'''
  def __init__(self, canvas, x, y, size, head, head_color, part_color):
    self.size = size
    self.canv = canvas
    self.head = head
    self.head_color = head_color
    self.part_color = part_color
    self.create_rectangle(x, y)

  def create_rectangle(self, x, y):
    '''Отрисовка куска'''
    self.x = x
    self.y = y
    x1 = x+self.size
    y1 = y+self.size
    if self.head:
      color = self.head_color
    else:
      color = self.part_color
    self.id = self.canv.create_rectangle(x, y, x1, y1, fill=color)

  def move(self,x,y):
    '''Удаляет старый кусок и отрисовывает другой
      в новой координате'''
    self.canv.delete(self.id)
    self.create_rectangle(x, y)

  def delete(self):
    '''Убирает с полотна кусок змейки'''
    self.canv.delete(self.id)

    
class Snake_food():
  '''Еда для змейки'''
  def __init__(self, canvas, x, y, size, color='#606060'):
    self.size = size
    self.canv = canvas
    self.x = x
    self.y = y
    x1 = x + size
    y1 = y + size
    self.id = self.canv.create_oval(x, y, x1, y1, fill=color)

  def delete(self):
    '''Убирает с полотна кусок змейки'''
    self.canv.delete(self.id)