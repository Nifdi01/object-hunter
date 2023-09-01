import torch
from collections import Counter
from iou import intersection_over_union


def mean_average_precision(
        pred_boxes,
        true_boxes,
        iou_threshold=0.5,
        box_format='corners',
        num_classes=20):
    """
    Calculates mean average precision 

    Parameters:
        pred_boxes (list): list of lists containing all bboxes with each bboxes
        specified as [train_idx, class_prediction, prob_score, x1, y1, x2, y2]
        true_boxes (list): Similar as pred_boxes except all the correct ones 
        iou_threshold (float): threshold where predicted bboxes is correct
        box_format (str): "midpoint" or "corners" used to specify bboxes
        num_classes (int): number of classes

    Returns:
        float: mAP value across all classes given a specific IoU threshold
    """

    # List for storing Average Precisions for respective classes
    average_precisions = list()
    # Used for numerical stability
    epsilon = 1e-6

    # Go through all the classes
    for _class in range(num_classes):
        detections = list()
        ground_truths = list()

        # Go through all the predicitions and ground truths and choose the ones that belong to the _class
        for detection in pred_boxes:
            if detection[1] == _class:
                detections.append(detection)

        for true_box in true_boxes:
            if true_box[1] == _class:
                ground_truths.append(true_box)


        # find the amount of bounding boxes for each training example
        # Counter here finds how many ground truth bboxes we get
        # for each training example, so let's say img 0 has 3,
        # img 1 has 5 then we will obtain a dictionary with:
        # amount_bboxes = {0:3, 1:5}
        amount_bounding_boxes = Counter([gt[0] for gt in ground_truths])

        # We then go through each key, val in this dictionary
        # and convert to the following (w.r.t same example):
        # ammount_bboxes = {0:torch.tensor[0,0,0], 1:torch.tensor[0,0,0,0,0]}
        for key, val in amount_bounding_boxes.items():
            amount_bounding_boxes[key] = torch.zeros(val)

        # Sort by box probabilities which is index 2
        detections.sort(key=lambda x: x[2], reverse=True)
        TP = torch.zeros((len(detections)))
        FP = torch.zeros((len(detections)))
        total_true_bboxes = len(ground_truths)
        
        # If none exists for this _class then we can skip it
        if total_true_bboxes == 0:
            continue

        
        for detection_idx, detection in enumerate(detections):
            # Only take out the ground truths that have the same idx as detection
            ground_truth_image = [
                bbox for bbox in ground_truths if bbox[0] == detection[0]]
            
            num_gts = len(ground_truth_image)
            
            best_iou = 0
            for idx, gt in enumerate(ground_truth_image):
                iou = intersection_over_union(torch.tensor(
                    detection[3:]), torch.tensor(gt[3:]), box_format=box_format)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = idx

            if best_iou > iou_threshold:
                # Only detect ground truth detection once
                if amount_bounding_boxes[detection[0]][best_gt_idx] == 0:
                    # true positive and add this bounding box to seen
                    TP[detection_idx] = 1   
                    amount_bounding_boxes[detection[0]][best_gt_idx] = 1
                else:
                    FP[detection_idx] = 1
           
            # If IOU is lower than threshold then its FP
            else:
                FP[detection_idx] = 1

        TP_cumsum = torch.cumsum(TP, dim=0)
        FP_cumsum = torch.cumsum(FP, dim=0)

        recalls = TP_cumsum / (total_true_bboxes + epsilon)
        precisions = torch.divide(TP_cumsum, (TP_cumsum + FP_cumsum + epsilon))
        precisions = torch.cat((torch.tensor([1]), precisions))
        recalls = torch.cat((torch.tensor([0]), recalls))
        # torch.trapz for numerical integration
        average_precisions.append(torch.trapz(precisions, recalls))

    return sum(average_precisions) / len(average_precisions)
