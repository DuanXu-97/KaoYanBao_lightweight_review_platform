from numpy import *
import itertools

support_dic = {}

global result_direct
result_direct ={ }
#获取整个数据库中的一阶元素
def createC1(dataSet):
    C1 = set([])
    for item in dataSet:
        C1 = C1.union(set(item))
    return [frozenset([i]) for i in C1]

def getLK(dataset, Ck, minsupport):
    global support_dic
    Lk = {}
    for item in dataset:
        for Ci in Ck:
            if Ci.issubset(item):  # 测试Ci中的每一个元素是否都在item中
                if not Ci in Lk:
                    Lk[Ci] = 1
                else:
                    Lk[Ci] += 1

    Lk_return = []
    for Li in Lk:
        support_Li = Lk[Li] / float(len(dataset))
        if support_Li >= minsupport:  # 用最小的支持度进行过滤
            Lk_return.append(Li)
            support_dic[Li] = support_Li
    return Lk_return


def genLk1(Lk):  # 将经过支持度过滤后的第K层数据融合都得到原始数据Ck1
    Ck1 = []
    for i in range(len(Lk) - 1):
        for j in range(i + 1, len(Lk)):
            if sorted(list(Lk[i]))[0:-1] == sorted(list(Lk[j]))[0:-1]:
                Ck1.append(Lk[i] | Lk[j])
    return Ck1


def genRule(Item, minconf=0.7):  # 递归对规则树进行剪枝
    global result_direct
    if len(Item) >= 2:
        for element in itertools.combinations(list(Item), 1):
            if support_dic[Item] / float(support_dic[Item - frozenset(element)]) >= minconf:
                print(str([Item - frozenset(element)]) + "---->" + str(element))
                result_direct[Item - frozenset(element)]=set(list(element))           #规则字典
                print(support_dic[Item] / float(support_dic[Item - frozenset(element)]))
                genRule(Item - frozenset(element))


def genItem(freqset, support_dic):
    for i in range(1, len(freqset)):
        for freItem in freqset[i]:
            genRule(freItem)


def main(dataset):
    global result_direct
    result_list = []
    Ck = createC1(dataset)
    while True:
        Lk = getLK(dataset, Ck, 0.5)  # 筛选
        if not Lk:
            break
        result_list.append(Lk)
        Ck = genLk1(Lk)  # 融合
        if not Ck:
            break

    print(support_dic)

    genItem(result_list, support_dic)
    return result_direct
