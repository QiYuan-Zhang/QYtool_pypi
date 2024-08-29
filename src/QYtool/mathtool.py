"""
Name: mathtool.py
Author: Xuewen Zhang
Date:at 28/04/2024
version: 1.0.0
Description: my own toolbox for research projects
"""

import numpy as np
import torch

class mathtool(object):
    def __init__(self):
        self.author = 'Xuewen Zhang'
        
        
    def hankel(self, L, datatype='array', *args):
            """
            Construct the Hankel matrix
                datatype (str): 'array' or 'tensor'
                args: x: data sequence (data_size, x_dim)
                L: row dimension of the hankel matrix
                T: data samples of data x
                return H(x): hankel matrix of x  H(x): (x_dim*L, T-L+1)
                H(x) = [x(0)   x(1) ... x(T-L)
                        x(1)   x(2) ... x(T-L+1)
                        .       .   .     .
                        .       .     .   .
                        .       .       . .
                        x(L-1) x(L) ... x(T-1)]
            """
            if datatype not in ['array', 'tensor']:
                raise ValueError(f"{datatype} not exist, datatype should be 'array' or 'tensor'.")

            hankeldata = []
            for x in args:
                T, x_dim = x.shape
                Hx = torch.zeros((L*x_dim, T-L+1), device=x.device) if datatype == 'tensor' else np.zeros((L*x_dim, T-L+1))
                for i in range(L):
                    Hx[i*x_dim:(i+1)*x_dim, :] = x[i:T-L+i+1, :].transpose(0, 1) if datatype == 'tensor' else x[i:T-L+i+1, :].transpose(1, 0)  # x need transpose to fit the hankel dimension
                hankeldata.append(Hx)
                
            if len(hankeldata) == 1:
                hankeldata = hankeldata[0]
            return hankeldata
        
        