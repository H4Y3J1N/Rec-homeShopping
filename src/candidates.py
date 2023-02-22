import numpy as np
import pandas as pd
import tqdm as tqdm

def general_most_popular(train):
    last_week_list = np.sort(train.weeks.unique())

    # 마지막 n주, n-1주 각각 MP를 50개씩 추출
    last_week_ver1 = last_week_list[-1]
    last_week_ver2 = last_week_list[-2]

    MP_latest_ver1_df = train.query(f"weeks == {last_week_ver1}")
    MP_df = MP_latest_ver1_df.groupby('item_id')['user'].count().sort_values(ascending=False).reset_index()
    MP_df.columns = ['item_id','general_counts_ver1']
    MP_ver1 = MP_df.copy()
    MP_candidate_df = MP_df[:100].copy()
    MP_candidate_df['join_col'] = 1

    customer_df = train[['user']].drop_duplicates()
    customer_df['join_col'] = 1
    mp_cand1 = customer_df.copy()
    mp_cand1 = mp_cand1.merge(MP_candidate_df, on="join_col")\
                .drop_duplicates(subset=['user','item_id'])[["user","item_id"]]

    MP_latest_ver2_df = train.query(f"weeks == {last_week_ver2}")
    MP_df = MP_latest_ver2_df.groupby('item_id')['user'].count().sort_values(ascending=False).reset_index()
    MP_df.columns = ['item_id','general_counts_ver2']
    MP_ver2 = MP_df.copy()
    MP_candidate_df = MP_df[:100].copy()
    MP_candidate_df['join_col'] = 1
    customer_df = train[['user']].drop_duplicates()
    customer_df['join_col'] = 1
    mp_cand2 = customer_df.copy()
    mp_cand2 = mp_cand2.merge(MP_candidate_df, on="join_col")[["user","item_id"]]
    mp_cand2 = mp_cand2.drop_duplicates(subset=['user','item_id'])[["user","item_id"]]

    popular_items_cand = pd.concat([mp_cand1, mp_cand2])
    popular_items_cand = popular_items_cand.drop_duplicates()

    # feature 작업
    general_mp_1 = pd.merge(MP_ver1, MP_ver2, how="left",on="item_id")
    general_mp_2 = pd.merge(MP_ver2, MP_ver1, how="left", on="item_id")
    general_MP_feature = pd.concat([general_mp_1, general_mp_2])
    general_MP_feature = general_MP_feature.drop_duplicates()

    return popular_items_cand, general_MP_feature


def recent30days_MP(train):
    recent_days = 30
    train_recent30 = train[train["timestamp"] >= (train["timestamp"].max() - pd.Timedelta(days=recent_days))]
    mp = train_recent30.item_id.value_counts().head(100).index.tolist()
    mp_unique = train_recent30.groupby("item_id").user.nunique().nlargest(100).index.tolist()
    recent30_mp = list(set(mp+mp_unique))
    users = train.user.unique().tolist()

    rows = []
    for user in users:
        for item in recent30_mp:
            row = {"user": user, "item_id": item}
            rows.append(row)
    df = pd.DataFrame(rows)
    return df

# def personal_most_popular(train):
#     reclick_users = train.groupby(["user", "item_id"])["timestamp"].count().reset_index()
#     reclick_users = reclick_users[reclick_users["timestamp"] > 3].sort_values(by=["user","timestamp"],ascending=False)
#     # 3번 이상 조회된 item 중 top 30개 
#     top_click = reclick_users.groupby("item_id").count()["timestamp"].reset_index().sort_values(by="timestamp", ascending=False).head(30)
#     head_df_list = []
#     for user_id in train.user.unique():
#         reclick_user_len = len(reclick_users[reclick_users["user"]==user_id].head(30))
#         if reclick_user_len <30:
#             # top N개가 없는 경우
#             user_df = reclick_users[reclick_users["user"]==user_id]
#             df = pd.DataFrame()
#             df["user"] = [user_id for _ in range(30-len(user_df))]
#             df["item_id"] = [top_click.item_id.values[num] for num in range(30-len(user_df))]
#             df = pd.concat([user_df, df])
#             head_df_list.append(df)
#         else:
#             head_df_list.append(reclick_users[reclick_users["user"]==user_id].head(30))
#         reclick_users_candidate = pd.concat(head_df_list)
#     return reclick_users_candidate 