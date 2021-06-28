import pandas as pd
import numpy as np
import re
import time
from flask import Flask, request, render_template,make_response

Industry_mapping = {
    'not available' : 'not available',
    'dairy': 'Agriculture',
    'farming': 'Agriculture',
    'fishery': 'Agriculture',
    'ranching': 'Agriculture',
    'agriculture': 'Agriculture',

    'arts and crafts': 'Arts',
    'fine art': 'Arts',
    'performing arts': 'Arts',
    'photography': 'Arts',

    'building materials': 'Construction',
    'civil engineering': 'Construction',
    'construction': 'Construction',


    'apparel & fashion': 'Consumer Goods',
    'consumer electronics': 'Consumer Goods',
    'consumer goods': 'Consumer Goods',
    'consumer services': 'Consumer Goods',
    'cosmetics': 'Consumer Goods',
    'food & beverages': 'Consumer Goods',
    'furniture': 'Consumer Goods',
    'luxury goods & jewelry': 'Consumer Goods',
    'sporting goods': 'Consumer Goods',
    'tobacco': 'Consumer Goods',
    'wine and spirits': 'Consumer Goods',


    'accounting': 'Corporate Services',    
    'business supplies and equipment': 'Corporate Services',
    'environmental services': 'Corporate Services',
    'events services': 'Corporate Services',
    'executive office': 'Corporate Services',
    'human resources': 'Corporate Services',
    'information services': 'Corporate Services',
    'management consulting': 'Corporate Services',
    'outsourcing/offshoring': 'Corporate Services',
    'professional training & coaching': 'Corporate Services',
    'security and investigations': 'Corporate Services',
    'staffing and recruiting': 'Corporate Services',
    'facilities services': 'Corporate Services',

    'architecture & planning': 'Design',
    'design': 'Design',
    'graphic design': 'Design',


    'elearning': 'Education',
    'e-learning': 'Education',
    'education management': 'Education',
    'higher education': 'Education',
    'primary/secondary education': 'Education',
    'research': 'Education',



    'mining & metals': 'Energy & Mining',
    'oil & energy': 'Energy & Mining',
    'utilities': 'Energy & Mining',


    'animation': 'Entertainment',
    'broadcast media': 'Entertainment',
    'computer games': 'Entertainment',
    'entertainment': 'Entertainment',
    'media production': 'Entertainment',
    'motion pictures and film': 'Entertainment',
    'music': 'Entertainment',



    'banking': 'Finance',    
    'capital markets':  'Finance', 
    'financial services':  'Finance', 
    'insurance':  'Finance', 
    'investment banking':  'Finance', 
    'venture capital & private equity':  'Finance',
    'investment management':  'Finance', 


    'computer hardware':  'Hardware & Networking', 
    'computer networking': 'Hardware & Networking', 
    'nanotechnology': 'Hardware & Networking', 
    'semiconductors': 'Hardware & Networking', 
    'telecommunications': 'Hardware & Networking', 
    'wireless':  'Hardware & Networking', 


    'biotechnology': 'Health Care',
    'hospital & health care': 'Health Care',
    'medical devices': 'Health Care',
    'medical practice': 'Health Care',
    'mental health care': 'Health Care',
    'pharmaceuticals': 'Health Care',
    'veterinary': 'Health Care',


    'alternative dispute resolution': 'Legal',
    'law practice': 'Legal',
    'legal services': 'Legal',


    'automotive': 'Manufacturing',    
    'aviation & aerospace':  'Manufacturing',
    'chemicals':  'Manufacturing', 
    'defense & space': 'Manufacturing',
    'electrical/electronic manufacturing':  'Manufacturing',
    'glass, ceramics & concrete': 'Manufacturing',
    'industrial automation': 'Manufacturing',
    'machinery':  'Manufacturing',
    'mechanical or industrial engineering': 'Manufacturing', 
    'packaging and containers': 'Manufacturing',
    'paper & forest products': 'Manufacturing',
    'plastics': 'Manufacturing',
    'railroad manufacture':  'Manufacturing',
    'renewables & environment': 'Manufacturing',
    'shipbuilding': 'Manufacturing',
    'textiles': 'Manufacturing',
    'wood timber': 'Manufacturing',
    'food production': 'Manufacturing',


    'market research': 'Media & Communications',    
    'marketing and advertising':  'Media & Communications',
    'newspapers': 'Media & Communications', 
    'online media': 'Media & Communications',
    'printing':  'Media & Communications',
    'public relations and communications': 'Media & Communications',
    'translation and localization':'Media & Communications',
    'writing and editing':  'Media & Communications',
    'multimedia': 'Media & Communications',
    'publishing': 'Media & Communications',
    'translation and localization': 'Media & Communications',
    'writing and editing': 'Media & Communications',
    'multimedia': 'Media & Communications',


    'civic & social organization':  'Non Profit',
    'fund raising': 'Non Profit',
    'fund-raising': 'Non Profit',
    'individual & family services':'Non Profit',
    'international trade and development': 'Non Profit',
    'libraries': 'Non Profit',
    'museums and institutions':  'Non Profit',
    'nonprofit organization management': 'Non Profit',
    'philanthropy':'Non Profit',
    'program development': 'Non Profit',
    'religious institutions': 'Non Profit',
    'think tanks': 'Non Profit',


    'government administration':  'Public Administration',
    'government relations': 'Public Administration',
    'international affairs':'Public Administration',
    'judiciary': 'Public Administration',
    'legislative office': 'Public Administration',
    'political organization':  'Public Administration',
    'public policy': 'Public Administration',


    'law enforcement':'Public Safety',
    'military': 'Public Safety',
    'public safety': 'Public Safety',

    'commercial real estate':  'Real Estate',
    'real estate': 'Real Estate',


    'airlines/aviation':'Recreation & Travel',
    'gambling & casinos':'Recreation & Travel',
    'hospitality': 'Recreation & Travel',
    'leisure, travel & tourism':  'Recreation & Travel',
    'recreational facilities and services': 'Recreation & Travel',
    'restaurants': 'Recreation & Travel',
    'sports': 'Recreation & Travel',
    'religious institutions': 'Non Profit',


    'retail': 'Retail',
    'supermarkets': 'Retail',
    'wholesale': 'Retail',

    'computer & network security': 'Software & IT Services',
    'computer software': 'Software & IT Services',
    'information technology and services': 'Software & IT Services',
    'internet': 'Software & IT Services',


    'import and export': 'Transportation & Logistics',
    'logistics and supply chain': 'Transportation & Logistics',
    'maritime': 'Transportation & Logistics',
    'package/freight delivery': 'Transportation & Logistics',
    'transportation/trucking/railroad': 'Transportation & Logistics',
    'warehousing': 'Transportation & Logistics',

    'alternative medicine': 'wellness & fitness',
    'health, wellness and fitness': 'wellness & fitness',

}

