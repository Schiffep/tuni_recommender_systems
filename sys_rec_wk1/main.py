import pandas as pd
pd.set_option("display.max_columns", None)

def displayData():
    df_ratings = pd.read_csv("./data/ratings.csv")
    print(df_ratings.head())
    df_movies = pd.read_csv("./data/movies.csv")
    print(df_movies.head())
    print("The count of ratings (rows) is " + str(df_ratings.shape[0]))

def userBased(min_periods=2):
    df_ratings = pd.read_csv("./data/ratings.csv")
    df_ratings = df_ratings[["userId", "movieId", "rating"]]
    ratings_pivot = df_ratings.pivot_table("rating", index="userId", columns="movieId")
    pearson = ratings_pivot.T.corr(method="pearson", min_periods=min_periods)
    user = 2
    sim_users = pearson[user].sort_values(ascending=False)[0:41].index.tolist()
    #sim_users.remove(user)
    #TODO: check if user in sim_users and add if nessecerrez remove 41


    averages = df_ratings[df_ratings.userId.isin(sim_users)].pivot_table("rating", index="userId", columns="movieId").T.mean()

    #TODO drop alreadz rated movies
    pred = df_ratings[df_ratings.userId.isin(sim_users)]
    #pred.set_index("userId")
    #print(pred)

    #for i in range(len(sim_users)):
    #    pred[pred["userId"] == sim_users[i]] = pred[pred["userId"] == sim_users[i]].subtract(averages[averages.index == sim_users[i]])


    pred_pivot = pred.pivot_table("rating", index="userId", columns="movieId")
    #print(pred_pivot)

    #sim_users.remove(user)

    new_pearson = pearson[pearson.index == user].T
    new_pearson = new_pearson[new_pearson.index.isin(sim_users)]

    sub_pivot = pred_pivot.sub(pred_pivot.mean(axis=1), axis=0)
    mult_pivot = sub_pivot.mul(new_pearson.squeeze(), axis=0)

    #TODO: divide by all 40??

    #TODO: remove already rated movies by user

    mult_pivot.drop(index=user)
    sim_users.remove(user)
    new_pearson = new_pearson[new_pearson.index.isin(sim_users)]

    sum_of_blank = new_pearson.sum()[user]

    print(mult_pivot)

    sum_adj_ratings = mult_pivot.sum(axis='columns')
    print(sum_adj_ratings)


    #print(mult_pivot)

    #print(df_ratings.head())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #displayData()
    userBased()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
