source /opt/conda/bin/activate
conda activate train_env

python run_evaluation.py \
-i /data/Drone_Audio_dataset_intflow/noisy_real/noisy \
-o /data/Drone_Audio_dataset_intflow/noisy_real/proc \
-m models_DTLN_Drone_48k_intflow_3/DTLN_Drone_48k_intflow_3.h5