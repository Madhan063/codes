// implementing stacks with singly linked lists

#include<iostream>
#include <bits/stdc++.h>
using namespace std;

struct Node{
	int data;
	struct Node* link;
};
struct Node* top;

void push(int x)
{
	struct Node* temp;
	temp = new Node();
	if (!temp)			// To chech if stack is full or empty
	{
		cout<<"stack overflow";
		exit(1);
	}
	temp->data = x;
	temp->link = top;
	top = temp; 
}
int isempty()
{
	return top == NULL;
}
int peek()
{
	if (isempty())
	{
		cout<<"stack underflow";
		exit(1);
	}
	return top->data;
}
void pop()
{
	struct Node* temp;
	temp = new Node();
	if (isempty())
	{
		cout<<"stack underflow"<<endl;
		exit(1);
	}
	temp = top;
	top = top->link;
	temp->link = NULL;
	free(temp);
}
void display()
{
	if (isempty())
	{
		cout<<"stack underflow"<<endl;
		exit(1);
	}
	struct Node* temp;
	temp = new Node();
	temp = top;
	while(temp!= NULL)
	{
		cout<<temp->data<<" ";
		temp = temp->link;
	}
}

int main() 
{ 
    // push the elements of stack 
    push(11); 
    push(22); 
    push(33); 
    push(44); 
  
    // display stack elements 
    display(); 
  
    // print top element of stack 
    cout << "\nTop element is " <<peek()<<endl; 
  
    // delete top elements of stack 
    pop(); 
    pop(); 
  
    // display stack elements 
    display(); 
  
    // print top element of stack 
    cout << "\nTop element is " <<peek()<<endl; 
    return 0; 
  
    // This code has been contributed by Striver  
}