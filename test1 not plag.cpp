#include <iostream>
#include <string>
using namespace std;

struct price{
	char ArrayTovar[8];
	char ArrayMag[8];
	char ArrayStoim[8];
};

void main(){
	//1)���� ������ � ������ ��������� �� 8 ���������
	//2)����� ������� � ���� �������
	//3)����� ���������� � ������������ � ��������
	//4)���� ������ ���������� �� ����� ���������
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
	cout<<"What do you want?"<<endl;
	string Want;
	cin>>Want;
	string test_word = "Level cost";
	if(Want==test_word){
		cout<<"Input cost:";
		int cost;
		cin>>cost;
		for(int i = 0; i < 8; i++){
			if(*Stoim[i]->ArrayStoim < cost){
				cout<<Tovar[i]->ArrayTovar;
			}
		}
	}
	else{
		cout<<"Wrong input";
	}
	for(int i = 0; i < 5; i++){
		delete []Tovar[i];
		delete []Mag[i];
		delete []Stoim[i];
	}
	delete []Tovar;
	delete []Mag;
	delete []Stoim;
}