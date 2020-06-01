def Appanalysis(genre, App):
    import CleanData
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.cluster import AgglomerativeClustering
    import statistics as s

    df = pd.read_csv('Data/google-play-store-apps/googleplaystore.csv')
    #make train test split
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state = 1)

    #print('Input Genre:')
    #genre = str(input()).strip("""!@#$%^&*()_-+={}|\[]:";',.<>?/~`'""").title()
    #print('Input App Name')
    #App = str(input()).strip("""!@#$%^&*()_-+={}|\[]:";',.<>?/~`'""").title()
    vals = {'App' : App, 'Category' : genre, 'Rating' : 0,
            'Reviews' : '0', 'Size' : '0', 'Installs' : '0', 'Type' : 'Free',
            'Price' : '0', 'Content Rating' : 'Everyone', 'Genres' : genre,
             'Last Updated' : 'January 1, 2018', 'Current Ver' : '1.0.0', 'Android Ver' : '1.0.0'}

    #top Genres
    topGenres = list(df.Genres.value_counts().iloc[:20].keys())

    #make an entry for each genre we will be working with
    for x in topGenres:
        vals['Genres'] = x
        vals['Category'] = x
        df = df.append(vals, ignore_index=True)

    #id = df[df['App'] == App and ].index[0]


    df = CleanData.cleanDFG(df)

    #create Frames for each genre
    dfs = []
    for t in topGenres:
        dfs.append(df[df['Genres'] == t])



    features = ['a', 'b', 'c', 'd', 'e', 'f', 'g' ,'h', 'i', 'j', 'k', 'l',
                'm', 'n','o','p','q','r','s','t','u','v','w','x','y','z',
                'nameLength', 'wordLength', 'syllables']
    scaler1 = StandardScaler()
    agc = AgglomerativeClustering(n_clusters = 10)
    clusters = []
    #analyze each Frame
    for d in dfs:
        scaler1_results = scaler1.fit_transform(d[features])
        agc_standard = agc.fit(scaler1_results)
        d['Label'] = agc_standard.labels_
        clusters.append(d[d.App == App].iloc[0].Label)


    def createStats(df, cluster):
        #get set in which new app resides
        df_app = df[df['Label'] == cluster]
        #your cluster statistics
        #print(df_app.Rating.describe())
        dfsets = []
        for num in range(10):
            dfsets.append(df[df['Label'] == num])
        means = []
        for x, df in enumerate(dfsets):
            curMean = df.Rating.mean()
            if (x == cluster):
                print('Your cluster {} install mean: {}'.format(x, curMean))
            else:
                print('Cluster {} install mean: {}'.format(x, curMean))
            means.append(curMean)
        deviation = s.stdev(means)
        m = s.mean(means)
        #print('Standard Deviation of cluster averages: {}'.format(deviation))
        #print('Mean of cluster averages: {}'.format(m))
        #print('Your cluster install average: {}'.format(means[cluster]))
        ymean = means[cluster]
        deltamean = abs(ymean - m)
        deviationsaway = deltamean / deviation
        #print ('you are {} deviation away from the mean'.format(deviationsaway))
        #print('Your app will have an average rating of {}'.format(df_app.Rating.mean()))
        #print('Your app will have an average of {} reviews'.format(df_app.Reviews.mean()))
        return {'ymean' : ymean, 'deviation_of_means' : deviation, 'means' : means, 'mean_of_means' : m, 'df_genre' : df_app}
        # for col in df.columns:
    #     print(df[col].describe())
    #     print(' - ')



    genreStats = {}
    for num, d in enumerate(dfs):
        #print('----------------')
        #print('Your app statistics in {} genre'.format(topGenres[num]))
        genreStats[topGenres[num]] = createStats(d, clusters[num])
    #print(genreStats)
    return genreStats
    # for num, t in enumerate(topGenres):
    #     print('{}'.format(t))
    #     print('Your mean: {}'.format(appmeans[num][0]))
    #     print('Your std: {}'.format(appmeans[num][1]))
    #     print('------------------------------')
