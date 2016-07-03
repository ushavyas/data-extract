###############################################
#                                             #
#  Name : extract_xls_script.sh               #
#  Desc : Executes extract_xls.py             #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 2 ];then
    echo "Error: extract_xls_script.sh - Number of arguments"
    exit 1
fi

input_file=$1
output_xls=$2
if [ ! -f $input_file ];then
    echo "Error: extract_xls_script.sh - $input_file does not exist"
    exit 1
fi

python ${PYTHON_DIR}/extract_xls.py -i $input_file -o $output_xls -l ${LOG_DIR}/extract_xls.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: extract_xls_script.sh - extract_xls.py failed"
    exit 1
fi
