###############################################
#                                             #
#  Name : link_refs_script.sh                 #
#  Desc : Executes link_refs.py               #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 3 ];then
    echo "Error: link_refs_script.sh - Number of arguments"
    exit 1
fi

res_file=$1
cited_ref_file=$2
citing_ref_file=$3
if [ ! -f $res_file ];then
    echo "Error: link_refs_script.sh - $res_file does not exist"
    exit 1
fi

python ${PYTHON_DIR}/link_refs.py -i $res_file -1 $cited_ref_file -2 $citing_ref_file -l ${LOG_DIR}/link_refs.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: link_refs_script.sh - link_refs.py failed"
    exit 1
fi
