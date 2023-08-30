import torch

def intersection_over_union(boxes_preds, boxes_labels, box_format="midpoint"):
    # boxes_labels and boxes_preds shape is (N, 4) where N is the number of bounding boxes
    
    # When given midpoint box format, we need to convert it to corners
    # Like for YOLO algorithm which would have (N, S, S, 4) in shape
    if box_format=='midpoint':
        # Coordinates for the first box
        box1_x1 = boxes_preds[..., 0:1] - boxes_preds[..., 2:3] / 2
        box1_y1 = boxes_preds[..., 1:2] - boxes_preds[..., 3:4] / 2
        box1_x2 = boxes_preds[..., 0:1] + boxes_preds[..., 2:3] / 2
        box1_y2 = boxes_preds[..., 1:2] + boxes_preds[..., 3:4] / 2
        
        # Coordinates for the second box
        box2_x1 = boxes_labels[..., 0:1] - boxes_labels[..., 2:3] / 2
        box2_y1 = boxes_labels[..., 1:2] - boxes_labels[..., 3:4] / 2
        box2_x2 = boxes_labels[..., 0:1] + boxes_labels[..., 2:3] / 2
        box2_y2 = boxes_labels[..., 1:2] + boxes_labels[..., 3:4] / 2
    
    elif box_format=='corners':
        # Coordinates for the first box
        box1_x1 = boxes_preds[..., 0:1] # (N, 1)
        box1_y1 = boxes_preds[..., 1:2]
        box1_x2 = boxes_preds[..., 2:3]
        box1_y2 = boxes_preds[..., 3:4]

        # Coordinates for the second box
        box2_x1 = boxes_labels[..., 0:1]
        box2_y1 = boxes_labels[..., 1:2]
        box2_x2 = boxes_labels[..., 2:3]
        box2_y2 = boxes_labels[..., 3:4]
    
    # Taking the intersection
    x1 = torch.max(box1_x1, box2_x1)
    y1 = torch.max(box1_y1, box2_y1)
    x2 = torch.min(box1_x2, box2_x2)
    y2 = torch.min(box1_y2, box2_y2)
    
    # clamp(0) is for the case when they do not intersect
    intersection = (x2-x1).clamp(0) * (y2-y1).clamp(0)
    
    # Calculating the union for the boxes
    box1_area = abs((box1_x2 - box1_x1) * (box1_y1 - box1_y2))
    box2_area = abs((box2_x1 - box2_x2) * (box2_y1 - box2_y2))
    union = box1_area + box2_area - intersection + 1e-6 # For numerical stability
    
    return intersection / union
    
    
    
    