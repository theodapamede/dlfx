from torch.utils.data import DataLoader
from utils.MedSigLIPDataset import MedSigLIPDataset

def get_dataloader(input_df, config):
    """
    Create train, validation, and test dataloaders from input dataframe.
    
    Args:
        input_df: DataFrame containing image paths, labels, and split information
        config: Configuration object containing img_base_path, labels, and batch_size
    
    Returns:
        tuple: (train_dataloader, valid_dataloader, test_dataloader)
    """
    # Prepare training data
    train_df = input_df[input_df.Split == 'Train'].reset_index(drop=True)#.iloc[0:1000]
    train_img_path = list(config.img_base_path + train_df.ImagePath)
    train_img_label = list(train_df[config.labels].values)
    
    # Prepare validation data
    valid_df = input_df[input_df.Split == 'Valid'].reset_index(drop=True)#.iloc[0:100]
    valid_img_path = list(config.img_base_path + valid_df.ImagePath)
    valid_img_label = list(valid_df[config.labels].values)
    
    # Prepare test data
    test_df = input_df[input_df.Split == 'Test'].reset_index(drop=True)
    test_img_path = list(config.img_base_path + test_df.ImagePath)
    test_img_label = list(test_df[config.labels].values)
    
    # Create datasets
    train_dataset = MedSigLIPDataset(image_paths=train_img_path, labels=train_img_label)
    valid_dataset = MedSigLIPDataset(image_paths=valid_img_path, labels=valid_img_label)
    test_dataset = MedSigLIPDataset(image_paths=test_img_path, labels=test_img_label)
    
    # Create DataLoaders
    train_dataloader = DataLoader(
        train_dataset, 
        batch_size=config.batch_size, 
        shuffle=True, 
        pin_memory=True, 
        num_workers=config.num_workers
    )
    valid_dataloader = DataLoader(
        valid_dataset, 
        batch_size=config.batch_size, 
        shuffle=False, 
        pin_memory=True, 
        num_workers=config.num_workers
    )
    test_dataloader = DataLoader(
        test_dataset, 
        batch_size=config.batch_size, 
        shuffle=False, 
        pin_memory=True, 
        num_workers=config.num_workers
    )
    
    return train_dataloader, valid_dataloader, test_dataloader

# Usage:
#train_dataloader, valid_dataloader, test_dataloader = get_dataloader(input_df, config)