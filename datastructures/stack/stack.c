#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct node {
    int data;
    struct node* next;
};

struct node* head;


int pop() {
    struct node* n;
    int ret;
    if (head == NULL) {
        printf("stack is empty\n");
        return 0;
    }
    n = head;
    head = head->next;
    ret = n->data;
    free(n);
    return ret;
}

void push(int data) {
    struct node* newnode;
    newnode = malloc(sizeof(struct node*));
    newnode->data = data;
    newnode->next = head;
    head = newnode;
}

int peek() {
    if (head == NULL) {
        printf("stack is empty\n");
        return 0;
    }
    return head->data;
}

int main() {
    int result;
    push(1);
    push(2);
    push(3);
    push(4);
    result = peek();
    printf("result = %d\n", result);
    result = pop();
    printf("result = %d\n", result);
    result = pop();
    printf("result = %d\n", result);
    result = pop();
    printf("result = %d\n", result);
    result = pop();
    printf("result = %d\n", result);
}
