###############################################
#                                             #
#  Name : wos_login_script.sh                 #
#  Desc : Executes wos_login.py               #
#                                             #
###############################################

PYTHON_DIR="/home/usha/wos/python"
LOG_DIR="/home/usha/wos/log"

if [ $# -ne 3 ];then
    echo "Error: wos_login_script.sh - Number of arguments"
    exit 1
fi

login_file=$1
user=$2
passwd=$3

python ${PYTHON_DIR}/wos_login.py -o $login_file -u $user -p $passwd -l ${LOG_DIR}/wos_login.log
ret=$?
if [ $ret -ne 0 ];then
    echo "Error: wos_login_script.sh - wos_login.py failed"
    exit 1
fi
