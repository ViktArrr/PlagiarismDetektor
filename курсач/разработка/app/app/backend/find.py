# from tokenization import *

# def mainnn(path, name_file):
def main(A, B, z, lines):
	# A=main(path, name_file)
	# B=main('../upload_file/Максим Родионов/ПОКС/1111111111111/', 'test1.cpp')
	# print(A)
	# print(B)

	# поиск наибольшей общей подстроки (longest common substring) 
	N=12

	out=[]
	output=[]

	# Алгоритм
	All=[]
	maxpp=''
	count=0
	for i in range(len(A)):
		for j in range(len(B)):
			if len(A)>(i+count):
				if A[i+count]!=B[j]:
					if len(maxpp)>N:
						All.append(maxpp)
						out.append(output)
						output=[]
					count=0
					maxpp=''
				else:
					# maxpp+=A[i]
					maxpp+=B[j]
					count+=1
					output.append(z[(j*2)+1])
			else:
				if len(maxpp)>N:
					All.append(maxpp)
					out.append(output)
					output=[]
				count=0
				maxpp=''
	# print(All)
	# print(len(All))
	# print(out)
	
	maxppp=''
	index=0
	for i in range(len(All)):
		if len(All[i])>len(maxppp):
			maxppp=All[i]
			index=i
	
	# print(maxppp)
	# print(len(maxppp))
	# print(out[index])
	word=''
	# print(int(out[index][0]))
	# print(int(out[index][-1]))
	for i in range(int(out[index][0]), int(out[index][-1])):
		word+=lines[i]

	# print(word)

	x=[0,0]
	x[0]=(len(maxppp)*100)/len(B)
	x[1]=word
	# print(x, '%')

	return x

# Нужно что бы не запускался например при запуске сервера
if __name__=='__main__':
	main(token1, token2)
	# mainnn('../upload_file/Максим Родионов/ПОКС/1111111111111/', 'test1.cpp')