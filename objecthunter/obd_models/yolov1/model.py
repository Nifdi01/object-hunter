import torch
import torch.nn as nn

# Define the architecture configuration for the YOLOv1 model
architecture_config = [
    # tuple = (kernel size, number of filters of output, stride, padding)
    (7, 64, 2, 3),
    "M",  # max-pooling 2x2 stride = 2
    (3, 192, 1, 1),
    "M",  # max-pooling 2x2 stride = 2
    (1, 128, 1, 0),
    (3, 256, 1, 1),
    (1, 256, 1, 0),
    (3, 512, 1, 1),
    "M",  # max-pooling 2x2 stride = 2
    # [tuple, tuple, repeat times]
    [(1, 256, 1, 0), (3, 512, 1, 1), 4],
    (1, 512, 1, 0),
    (3, 1024, 1, 1),
    "M",  # max-pooling 2x2 stride = 2
    # [tuple, tuple, repeat times]
    [(1, 512, 1, 0), (3, 1024, 1, 1), 2],
    (3, 1024, 1, 1),
    (3, 1024, 2, 1),
    (3, 1024, 1, 1),
    (3, 1024, 1, 1),
]

# Define a CNN block
class CNNBlock(nn.Module):
    """
    A building block for the YOLOv1 architecture.

    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        **kwargs: Additional arguments for the convolutional layer.

    Attributes:
        conv (nn.Conv2d): Convolutional layer.
        batchnorm (nn.BatchNorm2d): Batch normalization layer.
        leakyrelu (nn.LeakyReLU): Leaky ReLU activation function.
    """

    def __init__(self, in_channels, out_channels, **kwargs):
        super(CNNBlock, self).__init__()
        self.conv = nn.Conv2d(in_channels, out_channels, bias=False, **kwargs)
        self.batchnorm = nn.BatchNorm2d(out_channels)
        self.leakyrelu = nn.LeakyReLU(0.1)

    def forward(self, x):
        """
        Forward pass through the CNNBlock.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor after convolution, batch normalization, and activation.
        """
        x = self.conv(x)
        x = self.batchnorm(x)
        x = self.leakyrelu(x)
        return x

# Define the YOLOv1 model
class Yolov1(nn.Module):
    """
    YOLOv1 (You Only Look Once) model for object detection.

    Args:
        in_channels (int, optional): Number of input channels (default is 3 for RGB images).
        **kwargs: Additional keyword arguments.

    Attributes:
        architecture (list): YOLOv1 architecture configuration.
        in_channels (int): Number of input channels.
        darknet (nn.Sequential): Darknet convolutional layers.
        fcs (nn.Sequential): Fully connected layers for predictions.
    """

    def __init__(self, in_channels=3, **kwargs):
        super(Yolov1, self).__init__()
        self.architecture = architecture_config
        self.in_channels = in_channels
        self.darknet = self._create_conv_layers(self.architecture)
        self.fcs = self._create_fcs(**kwargs)

    def forward(self, x):
        """
        Forward pass through the YOLOv1 model.

        Args:
            x (torch.Tensor): Input tensor.

        Returns:
            torch.Tensor: Output tensor containing object detection predictions.
        """
        x = self.darknet(x)
        x = torch.flatten(x, start_dim=1)
        x = self.fcs(x)
        return x

    def _create_conv_layers(self, architecture):
        """
        Create convolutional layers based on the given architecture configuration.

        Args:
            architecture (list): YOLOv1 architecture configuration.

        Returns:
            nn.Sequential: Sequential module containing the convolutional layers.
        """
        layers = []
        in_channels = self.in_channels

        for x in architecture:
            if type(x) == tuple:
                layers += [
                    CNNBlock(
                        in_channels, x[1], kernel_size=x[0], stride=x[2], padding=x[3],
                    )
                ]

                in_channels = x[1]

            elif type(x) == str:
                layers += [nn.MaxPool2d(kernel_size=2, stride=2)]

            elif type(x) == list:
                conv1 = x[0]  # tuple
                conv2 = x[1]  # tuple
                num_repeats = x[2]  # integer

                for _ in range(num_repeats):
                    layers += [
                        CNNBlock(
                            in_channels,
                            conv1[1],
                            kernel_size=conv1[0],
                            stride=conv1[2],
                            padding=conv1[3],
                        )
                    ]

                    layers += [
                        CNNBlock(
                            conv1[1],
                            conv2[1],
                            kernel_size=conv2[0],
                            stride=conv2[2],
                            padding=conv2[3],
                        )
                    ]

                    in_channels = conv2[1]

        return nn.Sequential(*layers)

    def _create_fcs(self, split_size, num_boxes, num_classes):
        """
        Create fully connected layers for object detection predictions.

        Args:
            split_size (int): Size of the split grid.
            num_boxes (int): Number of bounding boxes per grid cell.
            num_classes (int): Number of object classes.

        Returns:
            nn.Sequential: Sequential module containing fully connected layers.
        """
        S, B, C = split_size, num_boxes, num_classes
        return nn.Sequential(
            nn.Flatten(),
            nn.Linear(1024 * S * S, 4096),
            nn.Dropout(0.5),
            nn.LeakyReLU(0.1),
            nn.Linear(4096, S * S * (C + B * 5)),  # (S,S,30)
        )
