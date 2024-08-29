# QYtool

> A wrapped useful tool package designed for research purposes, tailored specifically for my own research needs.
> Author: Xuewen Zhang

If you have questions, remarks, technical issues etc. feel free to use the issues page of this repository. I am looking forward to your feedback and the discussion.

> Introduction: [link](https://github.com/QiYuan-Zhang/QYtool)
> 
> PyPI site: [link]()

---


## I. How to use

This package operates within the Python framework.

### 1. Required packages

- Numpy
- Torch
- Rich
- Wanbd
- CasADi &emsp; &emsp;     <-- 3 <= __version__ <= 4


### 2. Usage

- Download the [*QYtool*](./src/) file and save it to your project directory.

- Or install using pip

```
    pip install QYtool
```
Then you can use the deepctools in your python project.


### II. QYtool toolbox organization
```
. 
└── mytool
    ├── timer: give execution time of function 
    ├── datatool: for data process
    ├── dirtool: for directory operation
    ├── nntool: for neural networks, load model, save model, construct casadi model  
    ├── mathtool: for math operation
    ├── progressbar: an example to build your own custom progressbar
    └── new_wandb_proj: an example of using wandb
```

## Version update

#### **1.0.0**: initial commit

#### 1.0.1 - 1.0.6: under development with name: `mytool`

#### 1.0.7: published and changed name to `QYtool`


## License

This project is developed by `Xuewen Zhang` (xuewen.zhang741@outlook.com).

The project is released under the APACHE license. See [LICENSE](LICENSE) for details.