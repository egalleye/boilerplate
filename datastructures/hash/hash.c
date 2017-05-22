#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int sdbm_hash(char* word){
    int itor;
    int hash_result;
    int hash_addr = 0;
    for (itor = 0; word[itor]!='\0'; itor++){
        hash_addr = word[itor] + (hash_addr << 6) + (hash_addr << 16) - hash_addr;
    }
    if (hash_addr < 0) hash_addr *= -1;
    hash_result = hash_addr % 128;
    return hash_result;
}

/*
int main(int argc, char* argv[]){
    char* test_str;
    int hash_result;
    test_str = malloc(sizeof(char)*strlen(argv[1]));
    strcpy(test_str, argv[1]);
    hash_result = sdbm_hash(test_str);
    printf("hash = %d\n", hash_result);
    free(test_str);
    return 0;
}
*/