# Emails Generic List
generic_list=['gmail.com',
              'yahoo.com',
              'hotmail.com',
              'aol.com',
              'hotmail.co.uk',
              'hotmail.fr',
              'msn.com',
              'yahoo.fr',
              'wanadoo.fr',
              'orange.fr',
              'comcast.net',
              'yahoo.co.uk',
              'yahoo.com.br',
              'yahoo.co.in',
              'live.com',
              'rediffmail.com',
              'free.fr',
              'gmx.de',
              'web.de',
              'yandex.ru',
              'ymail.com',
              'libero.it',
              'outlook.com',
              'uol.com.br',
              'bol.com.br',
              'mail.ru',
              'cox.net',
              'hotmail.it',
              'sbcglobal.net',
              'sfr.fr',
              'live.fr',
              'verizon.net',
              'live.co.uk',
              'googlemail.com',
              'yahoo.es',
              'ig.com.br',
              'live.nl',
              'bigpond.com',
              'terra.com.br',
              'yahoo.it',
              'neuf.fr',
              'yahoo.de',
              'alice.it',
              'rocketmail.com',
              'att.net',
              'laposte.net',
              'facebook.com',
              'bellsouth.net',
              'yahoo.in',
              'hotmail.es',
              'charter.net',
              'yahoo.ca',
              'yahoo.com.au',
              'rambler.ru',
              'hotmail.de',
              'tiscali.it',
              'shaw.ca',
              'yahoo.co.jp',
              'sky.com',
              'earthlink.net',
              'optonline.net',
              'freenet.de',
              't-online.de',
              'aliceadsl.fr',
              'virgilio.it',
              'home.nl',
              'qq.com',
              'telenet.be',
              'me.com',
              'yahoo.com.ar',
              'tiscali.co.uk',
              'yahoo.com.mx',
              'voila.fr',
              'gmx.net',
              'mail.com',
              'planet.nl',
              'tin.it',
              'live.it',
              'ntlworld.com',
              'arcor.de',
              'yahoo.co.id',
              'frontiernet.net',
              'hetnet.nl',
              'live.com.au',
              'yahoo.com.sg',
              'zonnet.nl',
              'club-internet.fr',
              'juno.com',
              'optusnet.com.au',
              'blueyonder.co.uk',
              'bluewin.ch',
              'skynet.be',
              'sympatico.ca',
              'windstream.net',
              'mac.com',
              'centurytel.net',
              'chello.nl',
              'live.ca',
              'aim.com',
              'bigpond.net.au'
                ]

generic_list2=['admin',
                'support',
                'billing',
                'hello',
                'careers',
                'domains',
                'partners',
                'press',
                'Info',
                'help',
                'noreply',
                'affiliates',
                'media',
                'hi',
                'hey',
                'Howdy',
                'Yourfriends',
                'donotreply',
                'sales',
                'marketing',
                'mail',
                'emailus',
                'Office',
                'Accounts',
                'Account',
                'IT',
                'HR',
                'Email',
                'email']
    #All Functions Created 
def Employee_cat(n):
    if n.isnumeric()==False:
        if n == '01-Oct'or n == '01-oct':
            return str("'1-10")
        if n == 'nov-50'or n == 'Nov-50':
            return str("'11-50")
        elif n == '1001-5000':
            return n
        elif n == 'Null':
            return None
        else:
            return n

# creating function to catergorize revenues
def Revenue_cat(n):
    if n <= 1000000:
        return ('$0M-$1M')
    elif n =='-9999':
        return('$0M-$1M')
    elif 1000001 <= n <= 10000000:
        return('$1M-$10M')
    elif 10000001 <= n <= 50000000:
        return('$10M-$50M')
    elif 50000001 <= n <= 100000000:
        return('$50M-$100M')
    elif 100000001 <= n <= 250000000:
        return('$100M-$250M')
    elif 250000001 <= n <= 500000000:
        return('$250M-$500M')
    elif 500000001 <= n <= 1000000000:
        return('$250M-$1B')
    elif 1000000001 <= n <= 100000000000:
        return('$1B-$10B')
    elif n > 100000000001 :
        return('$10B+')


# creating function to categorize Employees column

def resizing_employees(n):

    if n == 0:
        return '9999999999999999'
    elif n == '-9999':
        return '9999999999999999'
    elif n <= 10 or n=='1-10':
        return ' 1-10'
    elif 10 < n <= 50 or n=='11-50':
        return ' 11-50'
    elif 50 < n <= 200 or n=='51-200':
        return '51-200'
    elif 200 < n <= 500 or n=='201-500':
        return '201-500'
    elif 500 < n <= 1000 or n=='501-1000':
        return '501-1000'
    elif 1000 < n <= 5000 or n=='1001-5000':
        return '1001-5000'
    elif 5000 < n <= 10000 or n=='5001-10000':
        return '5001-10000'
    elif n > 10000:
        return '10000+'
    elif n == '01-Oct' or n == '01-oct':
        return ' 01-10'
    elif n == 'Nov-50' or n == 'nov-50':
        return ' 10-50'
    elif n == '51-200':
        return '51-200'
    elif n == '201-500':
        return '201-500'
    elif n == '501-1000':
        return '501-1000'
    elif n == '1001-5000':
        return '1001-5000'
    elif n == '5001-10000':
        return '5001-10000'



def employe(text):
    if text.isnumeric() == True:
        return text
    if text.isnumeric() == False:
        return 0




