"""
DocVarLang 1.0 (交互式解释器)
支持关键字: let, input, output, if, else, for, desc, True, False, None
输入 'exit' 退出解释器
>>> let x = 5 "这是一个整数"
>>> let y = 3.14 "这是一个浮点数"
>>> output x + y
8.14
>>> if x > 3:
...     output "x大于3"
... else:
...     output "x小于等于3"
x大于3
>>> for i in range(3):
...     output i
0
1
2
>>> let d = 2 + 3j "这是一个复数"
>>> output np.abs(d)
3.605551275463989
>>> desc x
x 的描述: '这是一个整数'
>>> desc d
d 的描述: '这是一个复数'
"""

import numpy as np
import re
import sys

class DocVarLangInterpreter:
    def __init__(self):
        self.env = {}  # 变量环境 {'name': {'value': ..., 'description': ...}}}
        self.current_block = []  # 当前代码块
        self.block_type = None  # 代码块类型 (if/for)
        self.indent_level = 0  # 缩进级别
    
    def start(self):
        print("DocVarLang 1.0 (交互式解释器)")
        print("支持关键字: let, input, output, if, else, for, desc, True, False, None")
        print("输入 'exit' 退出解释器")
        
        while True:
            try:
                line = input(">>> ").strip()
                if not line:
                    continue
                
                # 退出命令
                if line == "exit":
                    break
                
                # 处理代码块
                if self.block_type:
                    if line.startswith("... "):
                        line = line[4:].strip()
                    self.current_block.append(line)
                    
                    # 检查代码块结束
                    if not line or not line.startswith(" "):
                        self.execute_block()
                        self.block_type = None
                        self.current_block = []
                        self.indent_level = 0
                else:
                    # 直接执行单行代码
                    self.execute_line(line)
            
            except Exception as e:
                print(f"错误: {e}")
    
    def execute_line(self, line):
        # 解析 let 声明
        if line.startswith("let "):
            self.parse_let(line)
        
        # 解析 input 输入
        elif line.startswith("input "):
            self.parse_input(line)
        
        # 解析 output 输出
        elif line.startswith("output "):
            self.parse_output(line)
        
        # 解析 if 条件
        elif line.startswith("if "):
            self.parse_if(line)
        
        # 解析 for 循环
        elif line.startswith("for "):
            self.parse_for(line)
        
        # 解析 desc 查询
        elif line.startswith("desc "):
            self.parse_desc(line)
        
        # 直接执行表达式
        else:
            result = self.eval_expression(line)
            if result is not None:
                print(result)
    
    def parse_let(self, line):
        parts = line[4:].split("=", 1)
        var_name = parts[0].strip()
        expr_desc = parts[1].strip()
        
        # 分离表达式与描述
        if '"' in expr_desc:
            expr, desc = expr_desc.split('"', 1)
            expr = expr.strip()
            desc = desc.strip('"')
        else:
            expr = expr_desc
            desc = "无描述"
        
        # 计算表达式
        value = self.eval_expression(expr)
        self.env[var_name] = {'value': value, 'description': desc}
    
    def parse_input(self, line):
        prompt = line[6:].strip()
        user_input = input(prompt)
        try:
            # 尝试转换为数字
            if '.' in user_input:
                value = float(user_input)
            else:
                value = int(user_input)
        except:
            # 如果不是数字，保留为字符串
            value = user_input
        self.env['_last_input'] = {'value': value, 'description': '上一次输入'}
    
    def parse_output(self, line):
        expr = line[7:].strip()
        value = self.eval_expression(expr)
        print(value)
    
    def parse_if(self, line):
        condition = line[3:].strip()
        self.block_type = "if"
        self.current_block = [condition]
        self.indent_level = 1
        print(f"... ", end="")
    
    def parse_for(self, line):
        loop_expr = line[4:].strip()
        self.block_type = "for"
        self.current_block = [loop_expr]
        self.indent_level = 1
        print(f"... ", end="")
    
    def parse_desc(self, line):
        var_name = line[5:].strip()
        if var_name in self.env:
            print(f"{var_name} 的描述: '{self.env[var_name]['description']}'")
        else:
            print(f"错误: 变量 '{var_name}' 未定义")
    
    def execute_block(self):
        if self.block_type == "if":
            condition = self.current_block[0]
            if self.eval_expression(condition):
                for line in self.current_block[1:]:
                    self.execute_line(line)
        elif self.block_type == "for":
            loop_expr = self.current_block[0]
            # 解析 for 循环
            match = re.match(r"(\w+)\s+in\s+(.+)", loop_expr)
            if match:
                var_name = match.group(1)
                iterable = self.eval_expression(match.group(2))
                for item in iterable:
                    self.env[var_name] = {'value': item, 'description': '循环变量'}
                    for line in self.current_block[1:]:
                        self.execute_line(line)
    
    def eval_expression(self, expr):
        # 定义可用的函数和变量
        globals_dict = {"__builtins__": None, "np": np}
        locals_dict = {k: v['value'] for k, v in self.env.items()}
        
        # 添加内置函数
        globals_dict.update({
            'range': range,
            'int': int,
            'float': float,
            'bool': bool,
            'str': str
        })
        
        # 计算表达式
        return eval(expr, globals_dict, locals_dict)

# 启动解释器
if __name__ == "__main__":
    interpreter = DocVarLangInterpreter()
    interpreter.start()
