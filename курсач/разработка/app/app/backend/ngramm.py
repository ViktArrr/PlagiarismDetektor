# from tokenization import *

# def mainn(path, name_file):
def main(tokens):
	# tokens=main(path, name_file)
	# print(tokens)

	# Количество N-грамм K=L-N+1 где L – длина последователчьности токенов.
	N=12
	K=len(tokens)-N+1
	# print(K)

	# Создание N грамм
	ngramm=[]
	for i in range(K):
		word=''
		count=0
		while count<N:
			word+=tokens[i+count]
			count+=1
		ngramm.append(word)
	# print(ngramm)
	# print(len(ngramm))

	return ngramm

# Нужно что бы не запускался например при запуске сервера
if __name__=='__main__':
	main(tokens)
	# main(path, name_file)
	# mainn('../upload_file/Максим Родионов/ПОКС/1111111111111/', 'test1.cpp')