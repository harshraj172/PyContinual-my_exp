#Coding: UTF-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from transformers import BertTokenizer as BertTokenizer
import os
import torch
import numpy as np
import random
import nlp_data_utils as data_utils
from nlp_data_utils import ABSATokenizer
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler
import math



# domains = ['Video_Games','Toys_and_Games','Tools_and_Home_Improvement','Sports_and_Outdoors','Pet_Supplies',
#            'Patio_Lawn_and_Garden','Office_Products','Musical_Instruments','Movies_and_TV',
#            'Kindle_Store','Home_and_Kitchen','Health_and_Personal_Care','Grocery_and_Gourmet_Food','Electronics',
#            'Digital_Music','Clothing_Shoes_and_Jewelry','Cell_Phones_and_Accessories','CDs_and_Vinyl',
#            'Books','Beauty','Baby','Automotive','Apps_for_Android','Amazon_Instant_Video']

# domains = ['Video_Games','Toys_and_Games','Tools_and_Home_Improvement','Sports_and_Outdoors','Pet_Supplies',
#            'Patio_Lawn_and_Garden','Office_Products','Musical_Instruments','Movies_and_TV',
#            'Kindle_Store']

domains = ['derogation', 'animosity', 'dehumanization', 'threatening', 'support']

# domains = ['other.glorification', 'wc', 'bla.man', 'old.people', 'notargetrecorded', 'asi.chin', 'bla',
#  'arab', 'bla.wom', 'trans', 'indig.wom', 'indig', 'for', 'gay.wom', 'asi.east', 'asylum', 'eastern.europe', 'hispanic', 'trav', 'jew', 'ref',
#  'asi.pak', 'bis', 'nazis', 'mus.wom', 'asi.south', 'gendermin', 'hitler', 'immig', 'asi.man', 'wom', 'non.white.wom', 'non.white', 'gay.man',
#  'mus', 'mixed.race', 'asi', 'asi.wom', 'other.national', 'other.religion', 'pol', 'african', 'dis', 'russian', 'gay', 'lgbtq', 'ethnic.minority']

def get(logger=None,args=None):
    datasets = [ f'./dat/ssc/{args.domain_type}/'+domain for domain in domains]
    data={}
    taskcla=[]

    # Others
    f_name = f"./data_prep/ssc_random-{args.domain_type.split('-')[-1]}"

    with open(f_name,'r') as f_random_seq:
        random_sep = f_random_seq.readlines()[args.idrandom].split()

    args.ntasks = len(domains)
    
    print('random_sep: ',random_sep)
    print('domains: ',domains)
    print('ntasks: ',args.ntasks)
    
    for t in range(args.ntasks):
        dataset = datasets[domains.index(random_sep[t])]

        data[t]={}
        data[t]['name']=dataset
        data[t]['ncla']=2

        print('dataset: ',dataset)
        logger.info(dataset)

        processor = data_utils.DscProcessor()
        label_list = processor.get_labels()
        print(f"BERT Model : {args.bert_model}")
        tokenizer = ABSATokenizer.from_pretrained(args.bert_model)
        train_examples_text, train_examples = processor.get_train_examples(dataset)

        if args.train_data_size > 0: #TODO: for replicated results, better do outside (in prep_dsc.py), so that can save as a file
            random.Random(args.data_seed).shuffle(train_examples) #more robust
            train_examples = train_examples[:args.train_data_size]
            train_examples_text = train_examples_text[:args.train_data_size]

        #TODO: to be conssitent, sometimes we want to convert it back and save
        # with open('./dat/dsc/'+random_sep[t]+'/train_'+str(args.train_data_size),'w') as fw:
        #     logger.info('train_examples: '+str(len(train_examples)))
        #     for train_example in train_examples:
        #         fw.writelines(train_example.text_a + '\t' + train_example.label + '\n')
        #     logger.info('train_example.text_a: '+str(train_example.text_a))

        # Doble Saved:  So that no change on data even if we change the seed
        # if args.train_data_size > 0: # in some case, I might not cutting anything
        #     #So that no change on data even if we change the seed
        #     if not os.path.exists("./dat/dsc/"+str(random_sep[t])+"/train_data_"+str(args.train_data_size)+'_'+str(args.data_seed)):
        #         torch.save(train_examples,"./dat/dsc/"+str(random_sep[t])+"/train_data_"+str(args.train_data_size)+'_'+str(args.data_seed))
        #         logger.info("  save")
        #     else: #in that case, change seed will not change data
        #         train_examples = torch.load("./dat/dsc/"+str(random_sep[t])+"/train_data_"+str(args.train_data_size)+'_'+str(0)) #always use 0
        #         logger.info("  load")


        num_train_steps = int(math.ceil(len(train_examples) / args.train_batch_size)) * args.num_train_epochs
        # num_train_steps = int(len(train_examples) / args.train_batch_size) * args.num_train_epochs

        train_features = data_utils.convert_examples_to_features_dsc(
            train_examples, label_list, args.max_seq_length, tokenizer, "dsc")
        logger.info("***** Running training *****")
        logger.info("  Num examples = %d", len(train_examples))
        logger.info("  Batch size = %d", args.train_batch_size)
        logger.info("  Num steps = %d", num_train_steps)

