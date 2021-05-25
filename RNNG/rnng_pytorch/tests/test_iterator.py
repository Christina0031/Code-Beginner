import random

from torch.autograd import Variable
from torchtext.data import Dataset, Example, Field
'''
torchtext.data.Example :    用来表示一个样本，数据+标签
torchtext.data.Datasets:    数据集类，__getitem__ 返回 Example实例
torchtext.data.Field :      用来定义字段的处理方法（文本字段，标签字段）。比如指定的分词方法，
                            是否转成小写，起始与结束字符，补全字符以及词典等等
torchtext.data.Iterator:    迭代器，用来生成 batch
                            返回模型所需要的处理后的数据
'''

from rnng.iterator import SimpleIterator


random.seed(12345)


class TestSimpleIterator(object):   # 测试迭代器
    TEXT = Field()  # 定义样本的处理操作 
    '''
        examples: List of Examples.
        fields (List(tuple(str, Field))): The Fields to use in this tuple. 
            The string is a field name, and the Field is the associated field.
    '''
    examples = [    # 从原始数据构造出Example的列表
        Example.fromlist(['John loves Mary'], [('text', TEXT)]),  # Example.fromlist( 句子, fields ),
        Example.fromlist(['Mary cries'], [('text', TEXT)]),
    ]
    dataset = Dataset(examples, [('text', TEXT)])   # Example列表构造DataSet
                                                    # data.Dataset(examples, fields)
    TEXT.build_vocab(dataset)                       # 为该Field创建Vocab

    def make_iterator(self):
        return SimpleIterator(self.dataset, device=-1)

    def test_init_minimal(self):
        iterator = SimpleIterator(self.dataset)
        assert iterator.dataset is self.dataset
        assert iterator.batch_size == 1
        assert iterator.train
        assert iterator.device is None
        assert iterator.sort_key is None
        assert not iterator.sort
        assert not iterator.repeat
        assert iterator.shuffle == iterator.train
        assert not iterator.sort_within_batch

    def test_init_full(self):
        iterator = SimpleIterator(self.dataset, train=False, device=-1)
        assert not iterator.train
        assert iterator.device == -1

    def test_next(self):
        iterator = self.make_iterator()      
        # 使用iter()函数把list，dict，str等Iterable转换为Iterator
        sample = next(iter(iterator))       #TODO

        assert isinstance(sample.text, Variable)    # 是否为Variable类
        assert sample.text.size(1) == 1             #TODO


'''
Field参数说明

sequential: 是否把数据表示成序列，如果是False, 不能使用分词 默认值: True.
use_vocab: 是否使用词典对象. 如果是False 数据的类型必须已经是数值类型. 默认值: True.
init_token: 每一条数据的起始字符 默认值: None.
eos_token: 每条数据的结尾字符 默认值: None.
fix_length: 修改每条数据的长度为该值，不够的用pad_token补全. 默认值: None.
tensor_type: 把数据转换成的tensor类型 默认值: torch.LongTensor.
preprocessing:在分词之后和数值化之前使用的管道 默认值: None.
postprocessing: 数值化之后和转化成tensor之前使用的管道默认值: None.
lower: 是否把数据转化为小写 默认值: False.
tokenize: 分词函数. 默认值: str.split.
include_lengths: 是否返回一个已经补全的最小batch的元组和和一个包含每条数据长度的列表 . 默认值: False.
batch_first: Whether to produce tensors with the batch dimension first. 默认值: False.
pad_token: 用于补全的字符. 默认值: “”.
unk_token: 不存在词典里的字符. 默认值: “”.
pad_first: 是否补全第一个字符. 默认值: False.
'''