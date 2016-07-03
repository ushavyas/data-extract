###############################################
#                                             #
#  Name : cited_refs_script.sh                #
#  Desc : Executes cited_refs.py              #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 4 ];then
    echo "Error: cited_refs_script.sh - Number of arguments"
    exit 1
fi

cited_ref_file=$1
cited_ref_res_file=$2
cited_ref_dat_file=$3
cited_ref_link_file=$4
if [ ! -f $cited_ref_file ];then
    echo "Error: cited_refs_script.sh - $cited_ref_file does not exist"
    exit 1
fi

python ${PYTHON_DIR}/cited_refs.py -i $cited_ref_file -1 $cited_ref_res_file -2 $cited_ref_dat_file -3 $cited_ref_link_file -l ${LOG_DIR}/cited_refs.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: cited_refs_script.sh - cited_refs.py failed"
    exit 1
fi
