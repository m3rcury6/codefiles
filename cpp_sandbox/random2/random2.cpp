/*
want a good simple random number generator

*/
#include <iostream>
#include <random>
#include <vector>
using namespace std;

float mean(vector<int> &vec){
    int sum=0;
    for(int i=0;i<vec.size();i++){sum+=vec[i];}
    float m = (float)(sum) / (float)(vec.size());
    return m;
}

int max(vector<int> &vec){
    int m=0;
    for(int i=0;i<vec.size();i++){
        if(m<vec[i]){m=vec[i];}
    }
    return m;
}

int min(vector<int> &vec){
    int m=1e6;
    for(int i=0;i<vec.size();i++){
        if(m>vec[i]){m=vec[i];}
    }
    return m;
}


int main (){
    random_device rd;
    cout << "a random number: " << rd() << std::endl;

    cout << "kjg: at this point, will test and see what happens with 10k dice rolls" << endl;

    vector<int> v;
    for(int i=0;i<10000;i++){
        v.push_back(rd()%20+1);
    }

    cout << "average value:" << mean(v) << endl;
    cout << "max     value:" << max(v) << endl;
    cout << "min     value:" << min(v) << endl;


    return 0;
}
