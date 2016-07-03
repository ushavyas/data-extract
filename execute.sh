######################################################
#                                                    #
#  Name : execute.sh                                 #
#  Desc : To execute all jobs step by step           #
#                                                    #
######################################################

LOG_DIR="/home/usha/wos/log"
SHELL_DIR="/home/usha/wos/shell"
FILES_DIR="/home/usha/wos/files"

rm -f ${LOG_DIR}/wos_login.log ${LOG_DIR}/search_pattern.log ${LOG_DIR}/extract_data.log ${LOG_DIR}/link_refs.log ${LOG_DIR}/cited_refs.log ${LOG_DIR}/citing_refs.log ${LOG_DIR}/extract_xls.log ${LOG_DIR}/ref_links.log
if [ $? -ne 0 ];then
    echo "Error: Removing log files"
    exit 1
fi

echo -n "Username : "
read user
echo -n "Password : "
read -s passwd
echo -n "Journal name in quotes : "
read journal

    echo $journal
    name=`echo $journal | sed 's/ /_/g' | sed 's/"//g'`

    login_file="login_${name}.txt"
    res_file="result_${name}.txt"
    dat_file="data_${name}.txt"
    cited_ref_file="cited_ref_${name}.txt"
    citing_ref_file="citing_ref_${name}.txt"
    cited_ref_res_file="cited_ref_result_${name}.txt"
    citing_ref_res_file="citing_ref_result_${name}.txt"
    cited_ref_dat_file="cited_ref_data_${name}.txt"
    citing_ref_dat_file="citing_ref_data_${name}.txt"
    cited_ref_link_file="cited_ref_link_${name}.txt"
    citing_ref_link_file="citing_ref_link_${name}.txt"

    data_xls="actual_data_${name}.xls"
    cited_ref_data_xls="cited_ref_data_${name}.xls"
    cited_ref_link_xls="cited_ref_link_${name}.xls"
    citing_ref_data_xls="citing_ref_data_${name}.xls"
    citing_ref_link_xls="citing_ref_link_${name}.xls"

    # STEP 0
    # Login to the website
    echo "======================"
    ${SHELL_DIR}/wos_login_script.sh ${FILES_DIR}/$login_file $user $passwd &
    echo "Executing wos_login.py.."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "wos_login.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/wos_login.log`
    if [ "$stat" != "Success" ];then
        echo "Error: wos_login.py, check ${LOG_DIR}/wos_login.log for details"
        exit 1
    fi
    echo "Success: wos_login.py"

    # STEP 1
    # Search results for current journal
    echo "======================"
    ${SHELL_DIR}/search_pattern_script.sh ${FILES_DIR}/$login_file ${FILES_DIR}/$res_file "$journal" &
    echo "Executing search_pattern.py.."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "search_pattern.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/search_pattern.log`
    if [ "$stat" != "Success" ];then
        echo "Error: search_pattern.py, check ${LOG_DIR}/search_pattern.log for details"
        exit 1
    fi
    echo "Success: search_pattern.py"
    res_cnt=`cat ${FILES_DIR}/$res_file | wc -l`
    echo "Number of results found for $journal : $res_cnt"

    # STEP 2
    # Extract data for results found
    echo "======================"
    ${SHELL_DIR}/extract_data_script.sh ${FILES_DIR}/$res_file ${FILES_DIR}/$dat_file &
    echo "Executing extract_data.py.."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "extract_data.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/extract_data.log`
    if [ "$stat" != "Success" ];then
        echo "Error: extract_data.py, check ${LOG_DIR}/extract_data.log for details"
        exit 1
    fi
    echo "Success: extract_data.py"
    dat_cnt=`cat ${FILES_DIR}/$dat_file | wc -l`
    echo "Number of articles extracted for $journal : $dat_cnt"

    # Check the count of data extracted
    if [ $res_cnt -ne $dat_cnt ];then
        echo "Error: Count mismatch in $res_file and $dat_file files"
        exit 1
    fi

    # STEP 3
    # Extract cited references and citing references links
    echo "======================"
    ${SHELL_DIR}/link_refs_script.sh ${FILES_DIR}/$res_file ${FILES_DIR}/$cited_ref_file ${FILES_DIR}/$citing_ref_file &
    echo "Executing link_refs.py.."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "link_refs.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/link_refs.log`
    if [ "$stat" != "Success" ];then
        echo "Error: link_refs.py, check ${LOG_DIR}/link_refs.log for details"
        exit 1
    fi
    echo "Success: link_refs.py"
    cnt1=`cat ${FILES_DIR}/$cited_ref_file | wc -l`
    cnt2=`cat ${FILES_DIR}/$citing_ref_file | wc -l`

    if [ $cnt1 -ne $cnt2 ];then
        echo "Error: Count mismatch between $cited_ref_file and $citing_ref_file"
        exit 1
    fi

    # STEP 4 and 5
    # Extract all the cited reference results, corresponding data and connecting information
    echo "======================"
    ${SHELL_DIR}/cited_refs_script.sh ${FILES_DIR}/$cited_ref_file ${FILES_DIR}/$cited_ref_res_file ${FILES_DIR}/$cited_ref_dat_file ${FILES_DIR}/$cited_ref_link_file &
    # Extract all the citing reference results, corresponding data and connecting information
    ${SHELL_DIR}/citing_refs_script.sh ${FILES_DIR}/$citing_ref_file ${FILES_DIR}/$citing_ref_res_file ${FILES_DIR}/$citing_ref_dat_file ${FILES_DIR}/$citing_ref_link_file &
    echo "Executing cited_refs.py and citing_refs.py .."
    while true
    do
        sleep 30
        exec1=`ps -eaf | grep python | grep -c "cited_refs.py"`
        exec2=`ps -eaf | grep python | grep -c "citing_refs.py"`
        if [[ $exec1 -eq 0 && $exec2 -eq 0 ]];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/cited_refs.log`
    if [ "$stat" != "Success" ];then
        echo "Error: cited_refs.py, check ${LOG_DIR}/cited_refs.log for details"
        exit 1
    fi
    echo "Success: cited_refs.py"
    cited_dat_cnt=`cat ${FILES_DIR}/$cited_ref_dat_file | wc -l`
    cited_link_cnt=`cat ${FILES_DIR}/$cited_ref_link_file | wc -l`

    if [ $cited_dat_cnt -ne $cited_link_cnt ];then
        echo "Error: Count mismatch between $cited_ref_dat_file and $cited_ref_link_file"
        exit 1
    fi

    stat=`tail -1 ${LOG_DIR}/citing_refs.log`
    if [ "$stat" != "Success" ];then
        echo "Error: citing_refs.py, check ${LOG_DIR}/citing_refs.log for details"
        exit 1
    fi
    echo "Success: citing_refs.py"
    citing_dat_cnt=`cat ${FILES_DIR}/$citing_ref_dat_file | wc -l`
    citing_link_cnt=`cat ${FILES_DIR}/$citing_ref_link_file | wc -l`

    if [ $citing_dat_cnt -ne $citing_link_cnt ];then
        echo "Error: Count mismatch between $citing_ref_dat_file and $citing_ref_link_file"
        exit 1
    fi

    # STEP 6
    # Convert actual data into excel format
    echo "======================"
    ${SHELL_DIR}/extract_xls_script.sh ${FILES_DIR}/$dat_file ${FILES_DIR}/$data_xls &
    echo "Executing extract_xls.py for $dat_file .."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "extract_xls.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/extract_xls.log`
    if [ "$stat" != "Success" ];then
        echo "Error: extract_xls.py, check ${LOG_DIR}/extract_xls.log for details"
        exit 1
    fi
    echo "Success: extract_xls.py for $dat_file"

    # STEP 7
    # Convert cited references data into excel format
    echo "======================"
    ${SHELL_DIR}/extract_xls_script.sh ${FILES_DIR}/$cited_ref_dat_file ${FILES_DIR}/$cited_ref_data_xls &
    echo "Executing extract_xls.py for $cited_ref_dat_file .."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "extract_xls.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/extract_xls.log`
    if [ "$stat" != "Success" ];then
        echo "Error: extract_xls.py, check ${LOG_DIR}/extract_xls.log for details"
        exit 1
    fi
    echo "Success: extract_xls.py for $cited_ref_dat_file"

    # STEP 8
    # Convert cited references links into excel format
    echo "======================"
    ${SHELL_DIR}/ref_links_script.sh ${FILES_DIR}/$cited_ref_link_file ${FILES_DIR}/$cited_ref_link_xls &
    echo "Executing ref_links.py for $cited_ref_link_file .."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "ref_links.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/ref_links.log`
    if [ "$stat" != "Success" ];then
        echo "Error: ref_links.py, check ${LOG_DIR}/ref_links.log for details"
        exit 1
    fi
    echo "Success: ref_links.py for $cited_ref_link_file"

    # STEP 9
    # Convert citing references data into excel format
    echo "======================"
    ${SHELL_DIR}/extract_xls_script.sh ${FILES_DIR}/$citing_ref_dat_file ${FILES_DIR}/$citing_ref_data_xls &
    echo "Executing extract_xls.py for $citing_ref_dat_file .."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "extract_xls.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/extract_xls.log`
    if [ "$stat" != "Success" ];then
        echo "Error: extract_xls.py, check ${LOG_DIR}/extract_xls.log for details"
        exit 1
    fi
    echo "Success: extract_xls.py for $citing_ref_dat_file"

    # STEP 10
    # Convert citing references links into excel format
    echo "======================"
    ${SHELL_DIR}/ref_links_script.sh ${FILES_DIR}/$citing_ref_link_file ${FILES_DIR}/$citing_ref_link_xls &
    echo "Executing ref_links.py for $citing_ref_link_file .."
    while true
    do
        sleep 5
        exec=`ps -eaf | grep python | grep -c "ref_links.py"`
        if [ $exec -eq 0 ];then
            break
        fi
    done
    stat=`tail -1 ${LOG_DIR}/ref_links.log`
    if [ "$stat" != "Success" ];then
        echo "Error: ref_links.py, check ${LOG_DIR}/ref_links.log for details"
        exit 1
    fi
    echo "Success: ref_links.py for $citing_ref_link_file"

    echo "############################"
    echo "Job successful for Journal: $journal"
    echo "Following are intermediate files in $LOG:"
    echo $res_file $dat_file $cited_ref_file $citing_ref_file $cited_ref_res_file $citing_ref_file $cited_ref_dat_file $citing_ref_dat_file $cited_ref_link_file $citing_ref_link_file

    echo "############################"
    echo "Output excel files at $LOG:"
    echo $data_xls $cited_ref_data_xls $cited_ref_link_xls $citing_ref_data_xls $citing_ref_link_xls
