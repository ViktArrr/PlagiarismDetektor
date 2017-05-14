#include<iostream>
using namespace std;

template <class A1> void func1(A1 number, A1 number1);
template <class A1> void func2(A2 number, A2 number1);
template <class A1> void func3(A3 number, A3 number1);
template <class A1> void func4(A4 number, A4 number1);

void main(){
	int a = 5, b = 4;
	func1(a, b);
	func2(a, b);
	func3(a, b);
	func4(a, b);
	for(int i = 0; i < 5; i++){
		int MidValueArr1 = 0, MidValueArr2 = 0;
		for(int j = 0; j < 4; j++){
			MidValueArr1 += Arr1[i][j];
			MidValueArr2 += Arr2[i][j];
		}
		MidValueArr1 = MidValueArr1/4;
		MidValueArr2 = MidValueArr2/4;
		for(int k = 0; k < 4; k++){
			if(Arr1[i][k] < MidValueArr1){
				cout<<"count in Array1-"<<i + 1<<": "<<Arr1[i][k]<<endl;
			}
			if(Arr2[i][k] < MidValueArr2){
				cout<<"count in Array2-"<<i + 1<<": "<<Arr2[i][k]<<endl;
			}
		}
	}
	for(int i = 0; i < 5; i++){
		delete []Arr1[i];
		delete []Arr2[i];
	}
	delete []Arr1;
	delete []Arr2;
}
template <class 1> void func1(int number, int number1){
	int **Arr1, **Arr2;
	Arr1 = new int*[5];
	for(int i = 0; i < 5; i++){
		Arr1[i] = new int[4];
		for(int j = 0; j < 4; j++){
			cin>>Arr1[i][j];
		}
	}
}
template <class A1> void func2(int number, int number1){
	int **Arr1, **Arr2;
	Arr1 = new int*[5];
	for(int i = 0; i < 5; i++){
		Arr1[i] = new int[4];
		for(int j = 0; j < 4; j++){
			cin>>Arr1[i][j];
		}
	}
}
template <class A1> void func3(int number, int number1){
	Arr2 = new int*[5];
	for(int i = 0; i < 5; i++){
		Arr2[i] = new int[4];
		for(int j = 0; j < 4; j++){
			cin>>Arr2[i][j];
		}
	}
}
template <class A1> void func4(int number, int number1){
	for(int i = 0; i < 5; i++){
		cout<<"Array1-"<<i + 1<<":";
		for(int j = 0; j < 4; j++){
			cout<<Arr1[i][j]<<" ";
		}
		cout<<endl;
	}
}