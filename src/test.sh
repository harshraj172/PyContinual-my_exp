#!/bin/bash

export TRANSFORMERS_CACHE='./model_cache'
export HF_DATASETS_CACHE='./dataset_cache'

# # eval only
# for id in 0
# do
#     python run.py \
#         --domain_type 'domain-type' \
# 		--bert_model 'bert-base-uncased' \
# 		--backbone bert_adapter \
# 		--baseline b-cl \
# 		--task dsc \
# 		--eval_batch_size 128 \
# 		--train_batch_size 8 \
# 		--scenario til_classification \
# 		--idrandom 0  \
#         --eval_only \
#         --resume_from_file \
#         --output_dir 'res/' \
# 		--use_predefine_args
# done

# without resume 
for id in 0
do
    python run-2.py \
        --domain_type 'domain-type' \
		--bert_model 'bert-base-uncased' \
		--backbone bert_adapter \
		--baseline ctr \
		--task dsc \
		--eval_batch_size 128 \
		--train_batch_size 44 \
		--scenario til_classification \
		--idrandom 0  \
        --output_dir 'res/' \
		--use_predefine_args
done


## resume
# for id in 0
# do
#     python run.py \
#         --domain_type 'domain-target' \
# 		--bert_model 'bert-base-uncased' \
# 		--backbone bert_adapter \
# 		--baseline ctr \
# 		--task dsc \
# 		--eval_batch_size 128 \
# 		--train_batch_size 48 \
# 		--scenario til_classification \
# 		--idrandom 0  \
#         --resume_model \
#         --resume_from_task 3 \
#         --base_resume_from_aux_file 'saved_model/domain-target/ctr/aux/' \
#         --base_resume_from_file 'saved_model/domain-target/ctr/' \
#         --save_model \
#         --save_each_step \
#         --saved_model_dir 'saved_model/' \
#         --output_dir 'res/' \
# 		--use_predefine_args
# done