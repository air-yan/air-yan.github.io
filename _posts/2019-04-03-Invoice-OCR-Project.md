---
published: false
layout: single
mathjax: true
toc: true
toc_sticky: true
category: Accounting Automation
tags:
excerpt: "This is a OCR project to extract specific information from invoices/receipts"
title: Invoice OCR project
share: true
author_profile: true
---

# Invoice OCR and Extract

I'm so excited to write this post! This post is an introduction of the OCR project I write on my own. It's a mixture of various areas of learning including accounting, coding, string extraction, computer vision and OCR.

## Main Object
The main object of the project is to create a back-end program which can recognise invoices sent from the vendors to the company and automatically extract important information that accounting department needs as the input of data entries.

The target accuracy is 80%.

The information this program extract includes:
- Total Amount
- Invoice number or Account number
- Bill date
- Due date if available
- Check Payment Address if available
- Vendor Name


This project is currently targeted to invoice recognition rather than receipt recognition. Although these might sound similar to each other, they are completely two different things! Invoices are normally kept by company as PDFs (received from emails) which can be very complex in structure but the strings inside the PDFs are easy to be recognised. On the other hand, receipts might be blur and kept inproperly, but simplely structured.

Therefore, when extracting information from PDFs, we are more focused on the structure analysis of the string extraction; when extracting information from receipts, string recognition is more of a important task so we focus on pre-processing of the images using computer vision.

If time allowed, I will add the receipt feature into the project in the future.

## A Little Detail

### Image Preprocessing - Computer Vision

### OCR engine - Tesseract

### PDF extractor - PDFminer

### String Extraction - Regex + Levenshtein



