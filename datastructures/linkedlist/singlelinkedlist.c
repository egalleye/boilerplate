#include <stdio.h>
#include <stdlib.h>
#include <string.h>

struct node {
    int data;
    struct node* next;
};

struct node* head;

int append_node(int newdata) {
    struct node* newnode;
    struct node* n;
    printf("adding node %d\n", newdata);
    newnode = (struct node*) malloc(sizeof(struct node*));
    newnode->data = newdata;
    newnode->next = NULL;
    if (head == NULL) {
        head = newnode;
        return 0;
    } else {
        for (n = head; n->next != NULL; n = n->next);
        n->next = newnode;
    }
    return 0;
    
}

void print_list() {
    struct node* n;
    for (n = head; n->next != NULL; n = n->next) {
        printf("n->data = %d\n", n->data);
    }
    printf("n->data = %d\n", n->data);
}

int insert_node(int index, int data) {
    int itor;
    struct node* newnode;
    struct node* n;

    newnode = malloc(sizeof(struct node*));
    newnode->data = data;
    newnode->next = NULL;
    printf("inserting %d\n", newnode->data);
    if (head == NULL) {
        head = newnode;
    } else {
        for (itor = 0, n = head; itor < index - 1; itor++, n = n->next) {
            if (n->next == NULL) {
                printf("Index off end of list\n");
                newnode->next = n->next;
                n->next = newnode;
                return 0;
            }
        }
        newnode->next = n->next;
        n->next = newnode;
    }
        
    return 0;
}

void delete_node(int data) {
    struct node* n;
    struct node* rn;
    for (n = head; n->next != NULL; n = n->next) {
        if (n->next->data == data) {
            rn = n->next;
            n->next = n->next->next;
            break;
        }
    }
    if (rn->data == data) {
        printf("deleting node %d\n", rn->data);
        free(rn);
    } else {
        printf("Node %d not found\n", data);
    }
}


int main() {
    append_node(1);
    append_node(2);
    append_node(3);
    print_list();
    append_node(4);
    //append_node(5);
    append_node(6);
    append_node(7);
    insert_node(6, 8);
    print_list();
    delete_node(3);
    print_list();
    delete_node(8);
    print_list();

    return 0;
}
