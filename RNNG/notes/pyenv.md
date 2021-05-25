```
cd pytorch-rnng
conda activate py36

(py36) ji@U:~/pytorch-rnng$ python
>>> import torch  
>>> print(torch.__version__)
0.2.0_0

(py36) ji@U:~/pytorch-rnng$ pytest
```
typing.py修改为typing1.py 解决typing模块报错问题

```
运行：
run.py train -t /home/ji/pytorch-rnng/data/input/00/wsj_0001.mrg -s /home/ji/pytorch-rnng/data/output -d /home/ji/pytorch-rnng/data/working/01/wsj_0100.mrg --evalb /home/ji/pytorch-rnng/src/rnng/EVALB/./evalb --evalb-params /home/ji/pytorch-rnng/src/rnng/EVALB/new.prm

报错：
INFO - rnng.trainer - Setting random seed to 25122017
INFO - rnng.trainer - Preparing serialization directory in /home/ji/pytorch-rnng/data/output
INFO - rnng.trainer - Reading train corpus from /home/ji/pytorch-rnng/data/input/00/wsj_0001.mrg
INFO - rnng.trainer - Reading dev corpus from /home/ji/pytorch-rnng/data/working/01/wsj_0100.mrg
INFO - rnng.trainer - Building vocabularies
INFO - rnng.trainer - Found 5 words, 14 POS tags, 10 nonterminals, and 12 actions
INFO - rnng.trainer - Saving fields dict to /home/ji/pytorch-rnng/data/output/fields_dict.pkl
INFO - rnng.trainer - Building model
INFO - rnng.trainer - Saving model metadata to /home/ji/pytorch-rnng/data/output/model_metadata.json
INFO - rnng.trainer - Saving model parameters to /home/ji/pytorch-rnng/data/output/model_params.pth
1 : Length unmatch (15|18)
2 : Length unmatch (11|13)
INFO - rnng.trainer - Epoch 1 done (1.7199s): 6.66 samples/sec | loss 63.6487 | F1 nan
INFO - rnng.trainer - Saving model parameters to /home/ji/pytorch-rnng/data/output/model_params.pth
1 : Length unmatch (20|22)
2 : Length unmatch (12|13)
3 : Length unmatch (29|31)
4 : Length unmatch (33|36)
5 : Length unmatch (20|22)
6 : Length unmatch (16|18)
7 : Length unmatch (18|20)
8 : Length unmatch (32|35)
9 : Length unmatch (34|36)
10 : Length unmatch (36|39)
11 : Length unmatch (30|34)
12 : Length unmatch (10|12)
Traceback (most recent call last):
  File "/home/ji/pytorch-rnng/src/rnng/run.py", line 17, in <module>
    args.func(args)
  File "/home/ji/pytorch-rnng/src/rnng/commands/train.py", line 83, in main
    trainer.run()
  File "/home/ji/pytorch-rnng/src/rnng/trainer.py", line 192, in run
    self.network, self.train_iterator, self.max_epochs, self.optimizer)
  File "/home/ji/anaconda3/envs/py36/lib/python3.6/site-packages/torchnet/engine/engine.py", line 67, in train
    self.hook('on_end_epoch', state)
  File "/home/ji/anaconda3/envs/py36/lib/python3.6/site-packages/torchnet/engine/engine.py", line 31, in hook
    self.hooks[name](state)
  File "/home/ji/pytorch-rnng/src/rnng/trainer.py", line 259, in on_end_epoch
    f1_score = self.compute_f1()
  File "/home/ji/pytorch-rnng/src/rnng/trainer.py", line 308, in compute_f1
    return get_evalb_f1(res.stdout)
  File "/home/ji/pytorch-rnng/src/rnng/utils.py", line 13, in get_evalb_f1
    line = next(lines)
StopIteration

Process finished with exit code 1
```

