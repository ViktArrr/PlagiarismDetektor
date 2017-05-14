# from ngramm import *

# Разность множеств
def dell(A, B):
	result=[]
	for i in A:
		if i not in B:
			result.append(i)

	return result

# def mainnn(path, name_file):
def main(A, B):
	# A=mainn(path, name_file)
	# B=mainn('../upload_file/Максим Родионов/ПОКС/1111111111111/', 'test4.cpp')
	# print(A)
	# print(B)

	# Коэффициент Баруа-Маханты = 1- (|A\B| / |A|)
	# Насколько работа А состоит из работы В
	K_AinB=1-(len(dell(A, B))/ len(A))
	# Насколько работа В состоит из работы А
	K_BinA=1-(len(dell(B, A))/ len(B))
	# print(K_AinB)
	# print(K_BinA)
	
	maximum=max(K_AinB, K_BinA)
	# print('max', maximum)
	
	return maximum

# Нужно что бы не запускался например при запуске сервера
if __name__=='__main__':
	main(nramm1, nramm2)
	# mainnn('../upload_file/Максим Родионов/ПОКС/1111111111111/', 'test1.cpp')