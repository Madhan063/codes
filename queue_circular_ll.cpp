// circular queue with circular linked lists
#include<iostream>
#include <bits/stdc++.h>
using namespace std;

struct Node{
	int data;
	struct Node* link;
};

struct Queue
{
	struct Node *front, *rear;
	
};

void enqueue(Queue *q,int x)
{
	struct Node *temp = new Node;
	temp->data = x;
	if (q->front == NULL)
		q->front = q->rear = temp;
	else q->rear->link = temp;
	q->rear = temp;
	q->rear->link = q->front;
}
int dequeue(Queue *q)
{
	if(q->front == NULL)
	{
		cout<<"queue underflow";
		exit(1);
	}
	int value;
	if (q->front == q->rear)
	{
		value = q->front->data;
		free(q->front);
		q->front = NULL;
		q->rear = NULL;
	}
	else
	{
		struct 	Node* temp = new Node();
		temp = q->front;
		value = temp->data;
		q->front = temp->link;
		q->rear->link = q->front;
		free(temp);
	}
	return value;
}

void display(struct Queue *q)
{
	struct Node *temp = q->front;
	if (q->front == NULL)
	{
		cout<<"stack empty";
		exit(1);
	}
	while (temp->link != q->front)
	{
		cout<<temp->data<<" ";
		temp = temp->link;
	}
	cout<<temp->data<<endl;
}

int main() 
{ 
    // Create a queue and initialize front and rear 
    Queue *q = new Queue; 
    q->front = q->rear = NULL; 
  
    // Inserting elements in Circular Queue 
    enqueue(q, 14); 
    enqueue(q, 22); 
    enqueue(q, 6); 
  
    // Display elements present in Circular Queue 
    display(q); 
  
    // Deleting elements from Circular Queue 
    printf("\nDeleted value = %d", dequeue(q)); 
    printf("\nDeleted value = %d", dequeue(q)); 
  
    // Remaining elements in Circular Queue 
    display(q); 
  
    enqueue(q, 9); 
    enqueue(q, 20); 
    display(q); 
  
    return 0; 
} 