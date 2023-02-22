import pandas as pd
from datetime import datetime


def featureEngineering(train_user_seq_log):
    train_timestamp =  train_user_seq_log["timestamp"]
    train_user_seq_log_df = train_user_seq_log.copy()

    train_timestamp_df = train_timestamp.to_frame(name='timestamp')
    train_user_seq_log['day_of_week'] = train_timestamp_df['timestamp'].dt.dayofweek
    train_user_seq_log['hour'] = train_timestamp_df['timestamp'].dt.hour

    reference_date = datetime(2021, 2, 11)
    days = (train_timestamp - reference_date).dt.total_seconds() / (24 * 3600)
    days_df = days.astype(int).to_frame(name='days')
    weeks = (days / 7).astype(int) + 1
    weeks_df = weeks.to_frame(name='weeks')
    cumcount = train_user_seq_log.groupby('item_num').cumcount().to_frame(name='cumcount')
    cumcount['cumcount'] = cumcount['cumcount'] + 1

    train_user_seq_log = pd.concat([train_user_seq_log, days_df], axis=1)
    train_user_seq_log = pd.concat([train_user_seq_log, weeks_df], axis=1)
    train_user_seq_log = pd.concat([train_user_seq_log, cumcount], axis=1)

    mp_item = train_user_seq_log_df.item_num.value_counts().reset_index().rename(columns={"index":"item_num","item_num":"click_count"})
    min_val = mp_item['click_count'].min()
    range_val = mp_item['click_count'].max() - mp_item['click_count'].min()
    mp_item['click_count_normalized'] = (mp_item['click_count'] - min_val) / range_val
    train_user_seq_log = pd.merge(train_user_seq_log, mp_item, on='item_num', how='inner')

    user_click = train_user_seq_log_df.user.value_counts().reset_index().rename(columns={"index":"user","user":"user_click_count"})
    user_min_val = user_click['user_click_count'].min()
    user_range_val = user_click['user_click_count'].max() - user_click['user_click_count'].min()
    user_click['user_click_count_normalized'] = (user_click['user_click_count'] - user_min_val) / user_range_val
    train_user_seq_log = pd.merge(train_user_seq_log, user_click, on='user', how='inner')
    fe_train_user_seq_log = train_user_seq_log.drop_duplicates()

    return fe_train_user_seq_log
        