###############################################
#                                             #
#  Name : search_pattern_script.sh            #
#  Desc : Executes search_pattern.py          #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 3 ];then
    echo "Error: search_pattern_script.sh - Number of arguments"
    exit 1
fi

login_file=$1
res_file=$2
journal=$3
if [ ! -f $login_file ];then
    echo "Error: search_pattern_script.sh - $login_file does not exist"
    exit 1
fi

python ${PYTHON_DIR}/search_pattern.py -i $login_file -o $res_file -j "$journal" -l ${LOG_DIR}/search_pattern.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: search_pattern_script.sh - search_pattern.py failed"
    exit 1
fi
