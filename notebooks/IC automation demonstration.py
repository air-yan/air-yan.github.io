
# coding: utf-8

# ### Import Packages

# In[1]:


# preparation for notebook
import datetime
import pandas as pd


# ### Read and Clean Dataset

# In[2]:


# read source dataset and convert it into a pandas dataframe
source_df = pd.read_excel(io="Report.xlsx",sheet_name="Assignment")

# clean the dataset: if there is any row that the first column of it is null - we drop them
cleaned_df = source_df[source_df["Type"]          .isnull()          .apply(lambda x: True if x == False else False)]


# ### The Plan
# To transform each bill into IC we can have a core function. We build that first.
# 
# For a long list of bills, we have to do the transform in a neat way.
# - we build up dictionaries according to groups
# - divide the DataFrame into peaces according to the groups
# - run the core function at the lowest level
# - append them together than we have our result

# ### Preparations and References:

# In order to record the time of the IC transaction properly, we have to know the month and the year of the bill. We usually code last month's transaction one month later so we create below function:

# In[3]:


# prepare the function to show last month - will use it in the memo column in the core function below
def IC_month(today):
    if datetime.date.today().month == 1:
        month = 12
        year = today.year - 1
    else:
        month = today.month - 1
        year = today.year
    return datetime.date(year, month, today.day).strftime("%B %Y")

# test
testmonth = IC_month(datetime.date.today())
print('The last month is: {}'.format(testmonth))


# We need to build up a mapping reference so that in the core function below, we can transform our dataset into the desired format. You can see a sample of the first two lines of the mapping in below table.
# 1. Full Sub: structured name for the subsidiary (system accepted name)
# 2. Short Name: short name for subsidiaries. Use it in memo and file name
# 3. IC from: the account name for the "from line" of the IC
# 4. IC to: the account name for the "to line" of the IC

# In[4]:


# building up mapping reference
sub_mapping_ref = pd.DataFrame(data = {'Your Company, Inc.': ['Your Company, Inc.',  'US', '1501-01 Intercompany Receivable - Other : Intercompany Receivable - Other - from US', '2120-05 Intercompany Payable - Other : Intercompany Payable - Other - to US'], 'Your Company Public Sector, Inc.': ['Your Company, Inc. : Your Company Public Sector, Inc.',  'PS', '1501-11 Intercompany Receivable - Other : Intercompany Receivable - Other - from Public Sector', '2120-13 Intercompany Payable - Other : Intercompany Payable - Other - to Public Sector'], 'Your Company Singapore Pte. Ltd.': ['Your Company, Inc. : Your Company Singapore Pte. Ltd.',  'SG', '1501-06 Intercompany Receivable - Other : Intercompany Receivable - Other - from SG', '2120-09 Intercompany Payable - Other : Intercompany Payable - Other - to SG'], 'Your Company AU Pty Ltd.': ['Your Company, Inc. : Your Company HOLDING LIMITED : Your Company AU Pty Ltd.',  'AU', '1501-05 Intercompany Receivable - Other : Intercompany Receivable - Other - from AU', '2120-08 Intercompany Payable - Other : Intercompany Payable - Other - to AU'], 'Your Company Japan K.K.': ['Your Company, Inc. : Your Company Japan K.K.',  'JP', '1501-04 Intercompany Receivable - Other : Intercompany Receivable - Other - from JP', '2120-07 Intercompany Payable - Other : Intercompany Payable - Other - to JP'], 'Your Company Deutschland GmbH': ['Your Company, Inc. : Your Company Deutschland GmbH',  'DE', '1501-03 Intercompany Receivable - Other : Intercompany Receivable - Other - from DE', '2120-06 Intercompany Payable - Other : Intercompany Payable - Other - to DE'], 'Your Company Canada Ltd.': ['Your Company, Inc. : Your Company HOLDING LIMITED : Your Company Canada Ltd.',  'CA', '1501-08 Intercompany Receivable - Other : Intercompany Receivable - Other - from CA', '2120-10 Intercompany Payable - Other : Intercompany Payable - Other - to CA'], 'Your Company France': ['Your Company, Inc. : Your Company Deutschland GmbH : Your Company France',  'FR', '1501-10 Intercompany Receivable - Other : Intercompany Receivable - Other - from FR', '2120-12 Intercompany Payable - Other : Intercompany Payable - Other - to FR'], 'Your Company UK, Ltd.': ['Your Company, Inc. : Your Company HOLDING LIMITED : Your Company UK, Ltd.',  'UK', '1501-02 Intercompany Receivable - Other : Intercompany Receivable - Other - from UK', '2120-03 Intercompany Payable - Other : Intercompany Payable - Other - to UK'], 'Your Company Switzerland': ['Your Company, Inc. : Your Company Deutschland GmbH : Your Company Switzerland',  'SZ', '1501-16 Intercompany Receivable - Other : Intercompany Receivable - Other - from SZ', '2120-17 Intercompany Payable - Other : Intercompany Payable - Other - to SZ'], 'Your Company Benelux': ['Your Company, Inc. : Your Company Deutschland GmbH : Your Company Benelux',  'NL', '1501-14 Intercompany Receivable - Other : Intercompany Receivable - Other - from NL', '2120-15 Intercompany Payable - Other : Intercompany Payable - Other - to NL'], 'Your Company Sweden': ['Your Company, Inc. : Your Company Deutschland GmbH : Your Company Sweden',  'SW', '1501-12 Intercompany Receivable - Other : Intercompany Receivable - Other - from SW', '2120-14 Intercompany Payable - Other : Intercompany Payable - Other - to SW'], 'Your Company NZ Limited': ['Your Company, Inc. : Your Company HOLDING LIMITED : Your Company AU Pty Ltd. : Your Company NZ Limited',  'NZ', '1501-15 Intercompany Receivable - Other : Intercompany Receivable - Other - from NZ', '2120-16 Intercompany Payable - Other : Intercompany Payable - Other - to NZ'], 'Your Company South Africa': ['Your Company, Inc. : Your Company HOLDING LIMITED : Your Company UK, Ltd. : Your Company South Africa',  'SA', '1501-09 Intercompany Receivable - Other : Intercompany Receivable - Other - from SA', '2120-11 Intercompany Payable - Other : Intercompany Payable - Other - to SA']
})
sub_mapping_df = sub_mapping_ref.transpose()
sub_mapping_df.columns = ['Full Sub','Short Name', 'IC From', 'IC To']
sub_mapping_df.head(2)


