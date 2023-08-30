import torch
from iou import intersection_over_union


def non_max_supression(bounding_boxes, iou_threshold, threshold, box_format='corners'):
    """
    Does Non Max Suppression given bounding_boxes

    Parameters:
        bounding_boxes (list): list of lists containing all bounding_boxes with each bounding_boxes
        specified as [class_pred, prob_score, x1, y1, x2, y2]
        iou_threshold (float): threshold where predicted bounding_boxes is correct
        threshold (float): threshold to remove predicted bounding_boxes (independent of IoU) 
        box_format (str): "midpoint" or "corners" used to specify bounding_boxes

    Returns:
        list: bounding_boxes after performing NMS given a specific IoU threshold
    """
    assert type(bounding_boxes)==list
    bounding_boxes = [box for box in bounding_boxes if box[1] > threshold]
    bounding_boxes = sorted(bounding_boxes, key=lambda x: x[1], reverse=True)
    bounding_boxes_after_nms = []
    
    while bounding_boxes:
        chosen_box = bounding_boxes.pop(0)
        bounding_boxes = [box for box in bounding_boxes 
                          if box[0] != chosen_box[0]
                          or intersection_over_union(torch.Tensor(chosen_box[2:]), 
                                                     torch.Tensor(box[2:]), 
                                                     box_format=box_format) < iou_threshold
                          ]
        bounding_boxes_after_nms.append(chosen_box)
    
    return bounding_boxes_after_nms