source /opt/conda/bin/activate
conda activate train_env

python convert_weights_to_tf_lite.py \
-m ./pretrained_model/DTLN_Drone_48k_intflow_3.h5 \
-t ./pretrained_model/DTLN_Drone_48k_intflow_3