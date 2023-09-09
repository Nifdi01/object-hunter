import torch
from torch import nn
from metrics.iou import intersection_over_union

class YoloLoss(nn.Module):
    def __init__(self, S=7, B=2, C=20):
        """
        Initialize the YOLOv1 loss function.

        Args:
            S (int): Number of grid cells along one side of the image grid.
            B (int): Number of bounding boxes predicted by each grid cell.
            C (int): Number of classes to be predicted.
        """
        super(YoloLoss, self).__init__()
        self.mse = nn.MSELoss(reduction='sum')
        self.S = S
        self.B = B
        self.C = C
        self.lambda_noobj = 0.5  # Weight for the no object loss.
        self.lambda_coord = 5.0  # Weight for the coordinate loss.

    def forward(self, predictions, target):
        """
        Forward pass of the YOLOv1 loss function.

        Args:
            predictions (torch.Tensor): Predictions made by the YOLOv1 model.
            target (torch.Tensor): Ground truth target values.

        Returns:
            torch.Tensor: Total loss computed based on the predictions and targets.
        """
        predictions = predictions.reshape(-1, self.S*self.S, self.C+self.B*5)  # Reshape predictions tensor.

        # Calculate Intersection over Union (IoU) for bounding boxes.
        iou_b1 = intersection_over_union(predictions[...,21:25], target[...,21:25])
        iou_b2 = intersection_over_union(predictions[...,26:30], target[..., 21:25])
        ious = torch.cat([iou_b1.unsqueeze(0), iou_b2.unsqueeze(1)], dim=0)
        iou_maxes, bestbox = torch.max(ious, dim=0)

        exists_box = target[..., 20].unsqueeze(3)  # Identity of object i

        # BOX COORDINATE LOSS
        box_predictions = exists_box * (bestbox * predictions[..., 26:30] + (1-bestbox) * predictions[..., 21:25])
        box_targets = exists_box * target[..., 21:25]

        # Apply a transformation to ensure the square root of width and height predictions is positive.
        box_predictions[..., 2:4] = torch.sign(box_predictions[..., 2:4]) * torch.sqrt(torch.abs(box_predictions[..., 2:4]) + 1e-6)
        box_targets[..., 2:4] = torch.sqrt(box_targets[..., 2:4])

        box_loss = self.mse(torch.flatten(box_predictions, end_dim=-2), torch.flatten(box_targets, end_dim=-2))

        # OBJECT LOSS
        pred_box = (bestbox * predictions[..., 25:26] + (1-bestbox) * predictions[...,20:21])
        object_loss = self.mse(torch.flatten(exists_box * pred_box), torch.flatten(exists_box * target[..., 20:21]))

        # NO OBJECT LOSS
        no_object_loss = self.mse(torch.flatten((1-exists_box) * predictions[...,20:21], start_dim=1), torch.flatten((1-exists_box) * target[..., 20:21], start_dim=1))
        no_object_loss += self.mse(torch.flatten((1-exists_box) * predictions[...,25:26], start_dim=1), torch.flatten((1-exists_box) * target[..., 20:21], start_dim=1))

        # FOR CLASS LOSS
        class_loss = self.mse(torch.flatten(exists_box * predictions[...,:20], end_dim=-2), torch.flatten(exists_box * target[...,:20], end_dim=-2))

        # Compute the total loss
        loss = self.lambda_coord * box_loss + object_loss + self.lambda_noobj * no_object_loss + class_loss

        return loss
