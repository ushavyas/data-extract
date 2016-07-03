###############################################
#                                             #
#  Name : extract_data_script.sh              #
#  Desc : Executes extract_data.py            #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 2 ];then
    echo "Error: extract_data_script.sh - Number of arguments"
    exit 1
fi

res_file=$1
dat_file=$2
if [ ! -f $res_file ];then
    echo "Error: extract_data_script.sh - $res_file does not exist"
    exit 1
fi

python ${PYTHON_DIR}/extract_data.py -i $res_file -o $dat_file -l ${LOG_DIR}/extract_data.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: extract_data_script.sh - extract_data.py failed"
    exit 1
fi
