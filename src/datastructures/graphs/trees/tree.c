#include <stdio.h>
#include <stdlib.h>
#include <string.h>


struct node {
    int num;
    struct node* left;
    struct node* right;
};

struct node* root;

void print_tree_depth(void) {

}

void insert_node(int newnum) {
    struct node* newnode;
    struct node* node_ptr;
    newnode = malloc(sizeof(struct node*));
    newnode->num = newnum;
    newnode->left = NULL;
    newnode->right = NULL;
    printf("inserting %d\n", newnode->num);
    if (root == NULL) {
        root = newnode;
        return;
    }
    node_ptr = root;
    while (node_ptr != NULL) {
        if (newnum == node_ptr->num) {
            printf("already added %d\n", newnum);
            return;
        }
        if (newnum < node_ptr->num) 
        {
            if (node_ptr->left == NULL) 
            {
                node_ptr->left = newnode;
                return;
            } 
            else 
            {
                node_ptr = node_ptr->left;
            } 
        } 
        else 
        {
            if (node_ptr->right == NULL) 
            {
                node_ptr->right = newnode;
                return;
            } 
            else 
            {
                node_ptr = node_ptr->right;
            } 

        }
    }
    printf("shouldn't be here!\n");
    return;
}

int main() {
    root = malloc(sizeof(struct node*));
    root->num = 5;
    root->left = NULL;
    root->right = NULL;
    insert_node(1);
    insert_node(2);
    insert_node(3);
    insert_node(4);

}
