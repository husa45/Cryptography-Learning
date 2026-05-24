#include<iostream>
#include<cstring>
#define DELTA  0x9E3779B9
#define COUNTER 32
//No padding is used:
void TEA_encrypt(int *v,unsigned int* k){
    int v0 = v[0], v1 = v[1];
    long sum = 0;                                                                                                                                                               
    for (int i = 0; i < COUNTER;i++){
        v0 += ((v1 << 4) + k[0]) ^ (sum + v1) ^ ((v1 >> 5) + k[1]);
        v1 += ((v0<< 4) + k[2]) ^ (sum + v0) ^ ((v0 >> 5) + k[3]);
        sum += DELTA;
        v[0] = v0;
        v[1] = v1;
    }
}
void TEA_decrypt(int *v,unsigned int* k){
    int v0 = v[0], v1 = v[1];
    long sum = COUNTER * DELTA;
    for (int i = 0; i < 32; i++)
    {
        sum -= DELTA;
        v1 -= ((v0 << 4) + k[2]) ^ (sum + v0) ^ ((v0 >> 5) + k[3]);
        v0 -= ((v1 << 4) + k[0]) ^ (sum + v1) ^ ((v1 >> 5) + k[1]);
        v[0] = v0;
        v[1] = v1;
    }
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
    int plainLength = strlen(plainData) / 8;
    // divide into 64 bit blocks ,and encrypt every block;
    // key:
    unsigned int TEA_KEY[4] = {0x01234567, 0x89ABCDEF, 0xFEDCBA98, 0x76543210};
    //
    int initialSize = 8;
    char *encrypted = (char *)calloc(initialSize, 1);
    int *ptr = (int *)plainData;
   
   char * ptrHeap1 = encrypted;
    for (int i = 0; i <= plainLength; i++)
    {
        TEA_encrypt(ptr, TEA_KEY);
        memcpy(ptrHeap1, ptr, 8);
        encrypted = (char *)realloc((void *)encrypted, initialSize +=8);
        ptrHeap1 += 8;
        // move it 8 bytes forward;
        ptr += 2;
    }
    printf("%s\n", encrypted);
    //decrypting symmetrically:
    initialSize = 8;
    char *decrypted = (char *)calloc(initialSize, 1);
    char *ptrHeap2 = decrypted;
    int *ptrEncrypted = (int *)encrypted;
    for (int i = 0; i <= plainLength; i++)
    {
        TEA_decrypt(ptrEncrypted, TEA_KEY);
        memcpy(ptrHeap2, ptrEncrypted, 8);
        decrypted= (char *)realloc((void *)decrypted, initialSize +=8);
        ptrEncrypted += 2;
        ptrHeap2 += 8;
    }
    printf("Decrypted %s\n", decrypted);
    free(decrypted);
    free(encrypted);
}