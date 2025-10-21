
---

# 📘 Markdown 语法速查表

## 1. 标题 (Headings)

```markdown
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题
```

---

## 2. 段落 & 换行

```markdown
这是一个段落。

这是另一个段落。（空一行分隔）

行尾加两个空格  
换行
```

---

## 3. 强调 (Emphasis)

```markdown
*斜体* 或 _斜体_  
**粗体** 或 __粗体__  
***粗斜体***  
~~删除线~~
```

---

## 4. 列表 (Lists)

### 无序列表

```markdown
- 项目1
- 项目2
  - 子项目2.1
  - 子项目2.2
* 也可以用星号
+ 也可以用加号
```

### 有序列表

```markdown
1. 第一项
2. 第二项
   3. 子项 2.1
   4. 子项 2.2
```

### 任务列表

```markdown
- [x] 已完成任务
- [ ] 未完成任务
```

---

## 5. 链接 & 图片

```markdown
[这是链接](https://example.com)  
![这是图片](https://via.placeholder.com/150)  
[带标题的链接](https://example.com "提示文字")  
```

---

## 6. 引用 (Blockquotes)

```markdown
> 这是引用
>> 这是嵌套引用
```

---

## 7. 代码 (Code)

### 行内代码

```markdown
这是 `行内代码`
```

### 代码块

```语言名  
代码内容  
```

````markdown
```python
print("Hello Markdown")
````

````

---

## 8. 分隔线
```markdown
---
***
___
````

---

## 9. 表格

```markdown
| 姓名 | 年龄 | 专业 |
|------|------|------|
| 张三 |  20  | 生物 |
| 李四 |  21  | 计算机 |
```

---

## 10. 脚注

```markdown
这是一个脚注示例[^1]。

[^1]: 这里是脚注内容。
```

---

## 11. 内嵌 HTML

```markdown
<p align="center">居中对齐的文字</p>
```

---

## 12. 高级扩展 (支持情况取决于渲染器)

### 数学公式 (LaTeX)

```markdown
行内公式：$E = mc^2$  
块级公式：
$$
\frac{a}{b} = c
$$
```

### 图表/流程图 (Mermaid)

````markdown
```mermaid
graph TD;
  A[开始] --> B{条件};
  B -->|是| C[执行1];
  B -->|否| D[执行2];
````

````

### 折叠内容 (在 GitHub 支持)
```markdown
<details>
  <summary>点击展开</summary>
  这里是隐藏的内容。
</details>
````


