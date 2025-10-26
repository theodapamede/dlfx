import torch
from torch.utils.data import Dataset
from typing import List, Optional, Union
from utils.preprocess import convert_to_8bit_3channel
from transformers import AutoProcessor
from PIL import Image

class MedSigLIPDataset(Dataset):
    """
    PyTorch Dataset for SigLIP model preprocessing.
    Handles image loading and preprocessing using the SigLIP processor.
    """
    
    def __init__(
        self, 
        image_paths: List[str], 
        labels: Optional[List] = None,
        processor_name: str = "google/medsiglip-448",
        max_length: Optional[int] = None
    ):
        """
        Initialize the dataset with image paths and optional labels.
        
        Args:
            image_paths: List of paths to medical image files
            labels: Optional list of labels corresponding to images
            processor_name: HuggingFace model identifier for the processor
            max_length: Maximum sequence length for padding (if needed)
        """
        self.image_paths = image_paths
        self.labels = labels
        self.processor = AutoProcessor.from_pretrained(processor_name)
        self.max_length = max_length
        
        # Validate that paths and labels match if labels provided
        if labels is not None and len(image_paths) != len(labels):
            raise ValueError("Number of image paths must match number of labels")
    
    def __len__(self):
        """Return the total number of images in the dataset."""
        return len(self.image_paths)
    
    def __getitem__(self, idx):
        """
        Load and preprocess a single medical image.
        
        Returns:
            Dict containing processed tensors, optional label, and file path
        """
        # Load the medical image at the specified index
        image_path = self.image_paths[idx]
        try:
            image = Image.open(image_path)
            # Convert grayscale medical images to RGB format for model compatibility
            image = convert_to_8bit_3channel(image)
        except Exception as e:
            raise RuntimeError(f"Error loading image {image_path}: {e}")
        
        # Prepare processor arguments for image preprocessing
        processor_kwargs = {
            "images": image,
            "padding": "max_length",  # Ensure consistent tensor sizes
            "return_tensors": "pt"    # Return PyTorch tensors
        }
        
        # Add max_length if specified (for text processing compatibility)
        if self.max_length is not None:
            processor_kwargs["max_length"] = self.max_length
            
        # Process the image through SigLIP processor
        inputs = self.processor(**processor_kwargs)
        
        # Remove batch dimension added by processor (DataLoader will add it back)
        processed_data = {
            key: tensor.squeeze(0) for key, tensor in inputs.items()
        }
        
        # Include label if available (for supervised learning tasks)
        if self.labels is not None:
            lbl = torch.tensor(self.labels[idx])
            if lbl.dim()==0:
                processed_data['label'] = torch.unsqueeze(lbl, -1)
            else:
                processed_data['label'] = lbl
        # Include file path for tracking and debugging
        processed_data['path'] = image_path
        
        return processed_data