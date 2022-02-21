source /opt/conda/bin/activate
conda activate train_env

python run_evaluation.py \
-i /data/Drone_Audio_dataset_intflow/training_set/val/noisy \
-o /data/Drone_Audio_dataset_intflow/training_set/val/proc_2 \
-m models_DTLN_Drone_48k_intflow_2/DTLN_Drone_48k_intflow_2.h5