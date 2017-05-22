#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct node {
    int data;
    struct node* next;
};

struct node* head;
struct node* tail;

void add(int data) {
    struct node* newnode;
    newnode = malloc(sizeof(struct newnode*));
    newnode->data = data;
    if (head == NULL) {
        head = tail = newnode;
        newnode->next = NULL;
    } else {
        tail->next = newnode;
        tail = newnode;
    }
}

int peek() {
    if (head == NULL) {
        printf("Queue is empty!\n");
        return 0;
    }
    return head->data;
}
int is_empty() {
    if (head == NULL) {
        printf("Queue is empty!\n");
        return 1;
    }
    return 0;
}

int remove_node() {
    struct node* oldnode;
    int ret;
    if (head == NULL) {
        printf("Queue is empty!\n");
        return 0;
    }
    oldnode = head;
    head = head->next;
    ret = oldnode->data;
    free(oldnode);
    return ret;
}

int main() {
    int result;
    add(1);
    add(2);
    add(3);
    add(4);
    add(5);
    result = remove_node();
    printf("result = %d\n", result);
    result = remove_node();
    printf("result = %d\n", result);
    result = peek();
    printf("result of peek = %d\n", result);
    result = remove_node();
    printf("result = %d\n", result);
    result = remove_node();
    printf("result = %d\n", result);
    printf("result = %d\n", result);
    printf("result = %d\n", result);
    printf("result = %d\n", result);
    
}
