import torch 
import torch.nn as nn 
import torch.nn.functional as F

from torch.nn import Module 
import typing 

def _make_trainable(module: Module) -> None:
    """ Unfreezes a given module
    
    Arg:
        module: Module which you want to unfreeze 
    """
    for param in module.parameters():
        param.requires_grad = True
    module.train()

def _recursive_freeze(module : Module, 
        train_bn : bool =True) -> None:
    """ Layers freezer to make some layers nontrainable
        Args:
            module: Module which you want to freeze 
            train_bn: If you want Batch Norm to be trainable or not 
    """
    #Get list of model layers 
    children = list(module.children())
    if not children:
        if not (isinstance(module, BN_TYPES) and train_bn):
            for param in module.parameters():
                param.requires_grad = False
            module.eval()
        else:

            _make_trainable(module)
    else:
        for child in children:
            _recursive_freeze(module = child, train_bn = train_bn)


def freeze(module : Module, n: Optional[int] =  None, train_bn: bool = True) -> None:
    """

    :param module:  Module to freeze
    :param n:  max freeze depth
    :param train_bn:  if True, train on bn
    :return:
    """

    children = list(module.children())
    n_max = len(children) if n is None else n


    for child in children[:n_max]:
        _recursive_freeze(module = child, train_bn = train_bn)

    for child in children[nmax:]:
        _make_trainable(module=child)



def predefined_transform() -> None:
    """
    Example from docs
    https://github.com/albumentations-team/albumentations_examples/blob/master/notebooks/example.ipynb
    :return:
    """

    return A.Compose([
        A.RandomRotate90(),
        A.Flip(),
        A.Transpose(),
        A.OneOf([
            A.IAAAdditiveGaussianNoise(),
            A.GaussNoise(),
        ], p=0.2),
        A.OneOf([
            A.MotionBlur(p=.2),
            A.MedianBlur(blur_limit=3, p=0.1),
            A.Blur(blur_limit=3, p=0.1),
        ], p=0.2),
        A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2),
        A.OneOf([
            A.OpticalDistortion(p=0.3),
            A.GridDistortion(p=.1),
            A.IAAPiecewiseAffine(p=0.3),
        ], p=0.2),
        A.OneOf([
            A.CLAHE(clip_limit=2),
            A.IAASharpen(),
            A.IAAEmboss(),
            A.RandomBrightnessContrast(),            
        ], p=0.3),
        A.HueSaturationValue(p=0.3),
    ])







