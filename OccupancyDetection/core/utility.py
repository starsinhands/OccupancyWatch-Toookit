import numpy as np

def find_transition_points(y):
    """
    Find transition points in the y array.
    """
    diff = np.diff(y)
    pos_transitions = np.where(diff > 0)[0] + 1  # From 0 to 1
    neg_transitions = np.where(diff < 0)[0] + 1  # From 1 to 0
    return pos_transitions, neg_transitions

def calculate_f1(prediction, y_test, tolerance):
    # Find transition points in y_test
    pos_transitions_y_test, neg_transitions_y_test = find_transition_points(y_test)

    # Find transition points in prediction
    pos_transitions_prediction, neg_transitions_prediction = find_transition_points(prediction)

    # Initialize counters
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    # Calculate TP, FP, TN, FN
    for i in range(len(pos_transitions_y_test)):
        closest_index = np.argmin(np.abs(pos_transitions_prediction - pos_transitions_y_test[i]))
        if np.abs(pos_transitions_prediction[closest_index] - pos_transitions_y_test[i]) <= tolerance:
            true_positives += 1
            pos_transitions_prediction = np.delete(pos_transitions_prediction, closest_index)
    false_positives += len(pos_transitions_prediction)

    for i in range(len(neg_transitions_y_test)):
        closest_index = np.argmin(np.abs(neg_transitions_prediction - neg_transitions_y_test[i]))
        if np.abs(neg_transitions_prediction[closest_index] - neg_transitions_y_test[i]) <= tolerance:
            true_negatives += 1
            neg_transitions_prediction = np.delete(neg_transitions_prediction, closest_index)
    false_negatives += len(neg_transitions_prediction)

    # Calculate F1 score
    if true_positives + false_positives == 0:
        precision = 0
    else:
        precision = true_positives / (true_positives + false_positives)

    if true_positives + false_negatives == 0:
        recall = 0
    else:
        recall = true_positives / (true_positives + false_negatives)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    # Calculate average fragment length for FP and FN
    # FP waste
    # if false_positives == 0:
    #     average_fragment_length_fp = 0
    # else:
    #     total_length_fp = 0
    #     for transition in pos_transitions_prediction:
    #         length = 1
    #         while transition + length-1>len(y_test)-1 and prediction[transition + length-1] == 1:
    #             length += 1
    #         total_length_fp += length
    #     average_fragment_length_fp = total_length_fp / false_positives
    #
    # if false_negatives == 0:
    #     average_fragment_length_fn = 0
    # else:
    #     total_length_fn = 0
    #     for transition in neg_transitions_prediction:
    #         length = 1
    #         while transition + length-1>len(y_test)-1 and y_test[transition + length-1] == 1:
    #             length += 1
    #
    #         total_length_fn += length
    #     average_fragment_length_fn = total_length_fn / false_negatives

    # return f1, precision, recall, average_fragment_length_fp, average_fragment_length_fn
    return f1, precision, recall


# def find_transition_points(y):
#     """
#     Find transition points in the y array.
#     """
#     diff = np.diff(y)
#     pos_transitions = np.where(diff > 0)[0] + 1  # From 0 to 1
#     neg_transitions = np.where(diff < 0)[0] + 1  # From 1 to 0
#     return pos_transitions, neg_transitions
#
# def calculate_f1(prediction, y_test, tolerance):
#     # Find transition points in y_test
#     pos_transitions_y_test, neg_transitions_y_test = find_transition_points(y_test)
#
#     # Find transition points in prediction
#     pos_transitions_prediction, neg_transitions_prediction = find_transition_points(prediction)
#
#     # Initialize counters
#     true_positives = 0
#     false_positives = 0
#     false_negatives = 0
#     true_negatives = 0
#
#     # Calculate TP, FP, TN, FN
#     for i in range(len(pos_transitions_y_test)):
#         closest_index = np.argmin(np.abs(pos_transitions_prediction - pos_transitions_y_test[i]))
#         if np.abs(pos_transitions_prediction[closest_index] - pos_transitions_y_test[i]) <= tolerance:
#             true_positives += 1
#         else:
#             false_negatives += 1
#
#     for i in range(len(neg_transitions_y_test)):
#         closest_index = np.argmin(np.abs(neg_transitions_prediction - neg_transitions_y_test[i]))
#         if np.abs(neg_transitions_prediction[closest_index] - neg_transitions_y_test[i]) <= tolerance:
#             true_negatives += 1
#         else:
#             false_positives += 1
#
#     # Calculate F1 score
#     if true_positives + false_positives == 0:
#         precision = 0
#     else:
#         precision = true_positives / (true_positives + false_positives)
#
#     if true_positives + false_negatives == 0:
#         recall = 0
#     else:
#         recall = true_positives / (true_positives + false_negatives)
#
#     if precision + recall == 0:
#         f1 = 0
#     else:
#         f1 = 2 * (precision * recall) / (precision + recall)
#
#     return f1, precision, recall

import numpy as np


