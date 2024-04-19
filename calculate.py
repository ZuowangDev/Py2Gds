import re 

# 功能：将模型文件中的表达式中需要用户输入的变量换成值
def replace_variables(expression, variables):  

    # 使用正则表达式找到所有的变量（变量名由字母、数字和下划线组成）  
    pattern = r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b'  

    # 使用字典中的值替换表达式中的变量  
    def replace_var(match):  
        var_name = match.group(1) 

        # 如果变量不存在，则返回变量名本身   
        return str(variables.get(var_name, var_name)) 
    
    # 使用re.sub和回调函数替换变量   
    return re.sub(pattern, replace_var, expression)  

# 功能：判断是否是运算符
def is_operator(token):  
    return token in ['+', '-', '*', '/', '%', '<', '>', '&', '|']

# 功能：定义运算符优先级
def get_precedence(op):  
    precedences = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '<': 3, '>': 3, '&': 4,'|': 4}  
    return precedences[op]  

# 功能：支持浮点数，判断是否是数字
def is_number(s):  
    try: 

        # 尝试将字符串转换为浮点数  
        float(s)
        return True  
    except ValueError:  
        return False

# 功能：将中缀表达式转换成逆波兰表达式
def infix_to_postfix(expression: str):

    # 定义了两个栈
    # output：输出，stack：临时  
    output = []  
    stack = []  
    tokens = expression.replace('(', ' ( ').replace(')', ' ) ').split()  
  
    for token in tokens:  
        if is_number(token): 

            # 操作数直接压入output
            output.append(token)  
        elif is_operator(token):  
            while stack and is_operator(stack[-1]) and get_precedence(stack[-1]) >= get_precedence(token): 

                # 判断stack中优先级和待处理运算符优先级的关系
                # 弹出最后一个运算符，直到stack中的优先级都小于待处理运算符 
                output.append(stack.pop())  
            stack.append(token)  
        elif token == '(': 

            # 遇到左括号直接压入
            stack.append(token)  
        elif token == ')': 

            # 右括号一直弹出，直到遇到左括号，相当于堆栈中的堆栈
            top_token = stack.pop()  
            while top_token != '(':  
                output.append(top_token)  
                top_token = stack.pop()  
        else:  
            raise ValueError(f"Invalid token {token}")  
  
    while stack:  
        if stack[-1] == '(':  
            raise ValueError("Mismatched parentheses in expression")  
        output.append(stack.pop())

    # 返回的结果是转换出的逆波兰表达式 

    return ' '.join(output)  

# 功能：计算逆波兰表达式的值
def evaluate_postfix(postfix_expression: str):  
    stack = []  
    tokens = postfix_expression.split()  
  
    for token in tokens:  
        if is_number(token):  
            stack.append(float(token))  
        elif token in ['+', '-', '*', '/', '%', '<', '>', '&', '|']:  
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")  
            # 处理逻辑运算符  
            if token == '&':  
                b = stack.pop()  
                a = stack.pop()  
                result = a and b  
            elif token == '|':  
                b = stack.pop()  
                a = stack.pop()  
                result = a or b  
            # 处理比较运算符  
            elif token in ['<', '>']:  
                b = stack.pop()  
                a = stack.pop()  
                if token == '<':  
                    result = a < b  
                elif token == '>':  
                    result = a > b  
            # 处理算术运算符（这部分代码保持不变）  
            else:  
                b = stack.pop()  
                a = stack.pop()  
                if token == '+':  
                    result = a + b  
                elif token == '-':  
                    result = a - b  
                elif token == '*':  
                    result = a * b  
                elif token == '/':  
                    if b == 0:  
                        raise ValueError("Division by zero")  
                    result = a / b  
                elif token == '%':  
                    result = a // b  
  
            stack.append(result)   
        else:  
            raise ValueError(f"Invalid token {token} in postfix expression")  
  
    if len(stack) != 1:  
        raise ValueError("Invalid postfix expression")  
    
    # 堆栈中最后一个值就是结果
    return stack[0]

# 功能：整合计算函数
def count_total(expression: str, variables: dict):
    result = round(evaluate_postfix(infix_to_postfix(replace_variables(expression,variables))), 4)
    if isinstance(result, float) and result.is_integer():  
        result = int(result)
    return result

# 功能：获取所有变量名
def extract_variable_names(lst, variable_names):  
    # 假设lst是一个字符串列表，variable_names是一个包含要查找的变量名的字符串列表  
    found_variables = []  
      
    # 遍历variable_names列表中的每个变量名  
    for var_name in variable_names:  
        # 遍历lst列表中的每个元素  
        for item in lst:  
            # 检查元素是否为字符串类型，并且是否包含当前变量名  
            if isinstance(item, str) and var_name in item:  
                # 如果找到，则添加到结果列表中  
                found_variables.append(var_name)  
      
    # 返回找到的变量名列表（去重）  
    return list(set(found_variables))

# 功能：分解复杂带入第一步：将某一循环变量带入字符串列表
def rcp0(expression: list, key: str, vl: list):
    temp = []
    for pu in expression:
        for item in vl:
            dict = {key: item}
            temp.append(replace_variables(pu, dict))
    return temp

# 功能：分解复杂带入第二步：将值字典带入字符串列表
def rcp1(expression: list, value: dict):
    temp = []
    
    temp.append(expression)
    t = 0

    for item in value:
        temp.append(rcp0(temp[t], item, value[item]))

        t = t + 1
    return temp[-1]

# 功能：循环参数计算总值
def cir_total(expression: list, value: dict):
    keys_list = list(value.keys())  
    dictor = {}
    v_have= extract_variable_names(expression, keys_list)
    for item in v_have:
        dictor[item] = value[item]

    le = 1
    for key, vl in dictor.items():
        le = le * len(vl)

    temp = rcp1(expression, dictor)
    step = []
    for item in temp:
        step.append(round(evaluate_postfix(infix_to_postfix(item)), 4))

    for index, value in enumerate(step):  
        if isinstance(value, float) and value.is_integer():  
            step[index] = int(value)

    result = []
    for i in range(le):
        result.append([step[i], step[i + le], step[i + le * 2], step[i + le * 3], step[i + le * 4], step[i + le * 5]])

    return result

# 功能：处理layermap
def process_layermap(e_list: list, v_list: list):
    tmp = []
    for item in v_list:
        if e_list[4] == item[0]:
            if e_list[5] == item[1]:
                tmp = [item[2], item[3]]
            else:
                continue
        else:
            continue
    if tmp == []:
        tmp = [e_list[4], e_list[5]]
    return tmp
