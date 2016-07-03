###############################################
#                                             #
#  Name : citing_refs_script.sh               #
#  Desc : Executes citing_refs.py             #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 4 ];then
    echo "Error: citing_refs_script.sh - Number of arguments"
    exit 1
fi

citing_ref_file=$1
citing_ref_res_file=$2
citing_ref_dat_file=$3
citing_ref_link_file=$4
if [ ! -f $citing_ref_file ];then
    echo "Error: citing_refs_script.sh - $citing_ref_file does not exist"
    exit 1
fi

python ${PYTHON_DIR}/citing_refs.py -i $citing_ref_file -1 $citing_ref_res_file -2 $citing_ref_dat_file -3 $citing_ref_link_file -l ${LOG_DIR}/citing_refs.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: citing_refs_script.sh - citing_refs.py failed"
    exit 1
fi
