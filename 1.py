import random
from collections import deque

def tokenize_expression(s):
    """将表达式分割为独立的标记（数字、运算符、括号）"""
    tokens = []
    current_token = ''
    for char in s:
        if char in '+-*/d()':
            if current_token:
                tokens.append(current_token)
                current_token = ''
            tokens.append(char)
        else:
            current_token += char
    if current_token:
        tokens.append(current_token)
    return tokens

def infix_to_postfix(tokens):
    """将中缀表达式转换为后缀表达式（逆波兰表示法）"""
    precedence = {'(': 5, 'd': 4, '*': 3, '/': 3, '+': 2, '-': 2, ')': 1}
    output = []
    stack = []
    for token in tokens:
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # 弹出左括号
        else:
            while stack and stack[-1] != '(' and precedence[token] <= precedence.get(stack[-1], 0):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

def evaluate_postfix(postfix):
    """计算后缀表达式，处理骰子运算符"""
    stack = []
    for token in postfix:
        if token.isdigit():
            stack.append(int(token))
        else:
            if token == 'd':
                y = stack.pop()
                x = stack.pop()
                stack.append(sum(random.randint(1, y) for _ in range(x)))
            else:
                b = stack.pop()
                a = stack.pop()
                if token == '+': stack.append(a + b)
                elif token == '-': stack.append(a - b)
                elif token == '*': stack.append(a * b)
                elif token == '/': stack.append(a // b)  # 整除
    return stack[0]

def evaluate_dice_expression(expr):
    """整合流程：词法分析 -> 语法分析 -> 计算"""
    tokens = tokenize_expression(expr)
    postfix = infix_to_postfix(tokens)
    return evaluate_postfix(postfix)

# 示例测试
print(evaluate_dice_expression("3d6+5*2"))          # 示例：3d6+10
print(evaluate_dice_expression("(2d4+3)*5"))       # 示例：(2d4+3)*5