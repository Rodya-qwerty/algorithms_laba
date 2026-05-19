def check_brackets(string):
    stack = []
    
    brackets_map = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    for char in string:
        if char in '([{':
            stack.append(char)
        
        elif char in ')]}':
            if len(stack) == 0:
                return False
            
            if stack.pop() != brackets_map[char]:
                return False
    
    return len(stack) == 0


def check_multiple_strings(strings):
    for s in strings:
        result = check_brackets(s)
        print(f"{s} -> {result}")


if __name__ == "__main__":
    test_strings = ["()", "([)]", "{[]}", ')[]{}', "([{}])", "((())"]
    check_multiple_strings(test_strings)