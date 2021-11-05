import time
import os
import json
import random
import copy
import numpy as np
import sys

data_dir = './data/'
kd_acc_ls, ca_acc_ls, all_acc_ls = [], [], []


def random_answer(data_json):
    print('*' * 5, 'Random Answer', '*' * 5)

    qtype_res = {}
    for samp in data_json:
        qtype_res[samp['qtype']] = 0

    qtype_all = qtype_res.copy()
    for samp in data_json:
        qtype_all[samp['qtype']] += 1

        ans = random.randint(0, len(samp['options']) - 1)

        if samp['answer'] == list(samp['options'].keys())[ans]:
            qtype_res[samp['qtype']] += 1

    print('All data:', qtype_all)
    print('Random Answer Results:', qtype_res)
    kd_acc, ca_acc, all_acc = eval(qtype_all, qtype_res)
    kd_acc_ls.append(kd_acc)
    ca_acc_ls.append(ca_acc)
    all_acc_ls.append(all_acc)


def constant_answer(data_json):
    print('*' * 5, 'Constant Answer', '*' * 5)

    qtype_res = {}
    option_num = 0
    for samp in data_json:
        qtype_res[samp['qtype']] = 0
        if len(samp['options']) > option_num:
            option_num = len(samp['options'])

    qtype_res_ls = []
    for i in range(option_num):
        qtype_res_ls.append(qtype_res.copy())

    qtype_all = qtype_res.copy()
    for samp in data_json:
        qtype_all[samp['qtype']] += 1

        for ans in range(len(samp['options'])):
            if samp['answer'] == list(samp['options'].keys())[ans]:
                qtype_res_ls[ans][samp['qtype']] += 1

    print('All data:', qtype_all)
    for i in range(option_num):
        print('Constant [%c] Answer Results: %s' % (i + 65, qtype_res_ls[i]))
        eval(qtype_all, qtype_res_ls[i])


def mixed_answer(data_json, kd, ca):
    print('*' * 5, 'Mixed Answer', '*' * 5)

    qtype_res = {}
    for samp in data_json:
        qtype_res[samp['qtype']] = 0

    qtype_all = qtype_res.copy()
    for samp in data_json:
        qtype_all[samp['qtype']] += 1
        options_ls = list(samp['options'].values())

        def get_option_type(op_ls):
            op_ls_original = copy.deepcopy(op_ls)
            op_ls.sort(key=len)  # Ascending by length

            if (len(op_ls[1]) - len(op_ls[0])) - (len(op_ls[-1]) - len(op_ls[1])) > 0:  # Four long, one short
                return op_ls_original.index(op_ls[0])
            elif (len(op_ls[-1]) - len(op_ls[-2])) - (len(op_ls[-2]) - len(op_ls[0])) > 0:  # Four short, one long
                return op_ls_original.index(op_ls[-1])
            else:  # others
                if '1' in samp['qtype']:  # KD
                    return kd
                else:  # CA
                    return ca

        if '以上' in options_ls[-1] and ('都' in options_ls[-1] or '均' in options_ls[-1]):
            ans = 4  # option E
        else:
            ans = get_option_type(options_ls)

        try:
            if samp['answer'] == list(samp['options'].keys())[ans]:
                qtype_res[samp['qtype']] += 1
        except:
            None

    print('All data:', qtype_all)
    print('Mixed Answer Results:', qtype_res)
    eval(qtype_all, qtype_res)


def eval(qtype_all, qtype_res):
    kd_all, ca_all, kd, ca = 0, 0, 0, 0
    for key in qtype_all.keys():
        # all += qtype_all[key]
        if 'A1' in key or 'B1' in key:
            kd += qtype_res[key]
            kd_all += qtype_all[key]
        else:
            ca += qtype_res[key]
            ca_all += qtype_all[key]

    all_acc = (kd + ca) / (kd_all + ca_all)
    kd_acc = kd / kd_all
    ca_acc = ca / ca_all

    # print(all, kd, ca)
    print('KD-Questions Accuracy:', round(kd_acc, 4))
    print('CA-Questions Accuracy:', round(ca_acc, 4))
    print('ALL-Questions Accuracy:', round(all_acc, 4))
    print()
    return kd_acc, ca_acc, all_acc


def main():
    etype = 'Clinic'  # Clinic, Stomatology, PublicHealth, TCM, CWM
    file = etype + '.json'
    print(file)
    with open(data_dir + file, 'r', encoding='utf-8') as f1:
        data_json = json.load(f1)

    # random
    for i in range(5):
        random_answer(data_json)
    print('***** Random Answer Average*****')
    print('KD-Questions Accuracy:', round(np.mean(kd_acc_ls), 4))
    print('CA-Questions Accuracy:', round(np.mean(ca_acc_ls), 4))
    print('ALL-Questions Accuracy:', round(np.mean(all_acc_ls), 4))
    print('#' * 20)
    # Constant
    constant_answer(data_json)
    print('#' * 20)

    # mixed based on the Semple's results
    mixed_answer(data_json, 2, 2)  # A0 B1 C2 D3 E4


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("\nTotal time elapsed: %s s" % (end - start))
