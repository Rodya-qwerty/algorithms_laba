#include <iostream>
#include <climits>
#include <vector>
#include <algorithm>
using namespace std;


int algoritm_deykstra(int** matrix, const int n, int start, int end){

    int* ves = new int[n];
    for (int i = 0; i < n; i++)
        ves[i] = INT_MAX;

    ves[start] = 0;
    bool* posetil = new bool[n]{false};
    int* pred = new int[n];
    for (int i = 0; i < n; i++)
        pred[i] = -1;

    for (int q = 0; q<n; q++){

        int min_el = INT_MAX;
        int u = -1;
        for (int i = 0; i < n; i++){
            if ( (ves[i] < min_el) && (!posetil[i]) ){
                min_el = ves[i] ;
                u = i;
            }
        }

        if (u == -1)
            break;

        posetil[u] = true;

        for (int i = 0; i < n; i++){
            if (matrix[u][i] > 0){
                int new_ves = matrix[u][i] + ves[u];
                if (ves[i] > new_ves){
                    ves[i] = new_ves;
                    pred[i]=u;

                }
            }
        }
    }
    
    for (int i = 0; i < n; i++){
        cout << ves[i] << " ";
    }
    cout<<endl;
    int* path=new int[6];
    int size=0; 
    for (int i = end; i !=-1; i = pred[i]){
        path[size++] = i;
             
    }
    for (int i = size-1; i >=0 ; i--){
        cout<<path[i];
        if(i>0) cout<<" -> ";
             
    }
    return ves[end];

}

struct connect {
    int a = -1;
    int b = -1;
    int ves = -1;
};

connect* algoritm_kruskala(int** matrix, int n) {
    connect* ans = new connect[n - 1];
    int count = 0;

    // Компоненты связности
    int* comp = new int[n];
    for (int i = 0; i < n; i++)
        comp[i] = i;

    while (count < n - 1) {
        int min_ves = INT_MAX;
        int a = -1, b = -1;

        // Поиск минимального ребра
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                if (matrix[i][j] > 0 && matrix[i][j] < min_ves) {
                    min_ves = matrix[i][j];
                    a = i;
                    b = j;
                }
            }
        }

        if (a == -1 || b == -1) break;  // несвязный граф

        // Запоминаем вес и удаляем ребро из матрицы
        int weight = min_ves;
        matrix[a][b] = 0;
        matrix[b][a] = 0;

        // Проверяем, что вершины в разных компонентах
        if (comp[a] != comp[b]) {
            ans[count].a = a;
            ans[count].b = b;
            ans[count].ves = weight;
            count++;

            // Объединяем компоненты: все с номером comp[b] получают comp[a]
            int old_comp = comp[b];
            int new_comp = comp[a];
            for (int i = 0; i < n; i++) {
                if (comp[i] == old_comp)
                    comp[i] = new_comp;
            }
        }
    }

    delete[] comp;
    return ans;
}

class listNode{
public:
    int value;
    int key;
    listNode* next = nullptr;

    listNode(int value, int key):value(value),  key(key) {}

};

class MyHashMap {

private:

    listNode** head = new class listNode*[10] {nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr,nullptr};

public:
    
    void put(int key, int value) {
        int mup = key%10;
        if (head[mup] == nullptr){
            head[mup] = new listNode(value, key);
        }
        else{
            listNode* temp = head[mup];
            while(temp->next != nullptr && key != temp->key){
                temp = temp->next;
            }
            if(key == temp->key){
                    temp->value = value; 
            }
            else{
                temp->next = new listNode(value, key);
            }
        }
    }
    
    int get(int key) {
        int mup = key%10;
        if (head[mup] == nullptr){
           return -1;
        }
        listNode* temp = head[mup];
        while(temp->next != nullptr){
            if (temp->key == key){
                return temp->value;
            }
            temp = temp->next;
        }
        if (temp->key == key)
            return temp->value;
        return -1;
    }
    
    void remove(int key) {
        int mup = key%10;
        if (head[mup] == nullptr){
           return;
        }

        listNode* previously_temp = head[mup];
        if (head[mup]->key == key) { head[mup] = head[mup] -> next; return;}
        if (head[mup]->next == nullptr) {return;}
        listNode* temp = head[mup]->next;
        while(temp->next != nullptr){
            if (temp->key == key){
               previously_temp->next = temp->next;
               return; 
            }
            previously_temp = temp;
            temp = temp->next;
        }
        if (temp->key == key)
            previously_temp->next = nullptr;
    }
    
};

std::vector<int> find_way_out_in_labirint(int** matrix, int n, int start, int stop){
/*Найти кратчайший путь в лабиринте, где клетки имеют разную стоимость прохода. Нужно
выбрать подходящий алгоритм и объяснить выбор.*/

    // Решенеи будет представлять алгоритм Дейкстры
    
    // Заготовки: массивы с посещёнными и не посещёнными точками. Веса в каждой точке, старт 0, остольные "бесконечность", история 
    std::vector<bool> unvisit (n, true);
    std::vector<bool> visited (n, false);
    std::vector<int> ves (n, INT_MAX);
    ves[start] = 0; 
    std::vector<int> previousle(n, -1);

    // Пройдём по всем точкам, от них посмотрим соседий и сравним стоимость прохода до данной точки 
    for (int q = 0; q<n; q++){
        
        // будем искать минимальную точку относительно непросмотренных, так как реализуем "жадный алгоритм"
        int u = -1;
        int weight = INT_MAX;
        for(int i = 0; i<n; i++){
            if ( unvisit[i] &&  weight > ves[i]){
                u = i;
                weight =ves[i];
            }
        }

        if (u == -1)
            break;
        
        visited[u] = true; 
        unvisit[u] = false; 
        
        // Смотрим сосебей и проверяем путь до них, выбирая минимальный 
        for (int i = 0; i < n; i++){
            if(matrix[u][i] > 0){
                int new_weight = ves[u] + matrix[u][i];
                if (new_weight < ves[i]){
                    ves[i] = new_weight;
                    previousle[i] = u;
                }
            }
        }

        }

    for (int i = 0; i < ves.size(); i++){
        cout << ves[i] << " ";
    }

    cout << "\n";

    int t = stop; 
    while ( t != -1 ){
        cout << t <<"<--"; 
        t = previousle[t];
    }

        return ves; 
}



int main(){

    const int n = 6;
    int** matrix = new int*[n] {
    new int[n]{0, 3, 1, 3, 0, 0},
    new int[n]{3, 0, 4, 0, 0, 0},
    new int[n]{1, 4, 0, 0, 7, 5},
    new int[n]{3, 0, 0, 0, 0, 2},
    new int[n]{0, 0, 7, 0, 0, 4},
    new int[n]{0, 0, 5, 2, 4, 0}
    };


    find_way_out_in_labirint(matrix,n, 0, 1) ;




    for (int i = 0; i < 6; i++) delete[] matrix[i];
    delete[] matrix;




    return 0;
}