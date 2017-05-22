#include <iostream>
#include <string>
using namespace std;

struct price{
	char ArrayTovar[8];
	char ArrayMag[8];
	char ArrayStoim[8];
};

void main(){
	//1)ввод данных в массив состоящий из 8 элементов
	//2)вывод массива в виде таблицы
	//3)вывод информации в соответствии с запросом
	//4)если запрос невыполним то вывод сообщения
	price **Tovar = new price*[8];
	price **Mag = new price*[8];
	price **Stoim = new price*[8];
	for(int i = 0; i < 8; i++){
		Tovar[i] = new price;
		cout<<"Input Tovar["<<i<<"]:";
		cin>>Tovar[i]->ArrayTovar;
		Mag[i] = new price;
		cout<<"Input Mag["<<i<<"]:";
		cin>>Mag[i]->ArrayMag;
		Stoim[i] = new price;
		cout<<"Input Stoim["<<i<<"]:";
		cin>>Stoim[i]->ArrayStoim;
	}
	cout<<"Name Tovar | Name Mag | Stoim"<<endl;
	for(int i = 0;i < 8; i++){
		cout<<Tovar[i]->ArrayTovar<<"|"<<Mag[i]->ArrayMag<<"|"<<Stoim[i]->ArrayStoim<<endl;
	}
}