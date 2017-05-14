import sys
token_array_relation=[]
lines=[]

# K - Ключевое слово Зарезервированные слова, которые не вошли ни в один из нижеперечисленных типов.
# D - Разделитель Фигурные скобки, круглые скобки, точка с запятой и т.д.
# O - Операция	Присваивание, а также арифметические, логические и строковые операции.
# Q - Тип данных Один из встроенных типов данных: int, float, double, char и т.д. 
# F - Управляющая конструкция Управляющие и условные конструкции языка: if, else, switch, goto и т.д. 
# L - Циклическая конструкция Одна из циклических конструкций языка: for, while, do.

# добавить:
# Контейнер	Перечисления, структуры, объединения и т.д.	R
# Модификатор	Модификаторы доступа, модификаторы типов, константы и т.д.	M
# Идентификатор	Допустимые имена переменных, функций, классов.	I
# Строковый литерал	Один или несколько символов заключенных в двойные кавычки.	S
# Комментарий	Однострочные «//» или многострочные «/*…*/» комментарии.	C
# Численные значения	Целые и вещественные числа	N

def tokenization(string):
	token_array=[]
	index=0
	stringgg=''
	ax=0
	global lines 
	global token_array_relation

	#Проходимся по строке и разбираем её
	while index<len(string):
		if string[index]!=';' and string[index]!='{' and string[index]!='}':
			stringgg+=string[index]
		else:
			stringgg+=string[index]
			lines.append(stringgg)
			ax+=1
			# print(stringgg)
			stringgg=''

		# K - Ключевое слово Зарезервированные слова, которые не вошли ни в один из нижеперечисленных типов.
		if string[index]=='#':
			token_array.append('K')
			token_array.append('K')
			token_array_relation.append('K')
			token_array_relation.append(ax)
			token_array_relation.append('K')
			token_array_relation.append(ax)
			# ax+=1
			while string[index]!='>':
			 	index+=1
			index+=1
		
		# D - Разделитель Фигурные скобки, круглые скобки, точка с запятой и т.д.
		elif string[index]==';':
			token_array.append('D')
			token_array_relation.append('D')
			token_array_relation.append(ax)
			# ax+=1

		# D - Разделитель Фигурные скобки, круглые скобки, точка с запятой и т.д.
		elif string[index]=='{' or string[index]=='}' or string[index]=='[' or string[index]==']' or string[index]=='(' or string[index]==')':
			token_array.append('D')
			token_array_relation.append('D')
			token_array_relation.append(ax)
			# if string[index]=='{' or string[index]=='}':
				# token_array_relation.append(ax)
				# ax+=1

		# O - Операция	Присваивание, а также арифметические, логические и строковые операции.
		elif string[index]=='+' and string[index+1]=='+':
			token_array.append('O')
			token_array_relation.append('O')
			token_array_relation.append(ax)

		# O - Операция	Присваивание, а также арифметические, логические и строковые операции.
		elif string[index]=='+' or string[index]=='-' or string[index]=='=':
			token_array.append('O')
			token_array_relation.append('O')
			token_array_relation.append(ax)

		# O - Операция	Присваивание, а также арифметические, логические и строковые операции.
		elif string[index]=='*' and string[index+1]=='*':
			token_array.append('O')
			token_array_relation.append('O')
			token_array_relation.append(ax)

			while True:
				if string[index]==',':
					break
				elif string[index]==';':
					break
				elif string[index]==' ':
					break
				elif string[index]=='=':
					break
				else:
					index+=1

		# Q - Тип данных Один из встроенных типов данных: int, float, double, char и т.д. 
		elif string[index]=='v' and string[index+1]=='o' and string[index+2]=='i' and string[index+3]=='d':
			token_array.append('Q')
			token_array_relation.append('Q')
			token_array_relation.append(ax)

			# Если это тип данных, то далее возможно либо переменная либо функция
			index+=5

			# Флаг будет значить функция это или нет
			flag_func=False
			while True:
				# Здесь улучшить, ведь бывают различные преминения
				if string[index]=='=':
					break

				if string[index]=='(':
					flag_func=True
					break

				index+=1

			if flag_func:
				token_array.append('I')
				token_array_relation.append('I')
				token_array_relation.append(ax)

		# Q - Тип данных Один из встроенных типов данных: int, float, double, char и т.д. 
		elif string[index]=='i' and string[index+1]=='n' and string[index+2]=='t':
			token_array.append('Q')
			token_array_relation.append('Q')
			token_array_relation.append(ax)

		# F - Управляющая конструкция Управляющие и условные конструкции языка: if, else, switch, goto и т.д. 
		elif string[index]=='i' and string[index+1]=='f':
			token_array.append('F')
			token_array_relation.append('F')
			token_array_relation.append(ax)

		# F - Управляющая конструкция Управляющие и условные конструкции языка: if, else, switch, goto и т.д. 
		elif string[index]=='e' and string[index+1]=='l' and string[index+2]=='s' and string[index+3]=='e':
			token_array.append('F')
			token_array.append('D')
			token_array.append('I')
			token_array.append('D')
			token_array_relation.append('F')
			token_array_relation.append(ax)
			token_array_relation.append('D')
			token_array_relation.append(ax)
			token_array_relation.append('I')
			token_array_relation.append(ax)
			token_array_relation.append('D')
			token_array_relation.append(ax)
			
			while string[index]!=')':
				index+=1

			index+=1

		# L - Циклическая конструкция Одна из циклических конструкций языка: for, while, do. 
		elif string[index]=='f' and string[index+1]=='o' and string[index+2]=='r':
			token_array.append('L')
			token_array.append('D')
			token_array_relation.append('L')
			token_array_relation.append(ax)
			token_array_relation.append('D')
			token_array_relation.append(ax)
			
			if string[index+4]=='i' and string[index+5]=='n' and string[index+6]=='t':
				token_array.append('Q')
				token_array_relation.append('Q')
				token_array_relation.append(ax)
			
			token_array.append('I')
			token_array.append('O')
			token_array.append('N')
			token_array.append('D')
			token_array.append('I')
			token_array.append('O')
			token_array.append('N')
			token_array.append('D')
			token_array.append('I')
			token_array.append('O')
			token_array_relation.append('I')
			token_array_relation.append(ax)
			token_array_relation.append('O')
			token_array_relation.append(ax)
			token_array_relation.append('N')
			token_array_relation.append(ax)
			token_array_relation.append('D')
			token_array_relation.append(ax)
			token_array_relation.append('I')
			token_array_relation.append(ax)
			token_array_relation.append('O')
			token_array_relation.append(ax)
			token_array_relation.append('N')
			token_array_relation.append(ax)
			token_array_relation.append('D')
			token_array_relation.append(ax)
			token_array_relation.append('I')
			token_array_relation.append(ax)
			token_array_relation.append('O')
			token_array_relation.append(ax)

			index+=1
			while string[index]!=')':
				stringgg+=string[index]
				index+=1

			stringgg+=string[index]
			index+=1
			stringgg+=string[index]

		index+=1

	return token_array

def main(path, name_file):
	import io
	# открытие файла
	f=open(path+'/'+name_file, 'r')
	file=f.read()
	f.close()
	
	token_array=tokenization(file)
	# print(token_array)
	# print(len(token_array))
	
	# ПОПЫТКА ТОКЕНИЗАЦИИ СТАНДАРТНЫМ МЕТОДОМ
	# token_array=[]
	# import os
	# import tokenize
	# file=f.read()
	# data=os.system('Vitya.bat')
	# for line in f:
		#file=f.readline()
		# data=list(tokenize.generate_tokens(io.StringIO(line).readline))
		# print(data)
	# f.close()

	global token_array_relation
	# print(token_array)
	# print(len(token_array))
	# print(token_array_relation)
	# print(len(token_array_relation))

	global lines
	token_array.append(token_array_relation)
	token_array.append(lines)


	return token_array

# Нужно что бы не запускался например при запуске сервера
if __name__=='__main__':
	# main(path, name_file)
	main('../upload_file/Дмитрий Маликов/ТА/Условные_конструкции', 'test1.cpp')