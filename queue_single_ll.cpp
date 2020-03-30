// implementing queues with singly linked lists

#include<iostream>
using namespace std;

// defining singly linked list as a struct
struct Qnode{
	int data;
	Qnode* next;
	Qnode(int d)
	{
		data = d;
		next = NULL;
	}
};

struct Queue{
	Qnode *front, *rear;
	Queue()
	{
		front = rear = NULL;
	}
	void enqueue(int x)
	{
		Qnode* temp = new Qnode(x);
		if (rear == NULL)
		{
			front = rear = temp;
			return;
		}
		rear->next = temp;
		rear = temp;
	}
	void dequeue()
	{
		if(front == NULL)
		{
			cout<<"stack underflow";
			return;
		}
		Qnode* temp = front;
		front = front->next;
		if (front == NULL)
			rear = NULL;
		delete(temp);
	}
};

int main() 
{ 
  
    Queue q; 
    q.enqueue(10); 
    q.enqueue(20); 
    q.dequeue(); 
    q.dequeue(); 
    q.enqueue(30); 
    q.enqueue(40); 
    q.enqueue(50); 
    cout << "Queue Front : " << (q.front)->data << endl; 
    cout << "Queue Rear : " << (q.rear)->data; 
} 