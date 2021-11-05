import random
import time
import json

data_dir = './data/'


def noRepetRandomSampling(dataMat, number):
    '''
    Sampling without replacement
    :param dataMat: Dataset
    :param number: Number of samples
    :return: sample Sampling results
    '''
    try:
        length = len(dataMat)
        sample = random.sample(dataMat, number)
        return sample
    except Exception as e:
        print(e)


def stratifiedSampling(dataMat, number):
    '''
    Stratified sampling
    :param dataMat: Dataset
    :param number: Number of samples
    :return: sample Sampling results
    '''
    subNumber = int(number // len(dataMat))
    sample = []
    for data in dataMat:
        sample.append(noRepetRandomSampling(data, subNumber))

    return sample


def main():
    etype = 'Clinic_dev'  # Clinic, Stomatology, PublicHealth, TCM, CWM
    file = etype + '.json'
    print(file)
    with open(data_dir + file, 'r', encoding='utf-8') as f1:
        data_json = json.load(f1)

    A1, A2, A3A4, B1 = [], [], [], []
    for samp in data_json:
        if 'A1' in samp['qtype']:
            A1.append(samp)
        elif 'A2' in samp['qtype']:
            A2.append(samp)
        elif 'B1' in samp['qtype']:
            B1.append(samp)
        else:
            A3A4.append(samp)

    dataMat = [A1] + [B1] + [A2] + [A3A4]
    samp_num = round(len(data_json) * 0.05, 0)  # sample 5%

    res_samp = stratifiedSampling(dataMat, samp_num)
    for qtype in res_samp:
        print('Number of stratified samples:', len(qtype))
        print('qtype:', qtype[0]['qtype'])
        for res in qtype:
            print('[docs]')
            print(res['docs'].replace('\n', ''))

            print('[qtext]')
            print(res['qtext'])

            print('[options]')
            print(res['options'])

            print('[answer]')
            print(res['answer'])
            print()
        print()


if __name__ == "__main__":
    start = time.time()
    main()
    end = time.time()
    print("\nTotal time elapsed: %s s" % (end - start))
