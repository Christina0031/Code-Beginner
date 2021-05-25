from nltk.tree import Tree


def add_dummy_pos(tree):    # add_dummy_pos 添加虚拟词性？
    if not isinstance(tree, Tree):
        return Tree('XX', [tree])
    return Tree(tree.label(), [add_dummy_pos(t) for t in tree])


def get_evalb_f1(evalb_output):
    lines = reversed(evalb_output.strip().split('\n'))
    for i in range(20):
        line = next(lines)
    return float(line.split()[-1])


def id2parsetree(tree, id2nonterm, id2word):    # id2parsetree 通过位序生成树
    if not isinstance(tree, Tree):
        return id2word[tree]
    children = [id2parsetree(t, id2nonterm, id2word) for t in tree]
    return Tree(id2nonterm[tree.label()], children)    # label()是当前树木根结点的值