# ### The Core Function

# The core function have four steps:
# 1. Before creating the function, we prepare the desired columns for it. That's because the 'append' method in pandas DataFrame seems ignore the sorting order of the columns. We use the csv_columns to correct it in the end.
# 2. Create four empty DataFrame as demonstrated in the scenario in the post.
# 3. We transform the dataset for each of the four lines
#     1. Expense lines for 'from subsidiary'.
#     2. Expense lines for 'to subsidiary'.
#     3. Receivable line for 'from subsidiary'.
#     4. Payable line for 'to subsidiary'.
# 4. We append these dataframe together

# In[5]:


# 1. Prepare the desired columns
csv_columns = ['Line Subsidiary','Account','Debit','Credit','Memo']

# THE! greatest function to translate transactions into IC format
def translate_IC(test_df):
    df_from = pd.DataFrame()
    df_to = pd.DataFrame()
    df_from_total = pd.DataFrame()
    df_to_total = pd.DataFrame()
    
    # 3.1 lines for from subsidiary
    df_from['Line Subsidiary'] = test_df['Subsidiary'].apply(lambda x: sub_mapping_df.loc[x,'Full Sub'])
    df_from['Account'] = test_df['Account (Line): Name (GL-style)']
    df_from['Debit'] = None
    df_from['Credit'] = test_df['Amount (Foreign Currency)']
    df_from['Memo'] = test_df['Memo']

    # 3.2 lines for to subsidiary
    df_to['Line Subsidiary'] = test_df['IC Subsidiary'].apply(lambda x: sub_mapping_df.loc[x,'Full Sub'])
    df_to['Account'] = test_df['Account (Line): Name (GL-style)']
    df_to['Debit'] = test_df['Amount (Foreign Currency)']
    df_to['Credit'] = None
    df_to['Memo'] = test_df['Memo']

    # 3.3 total line for from subsidiary
    df_from_total['Line Subsidiary'] = test_df['Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'Full Sub'])
    df_from_total['Account'] = test_df['IC Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'IC From'])
    df_from_total['Debit'] = round(df_from['Credit'].sum(),2)
    df_from_total['Credit'] = None
    df_from_total['Memo'] = 'Intercompany from {} to {} for {} in {}'    .format(test_df['Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'Short Name']).iloc[0]                                                  ,test_df['IC Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'Short Name']).iloc[0]                                                  ,test_df['Num'].iloc[0]                                                  ,IC_month(datetime.date.today()) )

    # 3.4 total line for to subsidiary
    df_to_total['Line Subsidiary'] = test_df['IC Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'Full Sub'])
    df_to_total['Account'] = test_df['Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'IC To'])
    df_to_total['Debit'] = None
    df_to_total['Credit'] = round(df_from['Credit'].sum(),2)
    df_to_total['Memo'] = 'Intercompany from {} to {} for {} in {}'    .format(test_df['Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'Short Name']).iloc[0]                                                  ,test_df['IC Subsidiary'].iloc[0:1].apply(lambda x: sub_mapping_df.loc[x,'Short Name']).iloc[0]                                                  ,test_df['Num'].iloc[0]                                                  ,IC_month(datetime.date.today()) )

    # 4. append everything and return the greatest IC dataframe ever!
    test = df_from_total.append(df_from).append(df_to_total).append(df_to)
    return test.loc[:,csv_columns]


# ### Building up dictionaries and run the core function
# Remember that the first requirement is to:
# 
# *Given a list of bills, classify them into different groups according to:*
# 1. *IC (intercompany) from subsidiary, the employee payroll sub -- it's DE in the above case*
# 2. *Bill reference number -- unique key for bills*
# 3. *IC to subsidiary -- it's US in the above case*
# 
# In order to achieve this, we have **THREE STEPS**:
# 1. Find all 'IC sub' in the DataFrame, divide the dataframe according to it, put the DataFrame into the dictionary. Now we are ready for a loop inside the dictionary
# 2. We:
#     1. Loop through the above dictionary and do exactly the same for 'Reference Number' (a dict inside a dict)
#     2. Loop through the above dictionary and do exactly the same for 'to sub' (a dict inside a dict inside a dict...)
# 3. Append them together in the right order and save them in a csv

# #### STEP 1:

# In[6]:


# We use value_counts().index to extract subsidiary info
from_subsidiary = cleaned_df["Subsidiary"].value_counts().index

# create a dictionary and 
from_sub_dic = {}
for sub in from_subsidiary:
    sub_df = cleaned_df[cleaned_df["Subsidiary"].apply(lambda x: True if x == sub else False)]
    from_sub_dic[sub] = sub_df

# TEST CODE:
# test the result of the above codes
print("We have subsidiaries:")
count = 1
for sub in from_sub_dic.keys():
    print(" "*5 + str(count) + ". "+ sub)
    count += 1
print("-"*50)
print("Below is a glance of the DataFrame of the first item in the dictionary: ")
print("-"*50)
test_key = list(from_sub_dic.keys())
from_sub_dic[test_key[0]].head(2)


# #### STEP 2:

# In[7]:


for from_sub_key in from_sub_dic:
    # this is the dataframe for each "from sub"
    from_sub_df = from_sub_dic[from_sub_key]

    # create report id dictionary
    report_id_dic = {}
    report_id = from_sub_df['Num'].value_counts().index
    
    # report id loop inside from sub loop
    for each_id in report_id:
        report_id_df = from_sub_df[from_sub_df["Num"]
                                   .apply(lambda x: True if x == each_id else False)]
        report_id_dic[each_id] = report_id_df
        
        # create another dic inside for "to sub" (same steps as divide sub)
        to_sub_dic = {}
        to_subsidiary = report_id_df["IC Subsidiary"].value_counts().index
        
        # to sub loop inside report id loop inside from sub loop
        for to_sub in to_subsidiary:
            to_sub_df = report_id_df[report_id_df["IC Subsidiary"]
                                     .apply(lambda x: True if x == to_sub else False)]
            lowest_level_df = translate_IC(to_sub_df)
            to_sub_dic[to_sub] = lowest_level_df

        # overwrite report id dataframe by to sub dictionary, so we have a dic inside a dic inside a dic
        report_id_dic[each_id] = to_sub_dic

    # overwrite from sub dataframe by report id dictionary, so we have a dic inside a dic
    from_sub_dic[from_sub_key] = report_id_dic


# ---------
# #### STEP 3: 
# We concate these DataFrames together and create csv files in the directory for each sub. 
# 
# At the same time, we generate a overview for the loops and the result.
# 
# Well done!

# In[8]:


for i in from_sub_dic:
    print('From sub: ' + i)
    # create df for each from sub
    sub_df = pd.DataFrame(columns = csv_columns)
    to_sub_str = ""
    to_sub_list = []
    
    for j in from_sub_dic[i]:
        print(' '*5 + j)
        
        for k in from_sub_dic[i][j]:
            if k not in to_sub_list:
                to_sub_list.append(k) 
                to_sub_str += " " + sub_mapping_df.loc[k,'Short Name']
            
            print(' '*10 + 'To Sub: ' + k)
            # append df
            append_this_one = from_sub_dic[i][j][k]
            sub_df = sub_df.append(append_this_one)
#             print('test'+i,j,k)

    # save csv for every sub
    
    sub_df.to_csv('Advanced Intercompany from ' + sub_mapping_df.loc[i,'Short Name'] +' to' + to_sub_str + '.csv' ,index = False)
    print('Advanced Intercompany from ' + sub_mapping_df.loc[i,'Short Name'] +' to' + to_sub_str + '.csv')
    print('-'*40)

