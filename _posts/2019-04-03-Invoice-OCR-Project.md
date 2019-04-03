---
published: true
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

I'm so excited to write this post! This post is an introduction of the OCR project I write on my own. It's a mixture of various areas of learning including accounting, coding, string extraction, computer vision and OCR.

The github project is currently in private status, but it will be open to public once the accuracy achieves the desired level.

## Main Object
The main object of the project is to create a back-end program which can recognise invoices sent from the vendors to your company and automatically extract important information that accounting department needs as the input of data entries.

The target accuracy is 80%. Remember that this is an automation project, not a personal practice (well actually it is ;P), so an accuracy less than 80% means that you probably will bring more troubles to the team than conveniences.

The information this program extract includes:
- Total Amount
- Invoice number or Account number
- Bill date
- Due date if available
- Check Payment Address if available
- Vendor Name


This project is currently targeted to invoice recognition, but not receipt recognition. Although these might sound similar to each other, they are completely two different things! 

Invoices are normally kept by company as PDFs (received from emails) which can be very complex in structure but the strings inside the PDFs are easy to be recognised. On the other hand, receipts might be blur and kept inproperly and mostly likely they are probably sent to the accounting department as screenshots, so it's not that easy to do the OCR task but the good thing is that the characters are structured in an easyly understandable way - lines.

Therefore, when extracting information from PDFs, we are more focused on the structure analysis of the OCR; when extracting information from receipts, character recognition itself is an important task so we focus more on the pre-processing of the images using computer vision to improve accuracy.

If time allowed, I will add the receipt feature into the project in the future.

## Little Details
The plan of the process can be described as below:

### Classification and Extraction
Assume that we have an input of image from whatever sources (it can be uploaded from mobile phones, web sites or just put into the program using command lines), firstly, we need to know the format of the input because we need to classify them so we can know whether or not we need to do the OCR task.

If the format is PDF (well most of the cases I'm facing is PDF), we check the nature of the PDF - is it an image or a complex form built up from images, formats and strings. If it's latter, we use PDFminer (a python module) to extract the strings directly. Otherwise, we use computer vision to do the image preprocessing and then use Tesseract, the OCR engine, to extract the strings.

It's quite interesting to try and see the impact of different conditions of the images. Computer vision is a powerful tool.

### String Matching
<span style = "color: grey">*Don't read this paragraph, please. String matching is the most demotivating part in this project! I hate it! I have to try different Regexs and change it everytime when I finish a test... it's time-consuming and stupid... God, please send me a free engineer to help me out... Enough for complaining.*</span>

I assume everyone read this knows what Regex is and knows at least a little bit of how it works. If you don't, just know that it's a fuzzy matcher that can extract strings by different expressions.

The reason why I use regex here is that the strings extracted from an invoice can be badly structured. We can't control that nature because every invoice is different. Therefore, regex is what we need to extract strings from a pile of unstructured strings. <span style = "color: grey">*What a nightmare...*</span> I believe if we were dealing with receipts, there are better options available.

We can build different regex for different features and requirements.

### Output Scoring
Think that is the end of the program? No. What we get from the string matching process is not good enough. I did not try it out but I guess the accuracy of the above process can be lower than 60%.

A scoring process which scores the output of the above process can improve the accuracy dramatically. Think the biggest problem we faced in previous section - it's the structure of the strings. What if we analyse the invoices multiple times using different engines and different parameters? We can have many different results. By scoring those results and getting the best result out of them, we improve the accuracy of the program.

## End of story

Thank you for your time reading this. If you are interested and have any questions, please contact me anytime.

Cheers! =)






