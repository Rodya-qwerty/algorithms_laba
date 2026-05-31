#include <iostream>
#include <stack>
#include <string>
#include <vector>
using namespace std;

struct Node {
	string val;
	Node* left; 
	Node* right;

	Node(string str) : val(str), left(nullptr), right(nullptr)  {}
};

Node* buildingTree(vector<string> exp) {
	stack<Node*> stack;

	for (int i = 0; i < exp.size(); i++) {
		string expr = exp[i];
		if (expr == "+" || expr == "-" || expr == "*" || expr == "/") {

			Node* right = stack.top();
			stack.pop();
			Node* left = stack.top();
			stack.pop();

			Node* oper = new Node(expr);
			oper->left = left;
			oper->right = right;

			stack.push(oper);
		}
		else {
			Node* num = new Node(expr);
			stack.push(num);
		}
	}
	return stack.top();
}

double calculate(Node* root) {
	if (root == nullptr) {
		return 0;
	}
	if (root->val != "+" && root->val != "-" && root->val != "*" && root->val != "/") {
		return stod(root->val); //str -> num
	}
	double leftval = calculate(root->left);
	double rightval = calculate(root->right);

	if (root->val == "+") {
		return leftval + rightval;
	}
	if (root->val == "-") {
		return leftval - rightval;
	}
	if (root->val == "*") {
		return leftval * rightval;
	}
	if (root->val == "/") {
		return leftval / rightval;
	}
	return 0;
}

int Treeheight(Node* root) {
	if (root == nullptr) { return 0; }

	int lefth = Treeheight(root->left);
	int righth = Treeheight(root->right);

	if (lefth > righth) {
		return 1 + lefth;
	}
	else {
		return 1 + righth;
	}
}

int main() {
	vector<string> n;
	n.push_back("2");
	n.push_back("5");
	n.push_back("*");
	n.push_back("3");
	n.push_back("+");

	cout << "Expression: ";
	for (int i = 0; i < n.size(); i++) {
		cout << n[i] << " ";
	}
	cout << endl << endl;

	Node* tree = buildingTree(n);

	double result = calculate(tree);
	cout << "res: " << result << endl;

	int height = Treeheight(tree);
	cout << "h: " << height << endl;

	return 0;
}