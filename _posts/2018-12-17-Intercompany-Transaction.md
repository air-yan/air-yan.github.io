---
published: false
layout: single
mathjax: true
toc: true
toc_sticky: true
category: Accounting Automation
excerpt: "This post is to demonstrate how we can use Python to generate intercompany transaction journal entries automatically"
title: Accounting Automation - Intercompany Transactions
---

# Python Automation for Intercompany Transactions

## Intro and Preparation

This post demonstrates how we can use Python and Pandas library to help us do intercompany transaction journal entries automatically. The scenario and the requirement in this post is easy to understand. In real life, it can be more complex and harder to be solved.

To use this code to automate your accounting process, you should have:
- Python3 installed
- Pandas library

To make it easier to test and use your code, you can have
- Jupyter notebook
- Sublime Text
- Pyinstaller (to give this code to your colleagues who have no programing experience)

## Accounting Requirement (scenario)

*You can quickly scan through or skip this part if you are well knowledged in intercompany transaction.*

### Bill

We have expenses incurred in one subsidiary.

For example, we have a marketing specialist Lisa who is going to host a large marketing campaign in US for the development of US business. She spent some money on this campaign so we should record it in the expense system like this. 

|Sub|Account| Debit  | Credit | Explanation |
|----|-----| ------------- | ------------- |--------|
|DE|Campaign Expense| $10,000.00  |   | Bill |
|DE|Account Payable to Credit Card|   | $10,000.00  | Bill |

Memo: Lisa's campaign cost in U.S.
(We assume the above part of job has been fully automated but the below part has yet to be automated.)

### Intercompany Transaction Journal
However, these expenses are actually paid by another subsidiary, because Lisa is not an employee from our US subsidiary but an employee from German subsidiary. She come here to help. For some reasons, she spent this money out-of-pocket **or** from her German Corporate Credit Card. So this expense and money is recorded back to her own company - the German subsidiary.

Based on the above journal entry, the global accounting team needs to record an intercompany transaction journal which includes four lines of entries to transfer this expense from DE to US:

|Sub|Automation| Debit  | Credit | Explanation |
|----|-----| ------------- | ------------- |------------- |
|DE|Account Receivable from U.S.| $10,000.00  |   | Intercompany Transaction |
|DE|Campaign Expense|   | $10,000.00  | Intercompany Transaction |
|US|Account Payable to DE|   | $10,000.00  | Intercompany Transaction |
|US|Campaign Expense| $10,000.00  |   | Intercompany Transaction |

Memo: Lisa's campaign cost in U.S.

Together, we have:

|Sub|Automation| Debit  | Credit | Explanation |
|----|-----| ------------- | ------------- |------------- |
|DE|~~Campaign Expense~~| ~~$10,000.00~~  |   | Bill Entry |
|DE|Account Payable to Credit Card|   | $10,000.00  | Bill Entry |
|DE|Account Receivable from U.S.| $10,000.00  |   | Intercompany Transaction |
|DE|~~Campaign Expense~~|   | ~~$10,000.00~~  | Intercompany Transaction |
|US|Account Payable to DE|   | $10,000.00  | Intercompany Transaction |
|US|Campaign Expense| $10,000.00  |   | Intercompany Transaction |

The automation of generating the last four lines of entries is the main target of this project.
