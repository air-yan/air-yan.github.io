---
layout: archive
author_profile: true
title: Projects and Analysis
share: false
permalink: /projects_and_analyses/
---

<ul class="taxonomy__index">
    <li>
      <a href="#Automation">
        <strong>Automation Projects</strong> <span class="taxonomy__count">2</span>
      </a>
    </li>
</ul>

<ul class="taxonomy__index">
    <li>
      <a href="#DataAnalysis">
        <strong>Data Analysis</strong> <span class="taxonomy__count">1</span>
      </a>
    </li>
</ul>

<section id="Automation" class="taxonomy__section">
	<h2 class="archive__subtitle">Automation Projects</h2>
	<div class="entries-{{ page.entries_layout | default: 'list' }}">
	    <h2 class="archive__item-title" itemprop="headline">
	        <a href="https://air-yan.github.io/accounting%20automation/Invoice-OCR-Project/" rel="permalink">Invoice OCR Project</a>
	    </h2>
	    <p class="archive__item-excerpt" itemprop="description">{{ "This post is a demo of one of my programs. It explains how to extract information from invoices or receipts" | markdownify | strip_html | truncate: 160 }}</p>
        <h2 class="archive__item-title" itemprop="headline">
	        <a href="https://air-yan.github.io/accounting%20automation/Intercompany-Transaction/" rel="permalink">Pandas Project - Intercompany Transactions</a>
	    </h2>
	    <p class="archive__item-excerpt" itemprop="description">{{ "This post is a demo of one of my programs. It explains how to use Pandas to automate accounting tasks" | markdownify | strip_html | truncate: 160 }}</p>
	</div>
	<a href="#page-title" class="back-to-top">{{ site.data.ui-text[site.locale].back_to_top | default: 'Back to Top' }} &uarr;</a>
</section>

<section id="DataAnalysis" class="taxonomy__section">
	<h2 class="archive__subtitle">Data Analysis</h2>
	<div class="entries-{{ page.entries_layout | default: 'list' }}">
	    <h2 class="archive__item-title" itemprop="headline">
	        <a href="https://air-yan.github.io/data%20analysis/Titanic-Survival-Analysis/" rel="permalink">Titanic EDA and Modeling</a>
	    </h2>
	    <p class="archive__item-excerpt" itemprop="description">{{ "This is a practice for data science analysis. It include many processes like data cleaning, EDA, feature enginearing, and modeling." | markdownify | strip_html | truncate: 160 }}</p>
	</div>
	<a href="#page-title" class="back-to-top">{{ site.data.ui-text[site.locale].back_to_top | default: 'Back to Top' }} &uarr;</a>
</section>
