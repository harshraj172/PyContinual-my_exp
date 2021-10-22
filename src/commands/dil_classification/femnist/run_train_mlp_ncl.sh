#!/bin/bash
#SBATCH -p gpu20
#SBATCH -t 10:00:00
#SBATCH -o dil_nli_ncl_4-%j.out
#SBATCH --gres gpu:1


for id in 0
do
    python  run.py \
    --note random$id,6200\
    --ntasks 10 \
    --task femnist \
    --scenario dil_classification \
    --idrandom $id \
    --approach mlp_ncl  \
    --eval_batch_size 128 \
    --train_batch_size 32 \
    --model_path "./models/fp32/dil_classification/femnist/mlp_ncl_$id" \
    --save_model
done
#--nepochs 1
#    --train_data_size 500