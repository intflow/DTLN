source /opt/conda/bin/activate
conda activate train_env

python convert_weights_to_tf_lite.py \
-m ./models_DTLN_model/DTLN_model.h5 \
-t ./models_DTLN_model