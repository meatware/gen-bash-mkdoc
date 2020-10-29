"""Draws function callrelationships like unix "tree" command.

    from https://stackoverflow.com/questions/32151776/visualize-tree-in-bash-like-the-output-of-unix-tree
    >>> text='''apple: banana eggplant
    banana: cantaloupe durian
    eggplant:
    fig:'''
    >>> draw_tree(parser(text))
    ├─ apple
    |  ├─ banana
    |  |  ├─ cantaloupe
    |  |  └─ durian
    |  └─ eggplant
    └─ fig
"""

import sys
import logging
from functools import reduce

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

branch = "├"
pipe = "|"
end = "└"
dash = "─"


class Tree(object):
    def __init__(self, tag):
        self.tag = tag


class Node(Tree):
    def __init__(self, tag, *nodes):
        super(Node, self).__init__(tag)
        self.nodes = list(nodes)


class Leaf(Tree):
    pass


GLOBAL_LINE_HOLDER = []


def _draw_tree(tree, level, last=False, sup=[]):
    def update(left, i):
        if i < len(left):
            left[i] = "   "
        return left

    drawing = (
        "".join(reduce(update, sup, ["{}  ".format(pipe)] * level))
        + (end if last else branch)
        + "{} ".format(dash)
        + str(tree.tag)
    )
    print("0", drawing)
    GLOBAL_LINE_HOLDER.append(drawing)

    if isinstance(tree, Node):
        level += 1
        for node in tree.nodes[:-1]:
            _draw_tree(node, level, sup=sup)
        _draw_tree(tree.nodes[-1], level, True, [level] + sup)

    return GLOBAL_LINE_HOLDER


def draw_tree(trees):
    print("trees", trees)
    # sys.exit(0)
    for tree in trees[:-1]:
        _draw_tree(tree, 0)
    line_list = _draw_tree(trees[-1], 0, True, [0])

    print("line_list", line_list)
    full_ml_tree_str = "\n".join(line_list)
    print("line_list\n", full_ml_tree_str)

    # sys.exit(0)
    return full_ml_tree_str


class Track(object):
    def __init__(self, parent, idx):
        self.parent, self.idx = parent, idx


def parser(text):
    trees = []
    tracks = {}
    for line in text.splitlines():
        line = line.strip()
        key, value = map(lambda s: s.strip(), line.split(":", 1))
        # print("x", key, value, type(value))
        # sys.exit(0)
        nodes = value.split()
        if len(nodes):
            parent = Node(key)
            for i, node in enumerate(nodes):
                tracks[node] = Track(parent, i)
                parent.nodes.append(Leaf(node))
            curnode = parent
            if curnode.tag in tracks:
                t = tracks[curnode.tag]
                t.parent.nodes[t.idx] = curnode
            else:
                trees.append(curnode)
        else:
            curnode = Leaf(key)
            if curnode.tag in tracks:
                # well, how you want to handle it?
                pass  # ignore
            else:
                trees.append(curnode)
    return trees


if __name__ == "__main__":
    text = """apple: banana eggplant
    banana: cantaloupe durian
    eggplant:
    fig:"""

    # text = """ghf: hist_nlines grep_history _unique_history _fakecheese
    # grep_history: porky pies
    # _unique_history: _chop_first_column _add_line_numbers _top_ten
    # _add_line_numbers: yabba dabba doo
    # histdeln: histdel
    # _fakecheese: histdel _bacon
    # _bacon: _unique_history mayo"""

    draw_tree(parser(text))
