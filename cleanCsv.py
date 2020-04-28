import pandas as pd
import numpy as np
import re
import datetime
import warnings
warnings.filterwarnings('ignore')

# #dataframes
# df_a = pd.read_csv('Data/app-store-apple-data-set-10k-apps/AppleStore.csv')
# #df_a.set_index('id', inplace=True)
# df_a.drop(columns='Unnamed: 0', inplace=True)
# df_a_d = pd.read_csv('Data/app-store-apple-data-set-10k-apps/appleStore_description.csv')
# df_a_all = df_a.join(df_a_d, how='right', lsuffix='id')
# df_a_all.drop(columns=['idid', 'track_nameid', 'size_bytesid'], inplace=True)
# df_g = pd.read_csv('Data/google-play-store-apps/googleplaystore.csv')
# df_g_d = pd.read_csv('Data/google-play-store-apps/googleplaystore_user_reviews.csv')

############################

#clean methods

#removeplys - removes + sign
def removeplus(x):
    if type(x) == str:
        parts = x.split('+')
        try:
            return int(parts[0])
        except:
            nums = parts[0].split(',')
            final = ''
            for num in nums:
                final += num
            return int(nums[0] + nums[1])
    else:
        return x

#serparateLetters - seperates letters from string
#cleans string to numbers only

def separateLetters(x):
    if x == 'Varies with Device': #only letters
        return np.nan
    reg = re.compile("([0-9.]+)([a-zA-Z]+)") #numbers first
    reg2 = re.compile('([a-zA-Z]+)([0-9]+)') #letters first
    f = None
    try:
        #numbers first
        res = reg.match(x).groups()
        f = (float(res[0]), res[1])
    except:
        #print('in exception of numbers first')
        try:
            res = reg2.match(x).groups()
            #print('in letters first')
            #have to flip tuple
            f = (float(res[1]), res[0])
        except:
            #only numbers or letters
            #print('in exception of letters first')
            if x.isdigit(): #only numbers
                return float(x)
            else: #not convertible
                print('different combination of letters and numbers: {}'.format(x))
                return x
    #res[0] = number, res[1], letter
    if f[1] == 'k': #kilo
        return (f[0] * 1000)
    elif f[1] == 'M': #1e6
        return (f[0] * 1000000)
    else:
        print('different letter, pls update : {}'.format(f[1]))
        return f[0]

#removes dollar sign
def dropdollarsign(x):
    if (x[0] == '$'):
        return x[1:]
    else:
        return x

#takes the version of the app and returns it in decimal format
def versionToDecimal(x):
    if (type(x) == str):
        #take minimum of version range
        if ('-' in x):
            x = x.split(' - ')[0]
        #remove and up to take mimimum
        x = x.replace(' and up', '')
        #split multiple decimals
        #only use first
        if '.' in x:
            parts = x.split('.')
            final = parts[0] + '.' + parts[1]
            for part in parts[2:]:
                final += part
            return final
        else:
            return x
    else:
        return x


######### initiate clean of dataframes ##########

def cleanDatabases():
        #Size
    df_g.Size = df_g.Size.apply(separateLetters)
    df_g.Size.replace(to_replace='1,000+', value=1000, inplace=True)
    df_g.Size.replace(to_replace='Varies with device', value=0.00001, inplace=True)
    df_g.Size = df_g.Size.apply(lambda x: float(x))
    df_g.Size.replace(to_replace=0.00001 ,value=df_g[df_g.Size  > 0.01]['Size'].mean(), inplace=True)


    #reviews
    # be sure to add the letters value to the number
    print('Reviews')
    df_g['Reviews'] = df_g['Reviews'].apply(separateLetters)

    #Rating
    df_g['Rating'].fillna(0.001, inplace=True)
    df_g_na = df_g[df_g['Rating'] < 0]
    df_g.drop(index=10472, inplace=True) #df_g['Rating'] > 5
    #installs

    df_g.Installs.replace(to_replace='Free', value='0,0', inplace=True )
    df_g.Installs.replace(to_replace='0', value='0,0', inplace=True )
    df_g.Installs = df_g.Installs.apply(removeplus)

    #type - 'Paid' / 'Free'
    df_g.Type.replace(to_replace='0', value='Free', inplace=True)

    #price
    df_g.Price.replace(to_replace='Everyone', value='0', inplace=True)
    df_g.Price = df_g.Price.apply(dropdollarsign)
    df_g.Price = df_g.Price.apply(lambda x: float(x))

    #content rating
    content_rating_dict = {
        'Everyone' : 0,
        'Teen' : 1,
        'Everyone 10+' : 2,
        'Mature 17+' : 3,
        'Adults only 18+' : 4,
        'Unrated': 5
    }
    df_g['ContentRatingValue'] = df_g['Content Rating'].replace(content_rating_dict)

    #last updated
    df_g['Last Updated'] = pd.to_datetime(df_g['Last Updated'], format='%B %d, %Y', errors='coerce')

#end cleaning databases
### *** change variable lifespan in above method **** ###