app = Flask(__name__)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        df = pd.read_csv(request.files.get('file'),encoding='ISO-8859-1',)
        df = pd.DataFrame(df)
        df=df.replace('\ï','i',regex=True)
        df=df.replace('\¿','',regex=True)
        df=df.replace('\â','',regex=True)
        df=df.replace('\?','',regex=True)
        df = df.replace('\+','',regex=True)
        df=df.replace('\x80\x99s','',regex=True)
        try:
            cols = df.select_dtypes(['object']).columns
            df[cols] = df[cols].apply(lambda x: x.str.strip())
        except:
            pass

        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\.','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\-','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\'','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\.','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\(','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\)','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\[','',regex=True)
        df[['First Name','Last Name']]=df[['First Name','Last Name']].replace('\]','',regex=True)

        df_first=df.loc[df['First Name'].isnull()==True] #to error list
        df_first_index=df_first.index
        df=df.drop(index=df_first_index, axis='rows')

        df_first['remarks']='First Name Missing'

        df_alpha=df.loc[df['First Name'].str.isalpha()==False]# to error list
        df_alpha_index=df.loc[df['First Name'].str.isalpha()==False].index
        df_alpha['remarks']='First name contains value other than alphabets'
        df=df.drop(index=df_alpha_index, axis='rows')


        df_last=df.loc[df['Last Name'].str.isalpha()==False]# to error list
        df_last_index=df.loc[df['Last Name'].str.isalpha()==False].index
        df_last['remarks']='Last name contains value other than alphabets'
        df=df.drop(index=df_last_index, axis='rows')
        

                # Merging city, State , Country
        df['Company City']=df['Company City'].fillna(df['City'])
        df['Company State']=df['Company State'].fillna(df['State'])
        df['Company Country']=df['Company Country'].fillna(df['Country'])
        df['Company Phone']=df['Company Phone'].fillna(df['Phone'])
        df=df.drop(['City','State','Country','Phone'],axis='columns')


        # Filling values in Column that can have null values
        df[['Last Name', 'Employees','Annual Revenue','Industry','Company Address','Company City','Company State','Company Phone','Company Country','Person Linkedin Url','Company Linkedin Url','Facebook Url', 'Twitter Url','Company Phone','Keywords','SEO Description', 'Technologies']]=df[['Last Name', 'Employees','Annual Revenue','Industry','Company Address','Company City','Company State','Company Phone','Company Country','Person Linkedin Url','Company Linkedin Url','Facebook Url', 'Twitter Url','Company Phone','Keywords','SEO Description', 'Technologies']].fillna('-9999')
                
        first_single = df.loc[(df['First Name'].str.contains(pat='^[a-zA-z]$',regex=True))]
        Last_toosingle = first_single.loc[(first_single['Last Name'].str.contains(pat='^[a-zA-z]$',regex=True))]
        Last_toosingle['remarks']= 'Single letter in First and Last Name'
        Last_toosingle_index= first_single.loc[(first_single['Last Name'].str.contains(pat='^[0-9a-zA-z]$',regex=True))].index

        last_space = first_single.loc[(first_single['Last Name'].str.contains(pat='^$',regex=True))]
        last_space_index=first_single.loc[(first_single['Last Name'].str.contains(pat='^$',regex=True))].index
        last_space2=first_single.loc[first_single['Last Name'].str.contains(pat=' ',regex=True)]
        last_space2_index=first_single.loc[first_single['Last Name'].str.contains(pat=' ',regex=True)].index
        df=df.drop(index=last_space_index,axis='rows')
        df=df.drop(index=last_space2_index,axis='rows')
        df.drop(index=Last_toosingle_index,axis='rows')
        last_space['remarks']= 'Single letter in First Name and blank Last Name'
        last_space2['remarks']= 'Single letter in First Name and blank Last Name'

        df.loc[(df['Keywords'].str.contains(pat='^[a-zA-z0-9]$',regex=True)),'Keywords']=''
        df.loc[(df['SEO Description'].str.contains(pat='^[a-zA-z0-9]$',regex=True)),'SEO Description']=''
        df.loc[df['Technologies'].str.contains(pat = '^[a-zA-z0-9]$', regex = True),'Technologies']= ''

        Null_value_list=df[df.isna().any(axis=1)]
        Null_value_list['remarks'] = 'No value present in Either column'
        try:
            Null_value_index =df[df.isna().any(axis=1)].index
            df=df.drop(index=Null_value_index,axis='rows')
        except:
            pass


        # Listing Emails and finding match
        df[['n_Email','domain']] = df['Email'].str.split('@',expand=True)
        Email_List=df.loc[df['domain'].isin(generic_list)]
        mail_index1=df.loc[df['domain'].isin(generic_list)].index
        df=df.drop(labels=None, axis=0, index=mail_index1,)

        df['n_Email']=df['n_Email'].str.replace(' ','')
        df['n_Email']=df['n_Email'].str.replace('-','')
        df['n_Email']=df['n_Email'].str.replace('+','')
        df['n_Email']=df['n_Email'].str.replace("'",'')
        df['n_Email']=df['n_Email'].str.replace(".",'')
        df['n_Email']=df['n_Email'].str.replace("_",'')

        Email_List_num=df.loc[df['n_Email'].str.isalpha()==False]
        mail_index2=df.loc[df['n_Email'].str.isalpha()==False].index
        df=df.drop(axis=0, index=mail_index2)

        email_list2=df.loc[df['n_Email'].isin(generic_list2)]
        email_list2_index=df.loc[df['n_Email'].isin(generic_list2)].index
        df=df.drop(axis=0, index=email_list2_index)

        Email_List_num['remarks']='Email error(number prior to @)'
        Email_List['remarks']='Email match in generic List'
        email_list2['remarks']='Email match in generic List'

        Email_List=Email_List.append(Email_List_num)
        df.drop(columns=['n_Email','domain'], inplace=True,axis='columns')
        Email_List.drop(columns=['n_Email','domain'], inplace=True,axis='columns')# to be appended in error list

        df=df.astype(str)
        df['remarks']=df.applymap(lambda x: x.isascii()).all(axis='columns')

        def value_change(text):
            if text == False:
                return ('Language issue in either column')

        Error_list=df.loc[df['remarks']==False]
        # Adding remarks in error list
        Error_list['remarks'] = Error_list['remarks'].apply(lambda x :value_change(x))
        #Finding index of columns having language related issues
        index_names = df[(df['remarks'] == False)].index
        df= df.drop(index=index_names,axis='rows')
        df=df.drop(['remarks'],axis='columns')


        retiredlist=df.loc[df['Title'].str.contains(pat = '^retire', regex = True)]
        retiredlist=retiredlist.append(df.loc[df['Title'].str.contains(pat = 'retiree', regex = True)])
        retiredlist=retiredlist.append(df.loc[df['Title'].str.contains(pat = 'no/slonger', regex = True)])
        retired_list=['retired']
        retiredlist=retiredlist.append(df.loc[df['Title'].isin(retired_list)])
        retired_index=retiredlist.index
        df=df.drop(labels=None, axis=0, index=retired_index, columns=None, level=None, inplace=False, errors='raise')
        retiredlist['remarks']='Retired or no longer working'
        Error_list=Error_list.append(retiredlist)
        Error_list=Error_list.append(df_first)
        Error_list=Error_list.append(df_alpha)
        Error_list=Error_list.append(df_last)
        Error_list=Error_list.append(Last_toosingle)
        Error_list=Error_list.append(last_space)
        Error_list=Error_list.append(last_space2)
        Error_list=Error_list.append(email_list2)
        try:
            Error_list=Error_list.drop(['City','State','Country','Phone'],axis=1)
        except:
            pass


        #converting annual revenue to numeric column
        df_rev=df.loc[df['Annual Revenue'].str.contains(pat = '[0-9]E+', regex = True)]
        try:
            df_rev[['Annual Revenue','new']]=df_rev['Annual Revenue'].str.split('E\+',expand=True)
            df_rev[['Annual Revenue','new']]=df_rev[['Annual Revenue','new']].astype('float')
            df_rev['new']=10**df_rev['new']
            df_rev['Annual Revenue']=df_rev['new']*df_rev['Annual Revenue']
            df_rev=df_rev.drop('new',axis=1)
            rev_index=df.loc[df['Annual Revenue'].str.contains(pat = '[0-9]E+', regex = True)].index
            df=df.drop(labels=None, axis=0, index=rev_index, columns=None, level=None, inplace=False, errors='raise')
        except:
            pass


        df['Annual Revenue'] = pd.to_numeric(df['Annual Revenue'],errors='coerce')
        #Applying function
        df['Annual Revenue_n'] = df['Annual Revenue'].apply(lambda x :Revenue_cat(x))
        #dropping Annual Revenue Function
        df.drop('Annual Revenue', axis='columns', inplace= True)
        df['Annual Revenue_n'].fillna('$0M-$1M')
        

        #converting annual revenue to numeric column
        df_rev=df.loc[df['Employees'].str.contains(pat = '[0-9]E+', regex = True)]
        try:
            df_rev[['Employees','new']]=df_rev['Employees'].str.split('E\+',expand=True)
            df_rev[['Employees','new']]=df_rev[['Employees','new']].astype('float')
            df_rev['Employees']=10**df_rev['E.mployees']
            df_rev['Employees']=df_rev['new']*df_rev['Employees']
            df_rev=df_rev.drop('new',axis=1)
            rev_index=df.loc[df['Employees'].str.contains(pat = '[0-9]E+', regex = True)].index
            df=df.drop(labels=None, axis=0, index=rev_index, columns=None, level=None, inplace=False, errors='raise')
        except:
            pass


        df['Employees'] = pd.to_numeric(df['Employees'],errors='coerce')
        #Applying function
        df['Employees Size'] = df['Employees'].apply(lambda x :resizing_employees(x))
        # dropping Annual Revenue Function
        df.drop('Employees', axis='columns', inplace= True)
        try:
            df['Employees Size']=df['Employees Size'].replace('9999999999999999','',regex=True)
        except:
            pass

        df['Industry'].str.lower()
        df['Industry_M'] = df['Industry'].map(Industry_mapping)

        # deleting ''http://www.' from websites column
        df['Website']=df['Website'].str.replace('http://www.','')

        df['Title']=df['Title'].replace('\?','',regex=True)
        df['Title']=df['Title'].replace('\'','',regex=True)
        df['Title']=df['Title'].replace('\.','',regex=True)
        df['Title']=df['Title'].replace('\+',' ',regex=True)
        df['Title']=df['Title'].replace('\-','',regex=True)
        df['Title']=df['Title'].replace('\=','',regex=True)


        df['Title']=df['Title'].str.lower()
        df.loc[df['Title'].str.isnumeric()==True,'Title']=''
        # df['Seniority Level']='Entry'
        # df['Department']='Others'
        df_T_non_alpha=df.loc[df['Title'].str.isalnum()==False]
        df_T_non_alpha['remarks']='Title not clear'

        title_single=df.loc[(df['Title'].str.contains(pat='^[a-zA-z0-9]$',regex=True))]
        title_single['remarks']='Single alphabet of num in Title'
        title_num=df.loc[df['Title'].str.isnumeric()]
        title_single['remarks']='Title have number'
        title_single_index=df.loc[(df['Title'].str.contains(pat='^[a-zA-z]$',regex=True))].index
        title_num_index=df.loc[df['Title'].str.isnumeric()].index


        Last_toosingle=Last_toosingle.append(last_space)
        Last_toosingle=Last_toosingle.append(title_single)
        Last_toosingle=Last_toosingle.append(title_num)
        try:
            df=df.drop(index=title_num_index,axis='rows')
            df=df.drop(index=title_single_index,axis='rows')
        except:
            pass


        department_others_list=['owner','president','manager','partner','head','ceo','vp','evp','director','founder','office manager',
                                'president & ceo','plant manager','vice president','agent','co-founder']
        df.loc[df['Title'].isin(department_others_list),'Department']='Others'
        sn_list=['owner','president'] 
        df.loc[df['Title'].isin(sn_list),'Department']='Others'

        df.loc[df['Title'].str.contains(pat = 'executive', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'finance', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'nurse', regex = True),'Seniority Level']= 'Entry'

        df.loc[df['Title'].str.contains(pat = 'information\ssystem', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'consultant', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'associate', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'rector', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'research', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'realtor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'teacher', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'editor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'professor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'assistant', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'real\sestate\sagent', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'secretary', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'representative', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'member', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'advisor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'medical\sdoctor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'counsel', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'management', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'controller', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'development', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'insurance\sagent', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'human\sresource', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'broker', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'sales\sexecutive', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'alumni\sstaff', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'graphic\sdesign', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'staff\smember', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'doctor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'agent', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'physician', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'legal\sstaff', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'instructor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'librarian', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'production', regex = True),'Seniority Level']= 'Entry'                               
        df.loc[df['Title'].str.contains(pat = 'producer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'general/technical', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'technician', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'marketing', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'technology', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'professional', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'contractor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'facilities', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'publisher', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'it\sspecialist', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'educator', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'information\ssystems', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'maintenance\sstaff', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'sales\srepresentative', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'sheriff', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'purchasing', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'corporate\ssecretary', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'general\smedical', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'superintendent', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'faculty', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'recruiter', regex = True),'Seniority Level']= 'Entry'                             
        df.loc[df['Title'].str.contains(pat = 'facilities', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'sales\sassociate', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'advisor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'merchandise', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'fellow', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'government', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'cashier', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'pediatric', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'contributo', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'cpa\s', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'relations', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'graduate', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'merchandising', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'lecturer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'coordinator', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'attorney', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'clerk', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'programmer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'assistant', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'grade', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'reporter', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'franchisee', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'legal', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'photographer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'customer', regex = True),'Seniority Level']= 'Entry'

        df.loc[df['Title'].str.contains(pat = 'data\sentry', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'entry', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'operator', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'data\sprocessing', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'curator', regex = True),'Seniority Level']= 'Entry'

        df.loc[df['Title'].str.contains(pat = 'account', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'staff', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'specialist', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'actor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'adjunct', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'adviser', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'investigator', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'mechanic', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'anaesthe', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'analsyt', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'adviser', regex = True),'Seniority Level']= 'Entry'

        df.loc[df['Title'].str.contains(pat = 'anchor', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'anaesthe', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'user', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'architect', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'developer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'designer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'integrator', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'trainer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'appraiser', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'banker', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'bookkeeper', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'practitioner', regex = True),'Seniority Level']= 'Entry' 
        df.loc[df['Title'].str.contains(pat = 'writer', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'planner', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'foreman', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'artist', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'gynecolog', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'employee', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'host$', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'inspector', regex = True),'Seniority Level']= 'Entry'
        df.loc[df['Title'].str.contains(pat = 'salesperson', regex = True),'Seniority Level']= 'Entry'

        

        df.loc[df['Title'].str.contains(pat = 'head\s', regex = True),'Seniority Level']= 'Head'
        df.loc[df['Title'].str.contains(pat = 'head$', regex = True),'Seniority Level']= 'Head'

        df.loc[df['Title'].str.contains(pat = 'manager', regex = True),'Seniority Level']= 'Manager'
        df.loc[df['Title'].str.contains(pat = '\smgr', regex = True),'Seniority Level']= 'Manager'
        df.loc[df['Title'].str.contains(pat = 'mgr$', regex = True),'Seniority Level']= 'Manager'
        df.loc[df['Title'].str.contains(pat = '^gm$', regex = True),'Seniority Level']= 'Manager'
        df.loc[df['Title'].str.contains(pat = '^gm\s', regex = True),'Seniority Level']= 'Manager'

        df.loc[df['Title'].str.contains(pat = 'senior\s', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'senior$', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = '^senior$', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'architect\s', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'engineer', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'analyst', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'leader', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'lead', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'officer', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'admin\s', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'admin', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'administrator', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'supervisor', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'treasurer', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = 'general\scounsel', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = '^sr\s', regex = True),'Seniority Level']= 'Senior'
        df.loc[df['Title'].str.contains(pat = '^sr.', regex = True),'Seniority Level']= 'Senior'





        df.loc[df['Title'].str.contains(pat = 'intern', regex = True),'Seniority Level']= 'Internship'
        df.loc[df['Title'].str.contains(pat = 'student ', regex = True),'Seniority Level']= 'Internship'
        df.loc[df['Title'].str.contains(pat = 'apprentice ', regex = True),'Seniority Level']= 'Internship'


        df.loc[df['Title'].str.contains(pat = '[Pp]artner', regex = True),'Seniority Level']= 'Partner'

        Director=['director','board of members','board of director','managing director']
        df.loc[df['Title'].str.contains(pat = 'board\sof', regex = True),'Seniority Level']= 'Director'
        df.loc[df['Title'].str.contains(pat = 'director', regex = True),'Seniority Level']= 'Director'
        df.loc[df['Title'].str.contains(pat = 'managing\sdirector', regex = True),'Seniority Level']= 'Director'
        df.loc[df['Title'].str.contains(pat = 'board\smember', regex = True),'Seniority Level']= 'Director'
        df.loc[df['Title'].str.contains(pat = 'bod\s', regex = True),'Seniority Level']= 'Director'
        df.loc[df['Title'].str.contains(pat = 'trustee', regex = True),'Seniority Level']= 'Director'



        df.loc[df['Title'].str.contains(pat = '[Ff]ounder', regex = True),'Seniority Level']= 'Founder'
        df.loc[df['Title'].str.contains(pat = '[Cc]o\sfounder', regex = True),'Seniority Level']= 'Founder'

        df.loc[df['Title'].str.contains(pat = 'ceo', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'coo\s', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = '^coo$', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'coo[,.]', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'cmo\s', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'cco\s', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'cso\s', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'cfo\s', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = '^cfo', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'principal', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'chief\s', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'chief$', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'principle', regex = True),'Seniority Level']= 'C level'
        df.loc[df['Title'].str.contains(pat = 'dean\s', regex = True),'Seniority Level']= 'C level'


        df.loc[df['Title'].str.contains(pat = '[Pp]resident', regex = True),'Seniority Level']= 'Owner'

        df.loc[df['Title'].str.contains(pat = '[Cc]hair', regex = True),'Seniority Level']= 'Owner'
        df.loc[df['Title'].str.contains(pat = '\svice', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '^vice\s', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = 'vice\spresident', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = 'vp-', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '\svp\s', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '\svp$', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '^vp$', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = 'svp', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = 'avp', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '^vp', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '^evp', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = 'senior\sevp', regex = True),'Seniority Level']= 'VP'


        df.loc[df['Title'].str.contains(pat = 'senior\svp', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = 'sr\svp', regex = True),'Seniority Level']= 'VP'
        df.loc[df['Title'].str.contains(pat = '^srvp', regex = True),'Seniority Level']= 'VP'


        df.loc[df['Title'].str.contains(pat = '[Oo]wner', regex = True),'Seniority Level']= 'Owner'
        df.loc[df['Title'].str.contains(pat = '[Cc]hairman', regex = True),'Seniority Level']= 'Owner'
        df.loc[df['Title'].str.contains(pat = 'vicepresident', regex = True),'Seniority Level']= 'VP'



        df.loc[df['Title'].str.contains(pat = 'other', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'manager\s', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'manager', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'specialist', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'franchisee', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'specialist', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'sport', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'sports', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'adjunct', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'assistant', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'coach', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'adviser', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'advisorAnalsyt', regex = True),'Department']= 'Others'

        df.loc[df['Title'].str.contains(pat = 'analys', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'apprentice', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'warden', regex = True),'Department']= 'Others'
        df.loc[df['Title'].str.contains(pat = 'clerk', regex = True),'Department']= 'Others'


        df.loc[df['Title'].str.contains(pat = 'adminis', regex = True),'Department']= 'Administrative'
        df.loc[df['Title'].str.contains(pat = 'dba', regex = True),'Department']= 'Administrative'
        df.loc[df['Title'].str.contains(pat = '^admin', regex = True),'Department']= 'Administrative'
        df.loc[df['Title'].str.contains(pat = 'admin', regex = True),'Department']= 'Administrative'
        df.loc[df['Title'].str.contains(pat = '^admin\.', regex = True),'Department']= 'Administrative'


        df.loc[df['Title'].str.contains(pat = '^art', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = '\sart\s', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = 'arts$', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = 'design', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = 'animation', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = 'graphic', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = 'photographer', regex = True),'Department']= 'Arts And Design'
        df.loc[df['Title'].str.contains(pat = 'artist', regex = True),'Department']= 'Arts And Design'

        df.loc[df['Title'].str.contains(pat = 'support', regex = True),'Department']= 'Support'

        df.loc[df['Title'].str.contains(pat = 'business', regex = True),'Department']= 'Business Development'
        df.loc[df['Title'].str.contains(pat = 'business development', regex = True),'Department']= 'Business Development'

        df.loc[df['Title'].str.contains(pat = 'community', regex = True),'Department']= 'Community And Social Service'
        df.loc[df['Title'].str.contains(pat = 'social', regex = True),'Department']= 'Community And Social Service'
        df.loc[df['Title'].str.contains(pat = 'youth', regex = True),'Department']= 'Community And Social Service'
        df.loc[df['Title'].str.contains(pat = 'fire\sprotect', regex = True),'Department']= 'Community And Social Service'


        df.loc[df['Title'].str.contains(pat = 'consult', regex = True),'Department']= 'Consulting'


        df.loc[df['Title'].str.contains(pat = 'client', regex = True),'Department']= 'Customer Success'
        df.loc[df['Title'].str.contains(pat = 'customer', regex = True),'Department']= 'Customer Success'


        df.loc[df['Title'].str.contains(pat = 'educat', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'student', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'faculty', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'college', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'professor', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'learning', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'exam', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'school', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'university', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'teacher', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'science', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'tutor', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'academic', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'librar', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'instruct', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'admission', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'lecture', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'dean', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'grade', regex = True),'Department']= 'Education'
        df.loc[df['Title'].str.contains(pat = 'master', regex = True),'Department']= 'Education'


        df.loc[df['Title'].str.contains(pat = 'engineer', regex = True),'Department']= 'Engineering'
        df.loc[df['Title'].str.contains(pat = 'engineering', regex = True),'Department']= 'Engineering'
        df.loc[df['Title'].str.contains(pat = '\senggEng', regex = True),'Department']= 'Engineering'
        df.loc[df['Title'].str.contains(pat = '\seng\s', regex = True),'Department']= 'Engineering'

        df.loc[df['Title'].str.contains(pat = 'entrepreneur', regex = True),'Department']= 'Entrepreneurship'

        df.loc[df['Title'].str.contains(pat = 'financ', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'banking', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'cash', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'credit', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'loan', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'invest', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'broker', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'insurance', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'cfoBanker', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'banker', regex = True),'Department']= 'Finance'
        df.loc[df['Title'].str.contains(pat = 'wealth', regex = True),'Department']= 'Finance'

        df.loc[df['Title'].str.contains(pat = 'health', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'hospital', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'doctor', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'nurs', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'medic', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'clinic', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'radiology', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'patient', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'nutrition', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'anesthesiologist', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'pharma', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'surgery', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'anesthesia', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'anaesthe', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'cardiac', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'gynecolog', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'obstetric', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'oncolog', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'hematology', regex = True),'Department']= 'Healthcare Services'
        df.loc[df['Title'].str.contains(pat = 'denta', regex = True),'Department']= 'Healthcare Services'




        df.loc[df['Title'].str.contains(pat = 'human', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = 'recruit', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = 'payroll', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = 'talent\sacq', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = 'placement', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = '^hr', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = '^hr$', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = '\shr\s', regex = True),'Department']= 'Human Resource'
        df.loc[df['Title'].str.contains(pat = 'employment', regex = True),'Department']= 'Human Resource'

        df.loc[df['Title'].str.contains(pat = '^it\s', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = '\sit\s', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'information', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'software', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = '\scio\s', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = '\sciso\s', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = '\scto\s', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'developer', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'coder', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'coding', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'data', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'appli', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'desktop', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'techn', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'network', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'server', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'file\strans', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'applicat', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'web', regex = True),'Department']= 'Information Technology'
        df.loc[df['Title'].str.contains(pat = 'computer', regex = True),'Department']= 'Information Technology'




        df.loc[df['Title'].str.contains(pat = 'legal', regex = True),'Department']= 'Legal'
        df.loc[df['Title'].str.contains(pat = 'law', regex = True),'Department']= 'Legal'
        df.loc[df['Title'].str.contains(pat = 'attorney', regex = True),'Department']= 'Legal'
        df.loc[df['Title'].str.contains(pat = 'court', regex = True),'Department']= 'Legal'

        df.loc[df['Title'].str.contains(pat = 'market', regex = True),'Department']= 'Marketing'
        df.loc[df['Title'].str.contains(pat = 'advertis', regex = True),'Department']= 'Marketing'
        df.loc[df['Title'].str.contains(pat = '^cmo$', regex = True),'Department']= 'Marketing'
        df.loc[df['Title'].str.contains(pat = '^cmo\s', regex = True),'Department']= 'Marketing'
        df.loc[df['Title'].str.contains(pat = '\scmo\s', regex = True),'Department']= 'Marketing'


        df.loc[df['Title'].str.contains(pat = 'media', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'communication', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'music', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'youtube', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'serial', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'actor', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'actressAnchor', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'anchor', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'reporter', regex = True),'Department']= 'Media And Communication'

        df.loc[df['Title'].str.contains(pat = 'military', regex = True),'Department']= 'Military And Protective Services'
        df.loc[df['Title'].str.contains(pat = 'army', regex = True),'Department']= 'Military And Protective Services'

        df.loc[df['Title'].str.contains(pat = 'operat', regex = True),'Department']= 'Operations'
        df.loc[df['Title'].str.contains(pat = '^coo\s', regex = True),'Department']= 'Operations'
        df.loc[df['Title'].str.contains(pat = '^coo$', regex = True),'Department']= 'Operations'
        df.loc[df['Title'].str.contains(pat = 'compliance', regex = True),'Department']= 'Operations'

        df.loc[df['Title'].str.contains(pat = 'product\smanagement', regex = True),'Department']= 'Program And Project Management'
        df.loc[df['Title'].str.contains(pat = 'program\sand\sproject', regex = True),'Department']= 'Program And Project Management'
        df.loc[df['Title'].str.contains(pat = 'project\s', regex = True),'Department']= 'Program And Project Management'
        df.loc[df['Title'].str.contains(pat = 'program', regex = True),'Department']= 'Program And Project Management'
        df.loc[df['Title'].str.contains(pat = 'product', regex = True),'Department']= 'Program And Project Management'


        df.loc[df['Title'].str.contains(pat = 'purchas', regex = True),'Department']= 'Purchasing'
        df.loc[df['Title'].str.contains(pat = 'procure', regex = True),'Department']= 'Purchasing'
        df.loc[df['Title'].str.contains(pat = 'inventory', regex = True),'Department']= 'Purchasing'

        df.loc[df['Title'].str.contains(pat = 'quality', regex = True),'Department']= 'Quality Assurance'
        df.loc[df['Title'].str.contains(pat = '\sqa\s', regex = True),'Department']= 'Quality Assurance'
        df.loc[df['Title'].str.contains(pat = '\sqc\s', regex = True),'Department']= 'Quality Assurance'
        df.loc[df['Title'].str.contains(pat = 'assurance', regex = True),'Department']= 'Quality Assurance'
        df.loc[df['Title'].str.contains(pat = 'test', regex = True),'Department']= 'Quality Assurance'

        df.loc[df['Title'].str.contains(pat = 'construction', regex = True),'Department']= 'Real Estate'
        df.loc[df['Title'].str.contains(pat = 'property', regex = True),'Department']= 'Real Estate'
        df.loc[df['Title'].str.contains(pat = 'real\sestate', regex = True),'Department']= 'Real Estate'

        df.loc[df['Title'].str.contains(pat = 'research', regex = True),'Department']= 'Research'
        df.loc[df['Title'].str.contains(pat = '\sra\s', regex = True),'Department']= 'Research'

        df.loc[df['Title'].str.contains(pat = 'sale', regex = True),'Department']= 'Sales'
        df.loc[df['Title'].str.contains(pat = 'sales', regex = True),'Department']= 'Sales'
        df.loc[df['Title'].str.contains(pat = 'retail', regex = True),'Department']= 'Sales'

        df.loc[df['Title'].str.contains(pat = 'account', regex = True),'Department']= 'Accounting'
        df.loc[df['Title'].str.contains(pat = 'tax', regex = True),'Department']= 'Accounting'
        df.loc[df['Title'].str.contains(pat = 'bill', regex = True),'Department']= 'Accounting'
        df.loc[df['Title'].str.contains(pat = 'audit', regex = True),'Department']= 'Accounting'
        df.loc[df['Title'].str.contains(pat = 'budget', regex = True),'Department']= 'Accounting'
        df.loc[df['Title'].str.contains(pat = 'asset', regex = True),'Department']= 'Accounting'


        df.loc[df['Title'].str.contains(pat = 'law', regex = True),'Department']= 'Legal'
        df.loc[df['Title'].str.contains(pat = 'advocate', regex = True),'Department']= 'Legal'
        df.loc[df['Title'].str.contains(pat = 'marketing', regex = True),'Department']= 'Marketing'
        df.loc[df['Title'].str.contains(pat = 'media', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'communication', regex = True),'Department']= 'Media And Communication'
        df.loc[df['Title'].str.contains(pat = 'militaryBattalion', regex = True),'Department']= 'Military And Protective Services'
        df.loc[df['Title'].str.contains(pat = 'battalion', regex = True),'Department']= 'Military And Protective Services'
        

        ## Cleaning Phone Numbers

        df=df.replace('\(','',regex=True)
        df=df.replace('\)','',regex=True)
        df['Company Phone']=df['Company Phone'].str.replace(' ','')
        df['Company Phone']=df['Company Phone'].str.replace('-','')
        df['Company Phone']=df['Company Phone'].str.replace('+','')
        df['Company Phone']=df['Company Phone'].str.replace("'",'')
        df['Company Phone']=df['Company Phone'].str.replace(".",'')
        df['Company Phone']=df['Company Phone'].str.replace("?",'')

        # cleaning linkedin URL
        df[['correct', 'domain']]= df['Person Linkedin Url'].str.split('http://www.linkedin.com/in/'or'https://www.linkedin.com/in/',expand=True)
        df[['correct1', 'domain1']]= df['Company Linkedin Url'].str.split('http://www.linkedin.com/company/'or'https://www.linkedin.com/company/',expand=True)
        df.loc[df['domain'].isnull(),'Person Linkedin Url']=''
        df.loc[df['domain1'].isnull(),'Company Linkedin Url']=''


        df['Company City']=df['Company City'].str.replace('?','')
        df['Title']=df['Title'].str.replace('?','')
        df['Company State']=df['Company State'].str.replace('?','')
        df['Company Country']=df['Company Country'].str.replace('?','')
        df['Company']=df['Company'].str.replace('?','')

        df=df.replace('-9999','',regex=True)
        df.loc[df['Company Phone'].str.isnumeric()==False,'Company Phone']=''
        df.loc[df['Company Phone'].str.isalpha()==True,'Company Phone']=''
        df.loc[df['Company Phone']==9999,'Company Phone']=''
        df.loc[df['Company City'].str.isnumeric()==True,'Company City']=''
        df.loc[df['Company State'].str.isnumeric()==True,'Company State']=''
        df.loc[df['Company Country'].str.isnumeric()==True,'Company Country']=''
        df.loc[df['SEO Description'].str.isnumeric()==True,'SEO Description']=''
        df.loc[df['Technologies'].str.isnumeric()==True,'Technologies']=''
        df.loc[df['Keywords'].str.isnumeric()==True,'Keywords']=''


        Blank_title=df.loc[df['Title']==""]
        Blank_title['remarks']='Blank Title'
        Blank_title_index=df.loc[df['Title']==""].index
        df=df.drop(index=Blank_title_index,axis='rows')
        Error_list=Error_list.append(Blank_title)
        df.loc[df['Company Phone']=='9999','Company Phone']= ''
        df.loc[df['Annual Revenue_n']=='','Annual Revenue_n']= '$0-$1M'
        df.loc[df['Annual Revenue_n'].isna(),'Annual Revenue_n']= '$0-$1M'

        blank_industry=df.loc[df['Industry']=='']
        blank_industry['remarks']='Blank Industry'
        blank_industry_index=df.loc[df['Industry']==''].index
        df=df.drop(index=blank_industry_index, axis='rows')
        Error_list=Error_list.append(blank_industry)

        wrong_email=df.loc[~(df['Email'].str.contains(pat = '@', regex = True))]
        wrong_email['remarks']='Email id not Valid'
        wrong_email_index=df.loc[~(df['Email'].str.contains(pat = '@', regex = True))].index
        df=df.drop(index=wrong_email_index, axis='rows')
        Error_list=Error_list.append(wrong_email)

        df['Company Phone']= df['Company Phone'].str.strip()
        df['phone_count']=df['Company Phone'].str.len()
        df.loc[~((df['phone_count'] >= 7) & (df['phone_count'] <= 15)),'Company Phone']=""
        df=df.drop('phone_count',axis='columns')
        df['First Name']=df['First Name'].str.title()

        df['Company']=df['Company'].str.title()
        df['Last Name']=df['Last Name'].str.title()
        df['Title']=df['Title'].str.title()
        df['Industry']=df['Industry'].str.title()
        df['Industry_M']=df['Industry_M'].str.title()
        df['Company Address']=df['Company Address'].str.title()
        df['Company City']=df['Company City'].str.title()
        df['Company Country']=df['Company Country'].str.title()
        df['Website']=df['Website'].str.lower()
        df['Email']=df['Email'].str.lower()
        df['Person Linkedin Url']=df['Person Linkedin Url'].str.lower()
        df['Company Linkedin Url']=df['Company Linkedin Url'].str.lower()
        df['Person Linkedin Url']=df['Person Linkedin Url'].str.lower()
        df['Company Linkedin Url']=df['Company Linkedin Url'].str.lower()
        df['Facebook Url']=df['Facebook Url'].str.lower()
        df['Twitter Url']=df['Twitter Url'].str.lower()


        df['First Name']=df['First Name'].str.strip()
        df['Company']=df['Company'].str.strip()
        df['Last Name']=df['Last Name'].str.strip()
        df['Title']=df['Title'].str.strip()
        df['Seniority Level']=df['Seniority Level'].str.strip()
        df['Industry']=df['Industry'].str.strip()
        df['Industry_M']=df['Industry_M'].str.strip()
        df['Company Address']=df['Company Address'].str.strip()
        df['Company City']=df['Company City'].str.strip()
        df['Company Country']=df['Company Country'].str.strip()
        df['Website']=df['Website'].str.strip()
        df['Email']=df['Email'].str.strip()
        df['Person Linkedin Url']=df['Person Linkedin Url'].str.strip()
        df['Company Linkedin Url']=df['Company Linkedin Url'].str.strip()
        df['Person Linkedin Url']=df['Person Linkedin Url'].str.strip()
        df['Company Linkedin Url']=df['Company Linkedin Url'].str.strip()
        df['Facebook Url']=df['Facebook Url'].str.strip()
        df['Twitter Url']=df['Twitter Url'].str.strip()


        blank_comp=df.loc[df['Company']=='']
        blank_comp2=df.loc[df['Company'].isna()]
        blank_comp=blank_comp.append(blank_comp2)
        blank_comp['remarks']='Blank Company'
        blank_comp_index=df.loc[df['Company']==''].index
        df=df.drop(index=blank_comp_index, axis='rows')
        Error_list=Error_list.append(blank_comp)

        blank_web=df.loc[df['Website']=='']
        blank_web2=df.loc[df['Website'].isna()]
        blank_web=blank_web.append(blank_web2)
        blank_web['remarks']='Blank website'
        blank_web_index=df.loc[df['Website']==''].index
        df=df.drop(index=blank_web_index, axis='rows')
        Error_list=Error_list.append(blank_web)
        df['Company Address']=df['Company Address'].str.replace('?','')

        df = df[['First Name', 'Last Name', 'Title','Seniority Level','Department', 'Email', 'Company','Website', 'Employees Size',
            'Annual Revenue_n','Industry','Industry_M','Company Address','Company City','Company State','Company Country','Company Phone','Person Linkedin Url',
            'Company Linkedin Url','Facebook Url', 'Twitter Url', 'SEO Description', 
            'Keywords','Technologies' ]]


        
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=Clean.csv"
        resp.headers["Content-Type"] = "text/csv"

        upload.var=Error_list

        return resp

    return render_template('index.html')

           
 
@app.route('/error', methods=['GET', 'POST'])
def error():
    mu=upload.var
    mu = make_response(mu.to_csv())
    mu.headers["Content-Disposition"] = "attachment; filename=error.csv"
    mu.headers["Content-Type"] = "text/csv"  
    return mu   


if __name__ == '__main__':
    app.run(debug=True)