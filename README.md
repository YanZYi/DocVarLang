# **DocVarLang** — 带语义描述的轻量级编程语言

[![](https://img.shields.io/badge/Version-1.0-blue)](https://github.com/your-repo/docvarlang)
[![](https://img.shields.io/badge/License-MIT-green)](https://github.com/your-repo/docvarlang/blob/main/LICENSE)
[![](https://img.shields.io/badge/Python-≥3.8-blue)](https://www.python.org/downloads/)

## **一、项目简介**

**DocVarLang** 是一种易用的编程语言，结合了 **变量语义描述** 与 **科学计算能力**：
- **变量带描述**：每个变量可存储值及文本描述，提升代码可读性。
- **内置类型**：支持 `整形(int)`、`浮点(float)`、`布尔(bool)`、`字符(char)` 及 **复数(complex)**（集成 NumPy 库）。
- **核心功能**：包含输入输出、表达式运算、逻辑判断、分支、循环等。
- **交互式终端**：模仿 Python 风格，支持实时输入与执行。

**适用场景**：教学、快速原型开发、科学计算实验。

## **二、快速开始**

1. **安装依赖**：

```bash
pip install numpy
```

2. **运行解释器**：

```
python docvarlang_interpreter.py
```

3. **交互式示例**：

```
# 声明变量（带描述）
let x = 10 "速度（单位：m/s）"

# 输出变量值及描述
output x
desc x

# 复数运算
let z = 2 + 3j
output np.abs(z)  # 使用 NumPy 计算模长

# 循环与条件判断
for i in range(5):
    if i % 2 == 0:
        output i "偶数"
```

## **三、核心特性**

### 1. 变量声明与描述

```
let name = value "描述文本"
# 示例：
let pi = 3.14159 "圆周率近似值"
```

### 2. 查询描述

```
desc variable_name  # 输出变量描述
```

### 3. 复数类型（NumPy 支持）

```
let z1 = 1 + 2j
let z2 = 4 - 3j
let result = z1 * z2  # 复数乘法
output np.angle(result)  # 计算辐角（弧度）
```

### 4. 控制流

```
# 条件判断
if condition:
    ...
else:
    ...

# 循环
for i in range(n):
    ...
```

## **四、使用示例：斐波那契数列**

```
# 初始化变量
let a = 0 "斐波那契首项"
let b = 1 "斐波那契第二项"
let count = 10 "项数"

# 计算并输出
for i in range(count):
    output a
    let temp = a
    let a = b
    let b = temp + b

# 查看最终值描述
desc b  # 输出："当前斐波那契值（55）"
```

## **五、贡献与反馈**

- **提交 Issue**：GitHub Issues
- **代码贡献**：欢迎提交 PR，请遵循 贡献指南。
- **联系方式**：XXX（邮箱/社交媒体）

## **六、许可证**

MIT License. 详见 LICENSE 文件。

---

**版权所有 (c) 2026 Joey Yan**

---

**--- 文档结束 ---**

**✨ 欢迎探索 DocVarLang！**
