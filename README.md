# MLEC-QA

This repository contains the data and baseline code of The 2021 Conference on Empirical Methods in Natural Language Processing (EMNLP 2021) paper "MLEC-QA: A Chinese Multi-Choice Biomedical Question Answering Dataset".

- Paper: [ACL Anthology](https://aclanthology.org/2021.emnlp-main.698/)

If you would like to use the data or code, please cite:

```
@inproceedings{li-etal-2021-mlec,
    title = "{MLEC-QA}: {A} {C}hinese {M}ulti-{C}hoice {B}iomedical {Q}uestion {A}nswering {D}ataset",
    author = "Li, Jing  and
      Zhong, Shangping  and
      Chen, Kaizhi",
    booktitle = "Proceedings of the 2021 Conference on Empirical Methods in Natural Language Processing",
    month = nov,
    year = "2021",
    address = "Online and Punta Cana, Dominican Republic",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2021.emnlp-main.698",
    pages = "8862--8874",
}
```

MLEC-QA is a Chinese multi-choice Biomedical Question Answering Dataset. Questions in MLEC-QA are collected from the [National Medical Licensing Examination in China (NMLEC)](https://www.nmec.org.cn/Pages/ArticleInfo-13-10706.html), which are carefully designed by human experts to evaluate professional knowledge and skills for those who want to be medical practitioners in China.

We hope the release of the MLEC-QA dataset can serve as a valuable resource for research and evaluation in Open-domain QA, and also make advances for Biomedical Question Answering systems.

# Dataset

Download MLEC-QA dataset: [Google Drive](https://drive.google.com/file/d/1-v4c8bcTspgBINKticTF7A9OMum0CB_y/view?usp=sharing)

MLEC-QA is composed of 5 subsets with 136,236 Chinese multi-choice biomedical questions with extra materials (images or tables) annotated by human experts, and covers the following biomedical sub-fields:

- Clinic (临床): `Clinic_{train,dev,test}.json`
- Stomatology (口腔): `Stomatology_{train,dev,test}.json`
- Public Health (公共卫生): `PublicHealth_{train,dev,test}.json`
- Traditional Chinese Medicine (中医): `TCM_{train,dev,test}.json`
- Traditional Chinese Medicine Combined with Western Medicine (中西医结合): `CWM_{train,dev,test}.json`

The JSON dataset file format is as follows:

```
{
	"qid":The question ID,
	"qtype":["A1型题", "B1型题", "A2型题", "A3/A4型题"],
	"qtext":Description of the question,
	"qimage":Image or table path (if any),
	"options":{
		"A":Description of the option A,
		"B":Description of the option B,
		"C":Description of the option C,
		"D":Description of the option D,
		"E":Description of the option E
	},
	"answer":["A", "B", "C", "D", "E"]
}   	
```

# Baselines

Install the requirements:

```
cd code
pip install -r requirements.txt
```

## Control Methods

- **Random:** For each question, an option is randomly chosen as the answer from five candidate options. We perform this experiment five times and average the results as the baseline of the Random method.
- **Constant_j:** For each question, the $j^{th}$ option is always chosen as the answer to obtain the accuracy distribution of five candidate options.
- **Mixed:** The Mixed method simulates how humans solving uncertain questions, and consists of the following 3 strategies: 
  - The correct rate of choosing "All of the options above is correct/incorrect" is much higher than the other options.
  - Supposing the length of options is roughly equal, only one option is obviously longer with more detailed and specific descriptions, or is obviously shorter than the other options, then choose this option.
  - The correct option tends to appear in the middle of candidate options. The three strategies are applied in turn. If any strategy matches, then the option that matches the strategy is chosen as the answer.

## Open-Domain QA Methods

Open-Domain QA Methods is consist of a two-stage retriever-reader framework: 

- A retriever finding documents that (might) contain an answer from a large collection of documents. We adopt [Chinese Wikipedia dumps](https://dumps.wikimedia.org/) as our information sources, and use a distributed search and analytics engine, [ElasticSearch](https://www.elastic.co/), as the document store and document retriever.

- A reader finding the answer in given documents retrieved by the retriever. We fine-tune five pre-trained language models for machine reading comprehension as the reader.

### Document Retriever

1. Download Elasticsearch 7.10.1, Kibana 7.10.1 and run the servers locally with out-of-the-box defaults.
2. Create an inverted index of Chinese Wikipedia dumps in Elasticsearch using `wiki_zh_json2es.py`.
3. Run `retriever.py`.

### Document Reader

#### Models

The pre-trained language models used on Open-Domain QA Methods can be downloaded from huggingface, and using scripts from the scripts directory to convert them into the format that reader can load directly.

- BERT-Base: https://huggingface.co/bert-base-chinese

- BERT-Base-Multilingual: https://huggingface.co/bert-base-multilingual-uncased

- BERT-wwm-ext: https://huggingface.co/hfl/chinese-bert-wwm-ext

- RoBERTa-wwm-ext: https://huggingface.co/hfl/chinese-roberta-wwm-ext

- RoBERTa-wwm-ext-large: https://huggingface.co/hfl/chinese-roberta-wwm-ext-large

#### Usage

```bash
run_mlecqa.py [-h] [--pretrained_model_path PRETRAINED_MODEL_PATH]
                 [--output_model_path OUTPUT_MODEL_PATH]
                 [--vocab_path VOCAB_PATH] [--spm_model_path SPM_MODEL_PATH]
                 --train_path TRAIN_PATH --dev_path DEV_PATH
                 [--test_path TEST_PATH] [--config_path CONFIG_PATH]
                 [--embedding {word,word_pos,word_pos_seg,word_sinusoidalpos}]
                 [--max_seq_length MAX_SEQ_LENGTH]
                 [--relative_position_embedding]
                 [--relative_attention_buckets_num RELATIVE_ATTENTION_BUCKETS_NUM]
                 [--remove_embedding_layernorm] [--remove_attention_scale]
                 [--encoder {transformer,rnn,lstm,gru,birnn,bilstm,bigru,gatedcnn}]
                 [--mask {fully_visible,causal,causal_with_prefix}]
                 [--layernorm_positioning {pre,post}]
                 [--feed_forward {dense,gated}] [--remove_transformer_bias]
                 [--layernorm {normal,t5}] [--bidirectional]
                 [--factorized_embedding_parameterization]
                 [--parameter_sharing] [--learning_rate LEARNING_RATE]
                 [--warmup WARMUP] [--fp16] [--fp16_opt_level {O0,O1,O2,O3}]
                 [--optimizer {adamw,adafactor}]
                 [--scheduler {linear,cosine,cosine_with_restarts,polynomial,constant,constant_with_warmup}]
                 [--batch_size BATCH_SIZE] [--seq_length SEQ_LENGTH]
                 [--dropout DROPOUT] [--epochs_num EPOCHS_NUM]
                 [--report_steps REPORT_STEPS] [--seed SEED]
                 [--max_choices_num MAX_CHOICES_NUM]
                 [--tokenizer {bert,char,space}]
```

The example of using `run_mlecqa.py`:

```bash
python3 run_mlecqa.py --pretrained_model_path models/bert-base.bin \
--vocab_path models/google_zh_vocab.txt \
--train_path datasets/train.json \
--dev_path datasets/dev.json \
--test_path datasets/test.json \
--epochs_num 12 \
--batch_size 1 \
--seq_length 512 \
--max_choices_num 5 \
--learning_rate 2e-6 \
--report_steps 100 \

The actual batch size is --batch_size times --max_choices_num.
```

