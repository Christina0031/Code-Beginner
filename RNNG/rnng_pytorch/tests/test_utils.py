import textwrap             # textwrap模块

from nltk.tree import Tree
import pytest

from rnng.utils import add_dummy_pos, get_evalb_f1, id2parsetree


id2nonterm = 'S NP VP'.split()
id2word = 'John loves Mary'.split()


def test_id2parsetree():    # id2parsetree 通过位序生成树
    tree = Tree(0, [    #S
        Tree(1, [0]),   #NP John
        Tree(2, [1, Tree(1, [2])])  #VP loves NP Mary 
    ])
    expected = '(S (NP John) (VP loves (NP Mary)))'

    assert str(id2parsetree(tree, id2nonterm, id2word)) == expected


def test_add_dummy_pos():   # add_dummy_pos 添加虚拟词性？
    s = '(S (NP John) (VP loves (NP Mary)))'
    expected = '(S (NP (XX John)) (VP (XX loves) (NP (XX Mary))))'
    tree = Tree.fromstring(s)

    assert str(add_dummy_pos(tree)) == expected


def test_get_evalb_f1():    
    # textwrap.dedent 删除每一行中都存在的缩进
    evalb_output = textwrap.dedent("""
      Sent.                        Matched  Bracket   Cross        Correct Tag
    ID  Len.  Stat. Recal  Prec.  Bracket gold test Bracket Words  Tags Accracy
    ============================================================================
    1    3    0  100.00 100.00     4      4    4      0      3     0     0.00
    ============================================================================
                    100.00 100.00      4     4     4      0      3     0     0.00
    === Summary ===

    -- All --
    Number of sentence        =      1
    Number of Error sentence  =      0
    Number of Skip  sentence  =      0
    Number of Valid sentence  =      1
    Bracketing Recall         = 100.00
    Bracketing Precision      = 100.00
    Bracketing FMeasure       =  50.00
    Complete match            = 100.00
    Average crossing          =   0.00
    No crossing               = 100.00
    2 or less crossing        = 100.00
    Tagging accuracy          =   0.00

    -- len<=40 --
    Number of sentence        =      1
    Number of Error sentence  =      0
    Number of Skip  sentence  =      0
    Number of Valid sentence  =      1
    Bracketing Recall         = 100.00
    Bracketing Precision      = 100.00
    Bracketing FMeasure       = 100.00
    Complete match            = 100.00
    Average crossing          =   0.00
    No crossing               = 100.00
    2 or less crossing        = 100.00
    Tagging accuracy          =   0.00
    """)

    assert get_evalb_f1(evalb_output) == pytest.approx(50)  # pytest.approx 在一定误差内，两数字相等
