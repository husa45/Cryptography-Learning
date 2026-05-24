#include<iostream>
#include<string.h>
#define DELTA 0x9e3779b9

void XXTEA_encrypt(unsigned int* v,long n,unsigned int*k){
    unsigned long z=v[n-1],y,sum=0,e,p;
    if(n<2) return ;
    int rounds =6 +52/n;
    while(rounds-- >0){
sum+=DELTA;
e=(sum >>2) &3;

for(p=0;p<n-1;p++){
y=v[p+1];
z=v[p]+=
    ((z >>5 ^ y <<2)+(y >>3 ^z<<4)) ^
    ((sum ^y)+(k[(p&3)^e]^z));
}
y=v[0];
z=v[n-1] +=((z >>5 ^ y <<2)+(y >>3 ^z<<4)) ^
    ((sum ^y)+(k[(p&3)^e]^z));
    }
}
void XXTEA_decrypt(unsigned int* v,long n,unsigned int *k){
    unsigned long z,y=v[0],sum=0,e,p;
    if(n<2) return;
    unsigned rounds;
    rounds=6+52/n;
    sum=DELTA*rounds;
while(rounds--){
e=(sum >>2) &3;

for(p=n-1;p>0;p--){
z=v[p-1];
y=v[p]-=
    ((z >>5 ^ y <<2)+(y >>3 ^z<<4)) ^
    ((sum ^y)+(k[(p&3)^e]^z));
}
z=v[n-1];
y=v[0] -=((z >>5 ^ y <<2)+(y >>3 ^z<<4)) ^
    ((sum ^y)+(k[(p&3)^e]^z));
    sum-=DELTA;
    }
    
}
int main(void){
char plainData[] = "This text is pretty long, but will be "
                       "concatenated into just a single string. "
                       "The disadvantage is that you have to quote "
                       "each part, and newlines must be literal as "
                       "usual."
                       "This is fucken hillarious";
int plainLength=strlen(plainData);
int n=plainLength/4;
unsigned int blocks[n]={0};
for(int i=0;i<n;i++){
    blocks[i]=*(int *)(plainData+i*4);
}
unsigned int XTEA_KEY[4] = {0x798D038E,0x72319E4F,0xD00DDEE0,0xF001004E};
XXTEA_encrypt(blocks,n,XTEA_KEY);
for(int i=0;i<n;i++){
    //printf("%x\t",blocks[i]);
}
XXTEA_decrypt(blocks,n,XTEA_KEY);
for(int i=0;i<n;i++){
    char buff[4];
    buff[3]=(blocks[i]&0xff000000)>>24;
    buff[2]=(blocks[i]&0xff0000)>>16;
     buff[1]=(blocks[i]&0xff00)>>8;
     buff[0]=(blocks[i]&0xff) ;
    buff[4]=0;
    printf("%s",buff);
}
printf("\n");
}