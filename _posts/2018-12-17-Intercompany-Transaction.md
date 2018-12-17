---
published: true
layout: single
mathjax: true
toc: true
toc_sticky: true
category: Accounting Automation
excerpt: "This post is to demonstrate how we can use Python to generate intercompany transaction journal entries automatically"
title: Accounting Automation - Intercompany Transactions
---

# Intro and Preparation

This post demonstrates how we can use Python and Pandas library to help us do intercompany transaction journal entries automatically. The scenario and the requirement in this post is easy to understand. In real life, it can be more complex and need extra lines of codes to be solved.

To use this code to automate your accounting process, you should have:
- Python3 installed
- Pandas library

To make it easier to test and use your code, you can have
- Jupyter notebook
- Sublime Text
- Pyinstaller (to give this code to your colleagues who have no programing experience)

# Scenario

*You can quickly scan through or skip this part if you are well knowledged in intercompany transaction.*

## Bill

We have expenses incurred in one subsidiary.

For example, Lisa, a marketing specialist of your company, is going to host a large marketing campaign in US for the development of US business. She spent some money on this campaign so you can record it in the expense system like this. 

|Sub|Account| Debit  | Credit | Explanation |
|----|-----| ------------- | ------------- |--------|
|DE|Campaign Expense| $10,000.00  |   | Bill |
|DE|Account Payable to Credit Card|   | $10,000.00  | Bill |

Memo: Lisa's campaign cost in U.S. (Lisa is a DE employee)

We assume the above has been fully automated and the below has yet to be automated.

## Intercompany Transaction Journal
However, because Lisa is not an employee from your US subsidiary but an employee from your German subsidiary, these expenses are actually paid by DE. For some reasons, she spent this money out of her pocket *or* from her German Corporate Credit Card. So this bill is recorded back to her own company - the German subsidiary.

Based on the above bill, the global accounting team needs to record an intercompany transaction journal, which includes four lines of entries, to transfer this expense from DE to US:

|Sub|Automation| Debit  | Credit | Explanation |
|----|-----| ------------- | ------------- |------------- |
|DE|Account Receivable from U.S.| $10,000.00  |   | Intercompany Transaction |
|DE|Campaign Expense|   | $10,000.00  | Intercompany Transaction |
|US|Account Payable to DE|   | $10,000.00  | Intercompany Transaction |
|US|Campaign Expense| $10,000.00  |   | Intercompany Transaction |

Memo: Lisa's campaign cost in U.S.

# Requirement

Click [here](https://github.com/air-yan/air-yan.github.io/blob/master/excels/Report.xlsx) and click 'download' or 'view raw' to find the Excel file. (rest assured that this file does not include any macro)

What we need to do is to transform the bill entries in the Excel file into IC transactions in csv format.

Specifically:
1. Given a long list of bill items, classify them into different groups according to:
   - IC (intercompany) from subsidiary, the employee payroll sub -- it's DE in the above case
   - Bill reference number -- unique key for bills
   - IC to subsidiary -- it's US in the above case
2. Create core function to transfer bills into IC transactions
3. Apply core function to each above group to create IC transactions
4. For each "IC from subsidiary", create a csv file

# Solution

To view the explanation and solution code in a Jupyter notebook, click [here](https://nbviewer.jupyter.org/github/air-yan/air-yan.github.io/blob/master/notebooks/IC%20automation%20demonstration.ipynb).

To view the code in a python file, click [here](https://github.com/air-yan/air-yan.github.io/blob/master/notebooks/IC%20automation%20demonstration.py).

To test the solution, put the python file or jupyter notebook and the Excel file in a same directory and run the codes. You will find several csv files generated in the same directory.

# Cheers!

There are some tasks not only takes your time but also make you brain dead. With some extra knowledge, we can kill those brainless jobs and make you time more valuable. Cheers! :)
