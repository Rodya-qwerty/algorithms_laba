def check_brackets(string, typ):
    stack = []
    
    brackets_map = {
        ')': '(',
        ']': '[',
        '}': '{'
    }
    
    count = 0
    for char in string:
        if typ == char: count+=1
        if char in '([{':
            stack.append(char)
        
        elif char in ')]}':
             if typ == char: count+=1
            if len(stack) == 0:
                return False
            
            if stack.pop() != brackets_map[char]:
                return False
    
    return len(stack) == 0


def check_strings(strings):
    for s in strings:
        result = check_brackets(s)
        print(f"{s} -> {result}")


if __name__ == "__main__":
    strings = ["()", "([)]", "{[]}", ')[]{}', "([{}])", "((())"]
    check_strings(strings)
    # h