Дерево выражений для постфиксной записи
# Описание проекта
Программа преобразует математическое выражение из постфиксной формы (обратная польская запись) в бинарное дерево выражений и вычисляет его значение. В дереве листья содержат операнды (целые числа), а внутренние узлы — операторы (+, -, *, /).

# Реализованный функционал
Построение дерева выражений из постфиксной записи
Вычисление значения выражения с помощью рекурсивного обхода
Определение высоты дерева
Обработка ошибок (деление на ноль, некорректные операторы)

Структура узла дерева
cpp
struct Node {
    string val;        // значение: число или оператор
    Node* left;        // левый потомок
    Node* right;       // правый потомок
    
    Node(string x) : val(x), left(nullptr), right(nullptr) {}
};
Алгоритмы
1. Построение дерева
Принцип работы:

Используется стек узлов

При встрече операнда → создаётся узел-лист и помещается в стек

При встрече оператора → извлекаются 2 узла из стека (правый и левый операнды), создаётся внутренний узел с оператором, который помещается в стек

cpp
Node* buildingTree(vector<string> exp) {
    stack<Node*> st;
    
    for (string token : exp) {
        if (isOperator(token)) {
            Node* right = st.top(); st.pop();
            Node* left = st.top(); st.pop();
            
            Node* oper = new Node(token);
            oper->left = left;
            oper->right = right;
            
            st.push(oper);
        } else {
            st.push(new Node(token));
        }
    }
    return st.top();
}
Пример построения для выражения 3 4 + 2 *:

text
Шаг 1: 3 → [3]
Шаг 2: 4 → [3, 4]
Шаг 3: + → извлекаем 4 и 3, создаём узел [+] → [+]
Шаг 4: 2 → [+, 2]
Шаг 5: * → извлекаем 2 и +, создаём узел [*] → [*]
2. Вычисление выражения
Рекурсивный алгоритм:

Если узел — число → возвращаем его числовое значение

Если узел — оператор → рекурсивно вычисляем левое и правое поддеревья, применяем оператор

cpp
double calculate(Node* root) {
    if (!root) return 0;
    
    // Лист (число)
    if (!isOperator(root->val)) {
        return stod(root->val);
    }
    
    // Внутренний узел (оператор)
    double leftVal = calculate(root->left);
    double rightVal = calculate(root->right);
    
    if (root->val == "+") return leftVal + rightVal;
    if (root->val == "-") return leftVal - rightVal;
    if (root->val == "*") return leftVal * rightVal;
    if (root->val == "/") return leftVal / rightVal;
    
    return 0;
}
3. Определение высоты дерева
Высота — максимальное количество узлов на пути от корня до листа.

cpp
int Treeheight(Node* root) {
    if (!root) return 0;
    
    int leftHeight = Treeheight(root->left);
    int rightHeight = Treeheight(root->right);
    
    return 1 + max(leftHeight, rightHeight);
}
