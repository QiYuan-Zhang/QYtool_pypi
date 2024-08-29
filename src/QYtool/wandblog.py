"""
Name: log.py
Author: Xuewen Zhang
Date:at 03/05/2024
version: 1.0.0
Description: my own toolbox for research projects
"""

import wandb
import time

def new_wandb_proj(project_name, exp_name=time.strftime('%y%m%d'), config=None, project_notes=''):
    """
    Create a new project on wandb
    Args:
        project_name (str): the name of the project
        config (dict): the configuration of the project inculding the hyperparameters like {'lr': 0.01, 'batch_size': 32}
        project_notes (str): the description of the project
    Returns: None
    """
    wandb.init(project=project_name, name=exp_name, notes=project_notes, config=config)
    ## then use wandb.log() to log the data
    # wandb.log({'loss': 0.5, 'accuracy': 0.9})
    # ytable = wandb.Table(data=y_dpc, columns=['y' + str(i) for i in range(self.y_dim)])
    # wandb.log({'ytable': ytable})
    # yu_img = wandb.Image(fig1, caption='yu_deepc')
    # wandb.log({'yu_deepc': yu_img})
    return