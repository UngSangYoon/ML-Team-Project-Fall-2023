import numpy as np

# convert scores to one-hot targets
def score_to_target(scores):
    target = []
    for score in scores:
        if score[0] > 4:
            score[0] = 4
        if score[1] > 4:
            score[1] = 4
        target.append(int(score[0]*5 + score[1])) # e.g., 2*5 + 4 = 14 means score 2:4
    target = np.array(target)
    target = np.eye(5*5)[target]
    return target

# convert one-hot targets to scores
def target_to_score(targets):
    targets = np.argmax(targets, axis=1)
    scores = []
    for target in targets:
        score = [target // 5, target % 5]
        scores.append(score)
    scores = np.array(scores)
    return scores

def normalize_stats(stats):
    min_vals = np.min(stats, axis=0)
    max_vals = np.max(stats, axis=0)
    for i in range(stats.shape[1]):
        if max_vals[i] == 0 and min_vals[i] == 0:
            continue
        stats[:, i] = (stats[:, i] - min_vals[i]) / (max_vals[i] - min_vals[i])
    return stats, min_vals, max_vals