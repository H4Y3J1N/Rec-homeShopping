import numpy as np


def _ndcg_calculator(gt, rec, idcg):
    dcg = 0.0
    for i, r in enumerate(rec):
        if r == gt:
            print(type(r))
            dcg += 1.0 / np.log(i + 2)
    return dcg / idcg

def ndcg_calculator(answer, submission, n=10):
    idcg = sum((1.0 / np.log(i + 1) for i in range(1, n + 1)))
    assert (answer.user != submission.user).sum() == 0
    ndcg_list = []
    for (_, row_answer), (_, row_submit) in zip(answer.iterrows(), submission.iterrows()):
        ndcg_list.append(_ndcg_calculator(row_answer.item_id, row_submit.predicted_list, idcg))
    ndcg_score = sum(ndcg_list) / len(answer)
    return ndcg_score

def hit_at_k(answer, submission, n=10):
    assert (answer.user != submission.user).sum() == 0
    if n > len(answer):
        n = len(answer)
    hit = 0
    for i in range(len(answer)):
        answer_ids = answer['item_id'].loc[i]
        submission_ids = submission['predicted_list'].loc[i]
        hits = np.isin(submission_ids, answer_ids)
        hit += np.sum(hits) / len(hits)
    hit /= len(answer)
    return hit