from typing import Optional

from torchtext.data import Dataset, Iterator


class SimpleIterator(Iterator):
    def __init__(self,
                 dataset: Dataset,
                 train: bool = True,
                 device: Optional[int] = None) -> None:
        super().__init__(dataset, 1, train=train, repeat=False, sort=False, device=device)


'''
dataset: 加载的数据集
batch_size: Batch 大小.
batch_size_fn: 产生动态的batch大小的函数
sort_key: 排序的key
train: 是否是一个训练集
repeat: 是否在不同epoch中重复迭代
shuffle: 是否打乱数据
sort: 是否对数据进行排序
sort_within_batch: batch内部是否排序
device: 建立batch的设备 -1:CPU ；0,1 …：对应的GPU
'''