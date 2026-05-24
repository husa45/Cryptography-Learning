#include<cstring>
#include<cstdlib>
#include<stdio.h>
#define COUNTER 32
#define DELTA 0x9e3779b9
void XTEA_encrypt(unsigned int* v,unsigned int* key){
    unsigned int v0=v[0],v1=v[1];
    unsigned int sum=0;
    for(int i=0;i<COUNTER;i++){
        v0 +=(((v1 <<4)^(v1 >>5))+v1) ^(sum +key[sum&3]);
        sum+=DELTA;
        v1 +=(((v0 <<4)^(v0 >>5))+v0) ^(sum +key[(sum >>11)&0x3]);
    }
    v[0]=v0;
    v[1]=v1;
}
void XTEA_decrypt(unsigned int* v,unsigned int* key){
    unsigned int v0=v[0],v1=v[1];
    unsigned int  sum=COUNTER *DELTA;
    for(int i=0;i<COUNTER;i++){
        v1 -=(((v0 <<4)^(v0 >>5))+v0) ^(sum +key[(sum >> 11)&3]);
        sum-=DELTA;
        v0 -=(((v1 <<4)^(v1 >>5))+v1) ^(sum +key[sum&3]);
    }
    v[0]=v0;
    v[1]=v1;
}
int main(){
    //read plain input:
    char plainData[] = "This text is pretty long, but will be "
                       "concatenated into just a single string. "
                       "The disadvantage is that you have to quote "
                       "each part, and newlines must be literal as "
                       "usual."
                       "This is fucken hillarious";
    // fgets(plainData, 1024, stdin);
    int plainLength = 11;//strlen(plainData) / 8;
    // divide into 64 bit blocks ,and encrypt every block;
    // key:
    unsigned int TEA_KEY[4] = {0x798D038E,0x72319E4F,0xD00DDEE0,0xF001004E};
    //
    int initialSize = 8;
    char *encrypted = (char *)calloc(initialSize, 1);
    unsigned int *ptr = (unsigned int *)plainData;
   
   char * ptrHeap1 = encrypted;
    for (int i = 0; i <= plainLength; i++)
    {
        XTEA_encrypt(ptr, TEA_KEY);
        memcpy(ptrHeap1, ptr, 8);
        encrypted = (char *)realloc((void *)encrypted, initialSize +=8);
        ptrHeap1 += 8;
        // move it 8 bytes forward;
        ptr += 2;
    }

    //decrypting symmetrically:
    initialSize = 8;
    unsigned int *decrypted = (unsigned int *)calloc(initialSize, 1);
    unsigned int *ptrHeap2 = decrypted;
    unsigned int enc[12]={0xf7c3a0f5, 0x3e209b64,0xd87922ea, 0x817b39bf,0xc91d00bd, 0xc54efbf9,0xb8e4498f, 0xbf64fe19,0x5f5f552a, 0x68ac7cea,0x3bfc6cf2, 0xbb160c7e};
    unsigned int *ptrEncrypted = (unsigned int *)enc;
    for (int i = 0; i <= plainLength; i++)
    {
        XTEA_decrypt(ptrEncrypted, TEA_KEY);
        memcpy(ptrHeap2, ptrEncrypted, 8);
        decrypted= (unsigned int *)realloc((void *)decrypted, initialSize +=8);
        ptrEncrypted += 2;
        ptrHeap2 += 2;
    }
    printf("%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n%d\n",decrypted[0],decrypted[1],decrypted[2],decrypted[3],decrypted[4],decrypted[5],decrypted[6],decrypted[7],decrypted[8],decrypted[9],decrypted[10],decrypted[11]);
    free(decrypted);
    free(encrypted);
}