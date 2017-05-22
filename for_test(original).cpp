#include<iostream>
using namespace std;

int main(){
	int a, b, *A, *B, maxValue, proizValue, x, y;
	bool Valueindex;
	cout<<"Input size array:"<<endl;
	cin>>a>>b;
	A = new int[a];
	B = new int[b];
	cout<<"Array A:"<<endl;
    	for(int i = 0; i < a; i++){
        	cin>>A[i];
    	}
	cout<<"Array B:"<<endl;
    	for(int i = 0; i < b; i++){
        	cin>>B[i];
    	}
	cout<<endl<<"Array A: ";
    	for(int i = 0; i < a; i++){
        	cout<<A[i]<<" ";
    	}
	cout<<endl<<"Array B: ";
    	for(int i = 0; i < b; i++){
		cout<<B[i]<<" ";
    	}
	maxValue = A[0];
	if(maxValue < 0){
		Valueindex = false;
	}
	if(maxValue >= 0){
		Valueindex = true;
	}
	for(int i = 0; i < a; i++){
		if(A[i]==0){
			continue;
		}
		if(Valueindex){
			if(A[i]<0){
				x = A[i];
				x -= (A[i]*2);
				if(x > maxValue){
					maxValue = A[i];
					Valueindex = false;
					continue;
				}
			}
			if(A[i]>0){
				if(A[i] > maxValue){
					maxValue = A[i];
					Valueindex = true;
					continue;
				}
			}
		}
		if(!Valueindex){
			y = maxValue;
			y -= (maxValue*2);
			if(A[i]<0){
				x = A[i];
				x -= (A[i]*2);
				if(x > y){
					maxValue = A[i];
					Valueindex = false;
					continue;
				}
			}
			if(A[i]> 0){
				if(A[i] > y){
					maxValue = A[i];
					Valueindex = true;
					continue;
				}
			}
		}
	}
	cout<<endl<<"Max in array A: "<<maxValue<<endl;
	maxValue = B[0];
	if(maxValue < 0){
		Valueindex = false;
	}
	if(maxValue >= 0){
		Valueindex = true;
	}
	for(int i = 0; i < b; i++){
		if(B[i]==0){
			continue;
		}
		if(Valueindex==true){
			if(B[i]<0){
				x = B[i];
				x -= (B[i]*2);
				if(x > maxValue){
					maxValue = B[i];
					Valueindex = false;
					continue;
				}
			}
			if(B[i]>0){
				if(B[i] > maxValue){
					maxValue = B[i];
					Valueindex = true;
					continue;
				}
			}
		}
		if(Valueindex==false){
			y = maxValue;
			y -= (maxValue*2);
			if(B[i]<0){
				x = B[i];
				x -= (B[i]*2);
				if(x > y){
					maxValue = B[i];
					Valueindex = false;
					continue;
				}
			}
			if(B[i]> 0){
				if(B[i] > y){
					maxValue = B[i];
					Valueindex = true;
					continue;
				}
			}
		}
	}
	cout<<"Max in array B: "<<maxValue<<endl;
	proizValue = A[0];
	for(int i = 1; i < a; i++){
		proizValue *= A[i];
	}
	cout<<"Proizvedenie in array A: "<<proizValue<<endl;
	proizValue = B[0];
	for(int i = 1; i < b; i++){
		proizValue *= B[i];
	}
	cout<<"Proizvedenie in array B: "<<proizValue<<endl;
	delete[]A;
	delete[]B;
	return 0;
}