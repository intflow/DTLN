source /opt/conda/bin/activate
conda activate train_env

python run_evaluation.py \
-i /data/DNS-Challenge/training_set/val/noisy \
-o /data/DNS-Challenge/training_set/val/proc \
-m ./models_DTLN_model/DTLN_model.h5