#         all_input_ids = torch.tensor([f.input_ids for f in train_features], dtype=torch.long)
#         all_segment_ids = torch.tensor([f.segment_ids for f in train_features], dtype=torch.long)
#         all_input_mask = torch.tensor([f.input_mask for f in train_features], dtype=torch.long)
#         all_label_ids = torch.tensor([f.label_id for f in train_features], dtype=torch.long)
#         all_tasks = torch.tensor([t for f in train_features], dtype=torch.long)

#         train_data = TensorDataset(all_input_ids, all_segment_ids, all_input_mask, all_label_ids, all_tasks)


        # data[t]['train'] = train_data
        # data[t]['num_train_steps']=num_train_steps

        valid_examples_text, valid_examples = processor.get_dev_examples(dataset)
        # No need to change valid for DSC
        # if args.dev_data_size > 0:
        #     random.Random(args.data_seed).shuffle(valid_examples) #more robust
        #     valid_examples = valid_examples[:args.dev_data_size]

        valid_features=data_utils.convert_examples_to_features_dsc(
            valid_examples, label_list, args.max_seq_length, tokenizer, "dsc")
#         valid_all_input_ids = torch.tensor([f.input_ids for f in valid_features], dtype=torch.long)
#         valid_all_segment_ids = torch.tensor([f.segment_ids for f in valid_features], dtype=torch.long)
#         valid_all_input_mask = torch.tensor([f.input_mask for f in valid_features], dtype=torch.long)
#         valid_all_label_ids = torch.tensor([f.label_id for f in valid_features], dtype=torch.long)
#         valid_all_tasks = torch.tensor([t for f in valid_features], dtype=torch.long)

#         valid_data = TensorDataset(valid_all_input_ids, valid_all_segment_ids, valid_all_input_mask, valid_all_label_ids, valid_all_tasks)

        logger.info("***** Running validations *****")
        logger.info("  Num orig examples = %d", len(valid_examples))
        logger.info("  Num split examples = %d", len(valid_features))
        logger.info("  Batch size = %d", args.train_batch_size)

        # data[t]['valid']=valid_data


        processor = data_utils.DscProcessor()
        label_list = processor.get_labels()
        tokenizer = BertTokenizer.from_pretrained(args.bert_model)
        eval_examples_text, eval_examples = processor.get_test_examples(dataset)

        eval_features = data_utils.convert_examples_to_features_dsc(eval_examples, label_list, args.max_seq_length, tokenizer, "dsc")

        logger.info("***** Running evaluation *****")
        logger.info("  Num examples = %d", len(eval_examples))
        logger.info("  Batch size = %d", args.eval_batch_size)
#         all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
#         all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
#         all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
#         all_label_ids = torch.tensor([f.label_id for f in eval_features], dtype=torch.long)
#         all_tasks = torch.tensor([t for f in eval_features], dtype=torch.long)

#         eval_data = TensorDataset(all_input_ids, all_segment_ids, all_input_mask, all_label_ids, all_tasks)
        # Run prediction for full data

        # data[t]['test']=eval_data
        
        #**************************************************************
        features = train_features+valid_features+eval_features
        examples_text = train_examples_text+valid_examples_text+eval_examples_text
        all_input_ids = torch.tensor([f.input_ids for f in features], dtype=torch.long)
        all_segment_ids = torch.tensor([f.segment_ids for f in features], dtype=torch.long)
        all_input_mask = torch.tensor([f.input_mask for f in features], dtype=torch.long)
        all_label_ids = torch.tensor([f.label_id for f in features], dtype=torch.long)
        all_tasks = torch.tensor([t for f in features], dtype=torch.long)
        
        div_1, div_2, div_3 = int(len(all_input_ids)*0.8), int(len(all_input_ids)*0.9), len(all_input_ids) 
        train_data = TensorDataset(all_input_ids[:div_1], all_segment_ids[:div_1], all_input_mask[:div_1], all_label_ids[:div_1], all_tasks[:div_1])
        valid_data = TensorDataset(all_input_ids[div_1:div_2], all_segment_ids[div_1:div_2], all_input_mask[div_1:div_2], all_label_ids[div_1:div_2], all_tasks[div_1:div_2])
        eval_data = TensorDataset(all_input_ids[div_2:div_3], all_segment_ids[div_2:div_3], all_input_mask[div_2:div_3], all_label_ids[div_2:div_3], all_tasks[div_2:div_3])

        data[t]['train'] = train_data
        data[t]['num_train_steps']=num_train_steps
        data[t]['valid']=valid_data
        data[t]['test']=eval_data
        data[t]['test_examples_text']=examples_text[div_2:div_3]
        taskcla.append((t,int(data[t]['ncla'])))



    # Others
    n=0
    for t in data.keys():
        n+=data[t]['ncla']
    data['ncla']=n


    return data,taskcla