def majority_vote_filter(predictions, window_size):
    """
    应用多数投票滤波器对预测结果进行平滑处理。

    参数:
    predictions : numpy数组
        原始的预测结果数组。
    window_size : int
        投票窗口的大小。

    返回:
    numpy数组
        应用多数投票滤波后的预测结果数组。
    """
    # 初始化滤波后的结果数组，长度与预测结果相同
    filtered_predictions = np.zeros_like(predictions)

    # 对每个预测值应用多数投票
    for i in range(len(predictions)):
        # 确保不会超出数组的边界
        start = max(0, i - window_size + 1)
        end = min(len(predictions), i + 1)

        # 获取当前窗口内的预测结果
        window_predictions = predictions[start:end]

        # 计算窗口内0和1的数量
        num_zeros = np.sum(window_predictions == 0)
        num_ones = np.sum(window_predictions == 1)

        # 选择数量最多的作为该时间点的最终预测
        if num_zeros > num_ones:
            filtered_predictions[i] = 0
        else:
            filtered_predictions[i] = 1

    return filtered_predictions


def calculate_f1(prediction, y_test, tolerance):
    # Find transition points in y_test
    pos_transitions_y_test, neg_transitions_y_test = find_transition_points(y_test)

    # Find transition points in prediction
    pos_transitions_prediction, neg_transitions_prediction = find_transition_points(prediction)

    # Initialize counters
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    # Calculate TP, FP, TN, FN
    for i in range(len(pos_transitions_y_test)):
        closest_index = np.argmin(np.abs(pos_transitions_prediction - pos_transitions_y_test[i]))
        if np.abs(pos_transitions_prediction[closest_index] - pos_transitions_y_test[i]) <= tolerance:
            true_positives += 1
            pos_transitions_prediction = np.delete(pos_transitions_prediction, closest_index)
    false_positives += len(pos_transitions_prediction)

    for i in range(len(neg_transitions_y_test)):
        closest_index = np.argmin(np.abs(neg_transitions_prediction - neg_transitions_y_test[i]))
        if np.abs(neg_transitions_prediction[closest_index] - neg_transitions_y_test[i]) <= tolerance:
            true_negatives += 1
            neg_transitions_prediction = np.delete(neg_transitions_prediction, closest_index)
    false_negatives += len(neg_transitions_prediction)

    # Calculate F1 score
    if true_positives + false_positives == 0:
        precision = 0
    else:
        precision = true_positives / (true_positives + false_positives)

    if true_positives + false_negatives == 0:
        recall = 0
    else:
        recall = true_positives / (true_positives + false_negatives)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)

    # Calculate average fragment length for FP and FN
    # FP waste
    # if false_positives == 0:
    #     average_fragment_length_fp = 0
    # else:
    #     total_length_fp = 0
    #     for transition in pos_transitions_prediction:
    #         length = 1
    #         while transition + length-1>len(y_test)-1 and prediction[transition + length-1] == 1:
    #             length += 1
    #         total_length_fp += length
    #     average_fragment_length_fp = total_length_fp / false_positives
    #
    # if false_negatives == 0:
    #     average_fragment_length_fn = 0
    # else:
    #     total_length_fn = 0
    #     for transition in neg_transitions_prediction:
    #         length = 1
    #         while transition + length-1>len(y_test)-1 and y_test[transition + length-1] == 1:
    #             length += 1
    #
    #         total_length_fn += length
    #     average_fragment_length_fn = total_length_fn / false_negatives

    # return f1, precision, recall, average_fragment_length_fp, average_fragment_length_fn
    return f1, precision, recall


def calculate_f1(prediction, y_test, tolerance):
    # Find transition points in y_test
    pos_transitions_y_test, neg_transitions_y_test = find_transition_points(y_test)

    # Find transition points in prediction
    pos_transitions_prediction, neg_transitions_prediction = find_transition_points(prediction)

    # Initialize counters
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    # Calculate TP, FP, TN, FN
    for i in range(len(pos_transitions_y_test)):
        closest_index = np.argmin(np.abs(pos_transitions_prediction - pos_transitions_y_test[i]))
        if np.abs(pos_transitions_prediction[closest_index] - pos_transitions_y_test[i]) <= tolerance:
            true_positives += 1
            pos_transitions_prediction = np.delete(pos_transitions_prediction, closest_index)
    false_positives += len(pos_transitions_prediction)

    for i in range(len(neg_transitions_y_test)):
        closest_index = np.argmin(np.abs(neg_transitions_prediction - neg_transitions_y_test[i]))
        if np.abs(neg_transitions_prediction[closest_index] - neg_transitions_y_test[i]) <= tolerance:
            true_negatives += 1
            neg_transitions_prediction = np.delete(neg_transitions_prediction, closest_index)
    false_negatives += len(neg_transitions_prediction)

    # Calculate F1 score
    if true_positives + false_positives == 0:
        precision = 0
    else:
        precision = true_positives / (true_positives + false_positives)

    if true_positives + false_negatives == 0:
        recall = 0
    else:
        recall = true_positives / (true_positives + false_negatives)

    if precision + recall == 0:
        f1 = 0
    else:
        f1 = 2 * (precision * recall) / (precision + recall)
    return f1, precision, recall