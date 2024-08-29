"""
Name: nntool.py
Author: Xuewen Zhang
Date:at 03/05/2024
version: 1.0.0
Description: my own toolbox for research projects
"""

import os
import torch
import numpy as np
import casadi as cs
from rich import print as rprint


class nntool():
    def __init__(self):
        """
            Neural network related tools
        """
        self.name = 'Xuewen'
        self.flags = {'initialize': False}


    def init(self, model):
        """ Initialize the model """
        self.model = model
        self.model_param = dict(self.model.named_parameters())
        self.model_param_name = list(self.model_param.keys())
        self.flags['initialize'] = True
        return
    
    
    def load_model(self, paramdir, device=torch.device('cpu'), model=None, checkpoint_name='nn_model'):
        """
            Load the saved model
            paramdir: the path of the saved model pt files
            device: the device to load the model, cpu or gpu {'cuda:0'}
            kwargs: the model parameters
        """
        checkpoint = torch.load(paramdir, map_location=device)
        if model is None:
            if not self.flags['initialize']:
                raise ValueError('Please initialize the nntool (self.init(model)) first if do not provide the model.')
            self.model.load_state_dict(checkpoint[checkpoint_name])
            model = self.model
        else:
            model.load_state_dict(checkpoint[checkpoint_name])
        rprint(":inbox_tray: Model loaded [green]successfully[/green].")
        return model
    

    def save_model(self, savedir, train_loss, val_loss, train_loss_all, val_loss_all, model=None):
        """
        Used for saving the best training model and validation model
        Args:
            model: the NN model
            train_loss: each train epoch loss
            val_loss:each validation epoch loss
        Returns: None
        """
        if model is None:
            if not self.flags['initialize']:
                raise ValueError('Please initialize the nntool (self.init(model)) first if do not provide the model.')
            model = self.model
        # Validation sets are used to decide the parameters of the model
        train_min = np.min(train_loss_all)
        val_min = np.min(val_loss_all)

        # saves model weights if loss is the lowest ever
        if val_loss <= val_min:
            torch.save({"nn_model": model.state_dict()}, savedir+'val_model.pt')
        if train_loss <= train_min:
            torch.save({"nn_model": model.state_dict()}, savedir+'train_model.pt')
        return


    def save_parameters(self, savedir, model=None):
        """
            Save model parameters
            model: neural network model
            savedir: save path for parameters
        """
        if model is None:
            if not self.flags['initialize']:
                raise ValueError('Please initialize the nntool (self.init(model)) first if do not provide the model.')
            model = self.model
            model_param = self.model_param
        else:
            model_param = dict(model.named_parameters())
        
        if not os.path.exists(savedir):
            os.makedirs(savedir)

        for name, value in model_param.items():
            np.savetxt(savedir + '{}.txt'.format(name), value.detach().numpy())
        rprint(':page_facing_up: Model parameters saved as TXTs [green]successfully[/green].')
        return


    def model_casadi(self, input_dim, activation_fcn=None, model=None):
        """
            Construct the well-trained model using casadi and wrap it as a casadi Function for control optimization
            May need to change the structure according to the specific task
            input_dim: the dimension of the input layer
            activation_fcn: 'relu', 'tanh', if None, then no activation functions
            return: self.model_cas a function   output = self.model_cas(input)
        """
        if model is None:
            if not self.flags['initialize']:
                raise ValueError('Please initialize the nntool (self.init(model)) first if do not provide the model.')
            model_param = self.model_param
            model_param_name = self.model_param_name
        else:
            model_param = dict(model.named_parameters())
            model_param_name = list(model_param.keys())
            
        input_var = cs.SX.sym('input', input_dim)
        layer_num = int(len(self.model_param_name)/2)

        inputs = input_var
        for i in range(layer_num):
            fc_weight = np.array(model_param[model_param_name[i]].detach().numpy())
            fc_bias = np.array(model_param[model_param_name[i+1]].detach().numpy())
            output = cs.mtimes(fc_weight, input) + fc_bias
            if i != layer_num-1:                        # last layer no activation function
                if activation_fcn == 'relu':            # different activation functions
                    output = cs.fmax(output)
                elif activation_fcn == 'tanh':
                    output = cs.tanh(output)
            inputs = output                              # update input for the next layer

        # Create casadi function
        self.model_cas = cs.Function('model', [input_var], [output])
        return self.model_cas
    

    





