# AI Teaching Scaffold

## 一个轻量、免费的 AI 教学辅助平台

------

# 1. 项目简介

**AI Teaching Scaffold** 是一个面向教师和学生的轻量免费平台，目标不是教授复杂的 AI 技术，而是帮助用户 **把 AI 当作教学和学习工具来使用**。

目前很多教师虽然已经听说过 ChatGPT、Claude 等 AI 工具，但仍然存在几个问题：

- 不知道 AI 可以帮助完成哪些教学任务
- 不会编写有效的 Prompt
- 不确定如何在教学中安全使用 AI

因此，本项目希望解决的不是 **AI 技术门槛**，而是 **AI 在教学中的使用门槛**。

平台通过提供 **教学任务模板和自动生成 Prompt 的方式**，帮助教师快速利用 AI 提高教学效率。

------

# 2. 核心问题

当前教育环境中主要存在两个问题。

## 2.1 教师不会使用 AI 工具

很多教师：

- 不知道如何向 AI 提问
- 不知道如何让 AI 生成教学材料
- 不知道如何利用 AI 出题或批改作业

因此即使 AI 功能强大，也难以真正应用到教学中。

------

## 2.2 教学资源与时间有限

教师通常需要花费大量时间在：

- 设计题目
- 批改作业
- 编写教学材料
- 写学生反馈

AI 有机会成为一种 **低成本教学助手**，帮助教师减少重复性工作。

但前提是教师知道 **如何正确使用 AI**。

------

# 3. 项目定位

这个平台的核心是：

**AI for Teaching**

即：

**用 AI 辅助教学**

而不是：

**Teaching AI Technology**

平台帮助教师使用 AI 完成常见教学任务，例如：

- 生成练习题
- 创建小测验
- 批改学生答案
- 生成课堂讲解
- 编写学生反馈

AI 在这里被当作 **教学辅助工具**。

------

# 4. 产品理念：Scaffolding（脚手架式引导）

平台采用 **Scaffolding（脚手架）** 的设计理念。

用户不需要自己构思复杂 Prompt，而是通过简单选择任务，由平台自动生成适合的 AI Prompt。

基本流程如下：

教学任务选择

↓

填写简单参数

↓

平台生成 Prompt

↓

教师复制 Prompt 到 AI 工具

↓

AI 生成教学内容

↓

教师审核并使用

这种方式可以显著降低教师使用 AI 的门槛。

------

# 5. MVP（最小可行版本）

平台初版只保留最核心的 **5 个教学模块**。

------

# 5.1 生成练习题（Question Generator）

教师输入：

- 主题
- 年级
- 题目数量
- 题目类型

平台生成 Prompt，例如：

Example Prompt：

Create 5 multiple-choice questions about photosynthesis for grade 8 students.
 Each question should include four answer options and clearly indicate the correct answer.

教师可以将该 Prompt 复制到 AI 工具中生成题目。

------

# 5.2 创建小测验（Quiz Generator）

教师输入：

- 主题
- 年级
- 题目数量

平台生成 Prompt，例如：

Generate a 10-question algebra quiz for grade 9 students.
 Include answers and ensure the difficulty is appropriate for high school students.

------

# 5.3 批改学生答案（Answer Evaluation）

教师输入：

- 题目
- 学生答案

平台生成 Prompt，例如：

Evaluate the following student answer and provide constructive feedback.
 Identify whether the answer is correct and explain the reasoning.

------

# 5.4 生成课堂讲解（Lesson Explanation）

教师输入：

- 主题
- 年级

平台生成 Prompt，例如：

Explain the concept of photosynthesis for middle school students.
 Use simple language and provide clear examples.

------

# 5.5 学生反馈生成（Student Feedback）

教师输入：

- 学生表现
- 学习情况

平台生成 Prompt，例如：

Write encouraging feedback for a student who has improved in math but still struggles with fractions.

------

# 6. 设计原则

## 6.1 轻量化

平台尽量做到：

- 页面简单
- 加载速度快
- 技术结构简单

初期版本不直接运行 AI，而是 **生成 Prompt**，以降低开发成本。

------

## 6.2 免费开放

平台资源免费提供，降低教师使用 AI 的门槛。

------

## 6.3 易于理解

平台默认用户：

- 可能从未使用过 AI
- 不熟悉 Prompt 写作
- 技术基础较弱

因此界面和提示必须 **直观、简洁**。

------

# 7. 目标用户

平台主要面向：

**Primary Users**

- 中学教师
- 助教
- 教学助理
- 对 AI 不熟悉的教育工作者

**Secondary Users**

- 学生
- 自学者

但平台设计 **主要以教师需求为核心**。

------

# 8. 传播方式

项目的主要传播路径是 **学校传播（school outreach）**。

传播方式如下：

平台提供免费工具

↓

教师尝试使用

↓

教师推荐给学生

↓

学生接触并使用 AI 学习工具

这种方式可以通过教师影响整个课堂。

------

# 9. 本地适配

平台会考虑不同地区的实际条件，例如：

- 不同 AI 工具的可访问性
- 不同语言环境
- 不同网络条件

平台的设计目标是确保：

**即使在资源有限的环境中，也可以使用 AI 辅助教学。**

------

# 10. 长期愿景

项目的长期目标不是建立复杂的 AI 技术平台，而是构建一个：

**简单、可运行的 AI 教学脚手架平台**

未来可能扩展：

- 更多教学任务模板
- 教师社区共享 Prompt
- 本地化教育资源
- 开源教育合作

但初期重点始终是：

**先做一个能运行并被真实教师使用的平台。**

------

# 11. 核心使命

一句话总结这个项目：

**让即使完全不会使用 AI 的教师，也能轻松利用 AI 提高教学效率。**