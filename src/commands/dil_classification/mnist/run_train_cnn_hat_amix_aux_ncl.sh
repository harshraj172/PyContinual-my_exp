#!/bin/bash
#SBATCH -p gpu20
#SBATCH -t 20:00:00
#SBATCH -o dil_asc_adapter_mask_mixup_1-%j.out
#SBATCH --gres gpu:1


for id in 0 1 2 3 4
do
    CUDA_VISIBLE_DEVICES=1 python run.py \
    --bert_model 'bert-base-uncased' \
    --note random$id,last_id,Attn-HCHP,sup,naug1,selfattn,6200\
    --ntasks 10 \
    --nclasses 62 \
    --task femnist \
    --scenario dil_classification \
    --idrandom $id \
    --approach cnn_hat_aux_ncl \
    --eval_batch_size 128 \
    --train_batch_size 32 \
    --data_size full \
    --train_data_size 6200 \
    --image_size 28 \
    --image_channel 1 \
    --nepochs 100 \
    --aux_nepochs 500 \
    --temp 1 \
    --base_temp 1 \
    --output_dir './OutputBert' \
    --two_stage \
    --aux_net \
    --sup_loss \
    --amix \
    --attn_type self \
    --task_based \
    --mix_type Attn-HCHP-Outside \
    --naug 1
done
#--nepochs 1
#    --train_batch_size 128 \
#-m torch.distributed.launch --nproc_per_node=2
#    --distributed \
#    --multi_gpu \
#    --ngpus 2

#    --lr 0.05 \
#    --lr_min 1e-4 \
#    --lr_factor 3 \
#    --lr_patience 5 \
#    --clipgrad 10000

#semantic cap size 1000, 500, 2048
