"""
Name: datatool.py
Author: Xuewen Zhang
Date:at 28/04/2024
version: 1.0.0
Description: my own toolbox for research projects
"""

import os
import time
import json
import torch
import numpy as np
import casadi as cs
from rich import print as rprint


class datatool(object):
    def __init__(self):
        self.author = 'Xuewen Zhang'
        self.scale_tracker_reset()
        
        
    ## ---------------------- Data processing ---------------------- ##    
    # Change data type or device
    def toArray(self, *args):
        """Turn data to array"""
        data_list = []
        for data in args:
            if isinstance(data, np.ndarray):
                data_list.append(data)
            else:
                data_list.append(np.array(data))
        if len(data_list) == 1:
            data_list = data_list[0]
        return data_list


    def toList(self, *args):
        """Convert NumPy arrays/Torch tensors to Python lists"""
        data = []
        for x in args:
            if isinstance(x, list):
                data.append(x)
            else:
                data.append(x.tolist())
        if len(data) == 1:
            data = data[0]
        return data


    def toTorch(self, *args):
        """Turn data to array"""
        data_list = []
        for data in args:
            if isinstance(data, torch.Tensor):
                data_list.append(data)
            else:
                data_list.append(torch.FloatTensor(data))
        if len(data_list) == 1:
            data_list = data_list[0]
        return data_list


    def toDevice(self, device=None, *args):
        data_all = []
        if device is None:
            device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        for data in args:
            if torch.is_tensor(data):
                data = data.to(device)
            else:
                raise ValueError("Data/model is not torch type.")
            data_all.append(data)
        if len(data_all) == 1:
            data_all = data_all[0]
        return data_all
    
    
    # data scale
    def _scale_tracker(self, idx, value):
        """ Track if the idx and value shows up before """
        value_tuple = tuple(value)
        
        if (tuple(idx), value_tuple) in self.scale_track_dict:
            # If the data has been seen before, return 1
            return True
        else:
            # If the data has not been seen before, add it to the dictionary and return 0
            self.scale_track_dict[(tuple(idx), value_tuple)] = True
            return False
        
        
    def scale_tracker_reset(self):
        """ Reset the scale tracker """
        self.scale_track_dict = {}
        return
            
        
    def scale(self, sc1, sc2, method='minmax', datatype='array', *args):
        """
            Scale the data using 'minmax' or 'norm' methods
        Args:
            sc1 (array or tensor)(1, dim) or (dim,): if minmax, sc1 is the min value of x; if norm, sc1 is the mean value of x
            sc2 (array or tensor)(1, dim) or (dim,): if minmax, sc2 is the max value of x; if norm, sc2 is the std value of x
            method (str, optional): scale methods. Defaults to 'minmax', including 'minmax' and 'norm'.
            datatype (str, optional): data type. Defaults to 'array', including 'array' and 'tensor'.
            args: contains data x (array or tensor)(1, dim) or (dim,): original data
        Returns:
            x_ (array or tensor)(1, dim) or (dim,): scaled data
        """
        datatype_dict = {'array', 'tensor'}
        method_dict = {'minmax', 'norm'}
        self.checkarg([datatype, datatype_dict], [method, method_dict])

        data_scale  = []
        i = 0
        for x in args:
            i += 1
            if method == 'minmax':
                x_ = (x - sc1)/(sc2 - sc1)
                # check if have x_max - x_min == 0, if have, replace to zeros
                zero_idx, zero_dim = self.find0idx(datatype, sc2 - sc1)
                if len(zero_idx) != 0:
                    if zero_dim == 0:
                        x_[zero_idx] = 0 
                    else:
                        x_[:, zero_idx] = 0
                    constant_value = x[zero_idx] if zero_dim == 0 else x[0, zero_idx]
                    
                    if not self._scale_tracker(zero_idx, constant_value):
                        # only print once for the same constant value
                        rprint(f"[red] :warning: [cyan]'{i}'[/cyan] input data have constant value, index: [cyan]'{zero_idx}'[/cyan]: value: [cyan]{constant_value}[/cyan], replaced to [cyan]'0'[/cyan].")
            elif method == 'norm':
                x_ = (x - sc1)/sc2
            data_scale.append(x_)
            
        if len(data_scale) == 1:
            data_scale = data_scale[0]
        return data_scale
    
    
    def unscale(self, sc1, sc2, method='minmax', datatype='array', *args):
        """
            Unscale the data using 'minmax' or 'norm' methods
        Args:
            sc1 (array or tensor)(1, dim) or (dim,): if minmax, sc1 is the min value of x; if norm, sc1 is the mean value of x
            sc2 (array or tensor)(1, dim) or (dim,): if minmax, sc2 is the max value of x; if norm, sc2 is the std value of x
            method (str, optional): scale methods. Defaults to 'minmax', including 'minmax' and 'norm'.
            datatype (str, optional): data type. Defaults to 'array', including 'array' and 'tensor'.
            args: contains data x_ (array or tensor)(1, dim) or (dim,): scaled data
        Returns:
            x (array or tensor)(1, dim) or (dim,): unscaled data
        """
        datatype_dict = {'array', 'tensor'}
        method_dict = {'minmax', 'norm'}
        self.checkarg([datatype, datatype_dict], [method, method_dict])

        data = []
        i = 0
        for x_ in args:
            i += 1
            if method == 'minmax':
                x = x_ * (sc2 - sc1) + sc1
                # check if have x_max - x_min == 0, if have, replace to constant value
                zero_idx, zero_dim = self.find0idx(datatype, sc2 - sc1)
                if len(zero_idx) != 0:
                    constant_value = sc1[zero_idx] if zero_dim == 0 else sc1[:, zero_idx]
                    constant_value_slice = constant_value.copy() if zero_dim == 0 else constant_value[0].copy()
                    if zero_dim == 0:
                        x[zero_idx] = constant_value  
                    else:
                        x[:, zero_idx] = constant_value
                    if not self._scale_tracker(zero_idx, constant_value_slice):
                        # only print once for the same constant value
                        rprint(f"[red] :warning: [cyan]'{i}'[/cyan] input data have constant value, index: [cyan]'{zero_idx}'[/cyan]: unscale to constant value: [cyan]{constant_value_slice}[/cyan].")
            elif method == 'norm':
                x = x_ * sc2 + sc1
            data.append(x)
            
        if len(data) == 1:
            data = data[0]
        return data
    

    # other utils
    def mse(self, data1, data2):
        """Compute mse of data1 and data2"""
        if data1.shape != data2.shape:
            raise ValueError(f'data1 shape {data1.shape} != data2 shape {data2.shape}')
        else:
            mse = np.linalg.norm(data1 - data2, ord=2)  # 2 norm
        return mse
    
    
    def data_to_step(self, t=None, *args):
        """
            Transform the sequential data to step data
            args: x (data_size, x_dim): used for the sequential data such as control inputs
            t (data_size): specially for time data
        """ 
        data = []
        for x in args:
            x = x.T
            dim, n = x.shape
            x_step = np.zeros((dim, 2*n))

            for i in range(n):
                x_step[:, 2 * i] = x[:, i]
                x_step[:, 2 * i + 1] = x[:, i]
            
            data.append(x_step.T)

        if len(data) == 1:
            data = data[0]
        
        if t is not None:
            t_step = np.zeros(2*len(t))
            for i in range(len(t)):
                t_step[2 * i] = t[i]
                t_step[2 * i + 1] = t[i]
            ts = t[1]-t[0]
            t_step = t_step[1:]
            t_step = np.concatenate((t_step, np.array([t_step[-1] + ts])))
            return t_step, data 
        else:
            return data

    
    def checkarg(self, *args):
        """
            Check if the function inputs are in the feasible sets
        Args:
            args (list|[variable, variable_dict]): values of different variable inputs and feasible sets.
        """
        for [variable, feasible_dict] in args:
            if variable not in feasible_dict:
                raise ValueError(f"Input {variable} is not supported, should be {feasible_dict}.")
    
    
    def find0idx(self, datatype='array', *args):
        """
            Find the zeros index of the data x.
        Args: 
            args: x (array or tensor)(1, dim) or (dim,): data
            datatype (str, optional): data type. Defaults to 'array', including 'array' and 'tensor'.
        Returns:
            zero_idx (list): zeros index
        """
        datatype_dict = {'array', 'tensor'}
        self.checkarg([datatype, datatype_dict])
        
        if datatype == 'array':
            where = np.where
        elif datatype == 'tensor':
            where = torch.where
        
        idx, dim = [], []
        for x in args:
            dim_size = len(x.shape)
            zero_dim = dim_size - 1
            zero_idx = where(x == 0)[zero_dim]
            idx.append(zero_idx)
            dim.append(zero_dim)
        if len(idx) == 1:
            idx = idx[0]
            dim = dim[0]
        return idx, dim

        
    
    ## ---------------------- Load data ---------------------- ##
    def loadtxt(self, loaddir, *args):
        data = []
        for name in args:
            data.append(np.loadtxt(loaddir + '%s.txt' % name))
        if len(data) == 1:
            data = data[0]
        return data
    

    def loadpt(self, loaddir, device=torch.device('cpu'), *args):
        """
            Load pt files using torch
            loaddir: save path
            device: cpu or gpu, {'cuda:0'}
            *args: file name in string
        """
        data = []
        for name in args:
            data.append(torch.load(loaddir + '%s.pt' % name, map_location=device))
        if len(data) == 1:
            data = data[0]
        return data


    def load_config(self, savedir='', *args):
        """args: the str of the load josn file name"""
        data_list = []
        for name in args:
            config = open(savedir + '%s.json' % name)
            data = json.load(config)
            data_list.append(data)
        if len(data_list) == 1:
            data_list = data_list[0]
        return data_list


    ## ---------------------- Save data ---------------------- ##
    def savetxt(self, savedir, **kwargs):
        """Save the data into txt files"""
        for name, item in kwargs.items():
            if isinstance(item, torch.Tensor):
                item = self.toArray(item.cpu())
            if isinstance(item, list):
                item = self.toArray(item)
            if item.ndim == 0:
                item = np.array([item])
            np.savetxt(savedir + '%s.txt' % name, item)


    def save_datatoconfig(self, save_dir='', **kwargs):
        """Write the dict into txt"""
        for name, data in kwargs.items():
            file = open(save_dir + '%s.json' % name, 'w')
            file.write('{\n')

            count = 0

            for key, value in data.items():
                count += 1
                if count != len(data.keys()):
                    file.write(f'"{key}": {value},\n')
                else:
                    file.write(f'"{key}": {value}\n')

            file.write('}\n')
            file.close()


    def save_config(self, args, savedir, name):
        """Save the config into json file"""
        json_dir_val = os.path.join(savedir, "{}.json".format(name))
        with open(json_dir_val, 'w') as fp:
            json.dump(args, fp, indent=4, default=self.toList)


    def add_line_to_file(self, file_path, line):
        """Add one line sentence to certain txt"""
        with open(file_path, 'a') as f:
            f.write(line + '\n')
            
            
    def save_model(self, model, savedir, train_loss, train_loss_all, val_loss=None, val_loss_all=None):
        """
        Used for saving the best training model and validation model
        Args:
            model: the NN model
            train_loss: each train epoch loss
            val_loss:each validation epoch loss
        Returns: None
        """
        # saves model weights if loss is the lowest ever
        train_min = np.min(train_loss_all)
        if train_loss <= train_min:
            torch.save({"nn_model": model.state_dict()}, savedir+'train_model.pt')
        
        if val_loss is not None and val_loss_all is not None:
            val_min = np.min(val_loss_all)
            if val_loss <= val_min:
                torch.save({"nn_model": model.state_dict()}, savedir+'val_model.pt')
                
                

