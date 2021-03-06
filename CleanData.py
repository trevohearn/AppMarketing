#Trevor O'Hearn
#5/31/20
#imports and clean apps

#imports
import pandas as pd




#data to frame
# df_a = pd.read_csv('Data/app-store-apple-data-set-10k-apps/AppleStore.csv')
# #df_a.set_index('id', inplace=True)
# df_a.drop(columns='Unnamed: 0', inplace=True)
# df_a_d = pd.read_csv('Data/app-store-apple-data-set-10k-apps/appleStore_description.csv')
# df_a_all = df_a.join(df_a_d, how='right', lsuffix='id')
# df_a_all.drop(columns=['idid', 'track_nameid', 'size_bytesid'], inplace=True)
# df_g = pd.read_csv('Data/google-play-store-apps/googleplaystore.csv')
# df_g_d = pd.read_csv('Data/google-play-store-apps/googleplaystore_user_reviews.csv')

#methods

#removeplus
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

#seperateLetters
import re
#returns number only
#to do list: apply value of letter to number
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
                #print('different combination of letters and numbers: {}'.format(x))
                return x

    #res[0] = number, res[1], letter
    if f[1] == 'k': #kilo
        return (f[0] * 1000)
    elif f[1] == 'M': #1e6
        return (f[0] * 1000000)
    else:
        #print('different letter, pls update : {}'.format(f[1]))
        return f[0]

#removes dollar sign
def dropdollarsign(x):
    if (x[0] == '$'):
        return x[1:]
    else:
        return x

#version of app to decimal format
#converts the app version to decimal format
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


#returns list of top genres per number of clusters sent
def testCluster(X,df_g, n = 30, name = 'Label', genre='Genres'):
    agc = AgglomerativeClustering(n_clusters = n)
    agc_minmax = agc.fit(X)
    df_g[name] = agc_minmax.labels_

    glist = []
    for i in range(n):
        df_gCur = df_g[df_g[name] == i]
        label = df_gCur[genre].value_counts().index[0]
        glist.append(label)
    return glist


#clean google dataframe

def cleanDFG(df_g):
    #df_g = pd.read_csv('Data/google-play-store-apps/googleplaystore.csv')
    #Size
    df_g.Size = df_g.Size.apply(separateLetters)
    df_g.Size.replace(to_replace='1,000+', value=1000, inplace=True)
    df_g.Size.replace(to_replace='Varies with device', value=0.00001, inplace=True)
    df_g.Size = df_g.Size.apply(lambda x: float(x))
    df_g.Size.replace(to_replace=0.00001 ,value=df_g[df_g.Size  > 0.01]['Size'].mean(), inplace=True)


    #reviews
    # be sure to add the letters value to the number
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
    df_g = createNameFeatures(df_g, 'App')
    return df_g

def createNameFeatures(frame, column):
    print('in name features')
    df = frame
    consonants = ['b', 'c', 'd', 'f','g','h','j', 'k',
                'l', 'm', 'n', 'p', 'q','r','s','t','v',
                'w','x','y','z']
    vowels = ['a', 'e','i', 'o', 'u']
    alphabet = {'a' : 0, 'e' : 0,'i' : 0, 'o' : 0, 'u' : 0,
    'b' : 0, 'c' : 0, 'd' : 0, 'f' : 0,'g' : 0,'h' : 0 ,'j' : 0, 'k' : 0,
    'l' : 0, 'm' : 0, 'n' : 0, 'p' : 0, 'q' : 0,'r' : 0,'s' : 0,'t' : 0,'v' : 0,
    'w' : 0,'x' : 0,'y' : 0 ,'z' : 0}
    #count letters
    df['nameLength'] = df[column].apply(lambda x : len(x))
    #count words
    df['wordLength'] = df[column].apply(lambda x: len(x.split(' ')))
    #count how many letters
    for a in alphabet:
        df[a] = df[column].apply(lambda x : x.lower().count(a))
    #count syllables
    df['syllables'] = df[column].apply(syllables)
    return df

#count syllables
def syllables(word):
    count = 0
    vowels = 'aeiouy'
    word = word.lower().strip(".:;?!")
    if word[0] in vowels:
        count +=1
    for index in range(1,len(word)):
        if word[index] in vowels and word[index-1] not in vowels:
            count +=1
    if word.endswith('e'):
        count -= 1
    if word.endswith('le'):
        count+=1
    if count == 0:
        count +=1
    return count




#set apple dataframe indices
# df_a_d.set_index('id', inplace=True)
# df_a.set_index('id', inplace=True)
