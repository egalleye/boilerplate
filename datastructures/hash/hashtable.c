#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include "hash.h"


char* hashtable[128][32];

int insert_hash(char* word) {
    int hash_idx, itor, wordlen;
    char* newhashword;
    wordlen = strlen(word);
    newhashword = malloc(sizeof(char)*wordlen);
    strncpy(newhashword, word, wordlen);
    hash_idx = sdbm_hash(newhashword);
    for (itor = 0; hashtable[hash_idx][itor] != NULL; ++itor){
        printf("[%d] = %s\n", itor, hashtable[hash_idx][itor]);
    }
    hashtable[hash_idx][itor] = newhashword;
  
    return 0;
}

void print_hashtable() {
    int itor;
    int inneritor;
    for (itor = 0; itor < 128; itor++) {
        printf("[%d] ", itor);
        for(inneritor = 0; hashtable[itor][inneritor] != NULL; inneritor++) {
            printf("%s ", hashtable[itor][inneritor]);
        }
        printf("\n");
    }
}

void delete_hashtable() {
    int itor;
    int inneritor;
    for (itor = 0; itor < 128; itor++) {
        for(inneritor = 0; hashtable[itor][inneritor] != NULL; inneritor++) {
            free(hashtable[itor][inneritor]);
        }
    }
}

int readfile(char* filename) {
    printf("filename = %s\n", filename);
    char c;
    char buffer[64];
    int fd;
    int idx = 0;
    int ret;
    fd = open(filename, O_RDONLY, S_IREAD);
    while(read(fd, &c, 1)) {
        if (c == ' ') {
            buffer[idx] = '\0';
            printf("word = %s\n", buffer);
            ret = insert_hash(buffer);
            idx = 0;
        } else {
            buffer[idx] = c;
            idx++;
        }
    }

    return 0;
}


void usage() {
    printf("usage:\n>./hashtable [filename.txt]\n");
    exit(0);
}
int main(int argc, char* argv[]) {
    if (argc != 2) usage();

    readfile(argv[1]);
    print_hashtable();
    return 0;
}

/*
int main(int argc, char* argv[]){
    int instrlen;
    char* test_str0;
    char test_str1[] = "bu";
    char test_str2[] = "bsdf";
    int hash_result;
    int ret;
    
    if (argc != 2) {
        printf("usage:\n./hashtable [word]\n");
        return 0;
    } 
    //instrlen = strlen(argv[1]);
    //test_str0 = malloc(sizeof(char)*instrlen);
    //strncpy(test_str0, argv[1], instrlen);
    print_hashtable();
    ret = insert_hash(argv[1]);
    print_hashtable();
    ret = insert_hash(test_str1);
    printf("Added bu\n");
    print_hashtable();
    ret = insert_hash(test_str2);
    printf("Added bsfd\n");
    print_hashtable();
    delete_hashtable();
    free(test_str0);
    return 0;
}
*/
