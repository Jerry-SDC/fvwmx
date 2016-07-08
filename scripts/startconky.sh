#!/usr/bin/env bash

tmp_conf=${FVWM_TMPDIR}/`basename $1`

cp -f $1 ${tmp_conf}

# CPU Model replacement
cpu_model=`awk '/model name/{for (i = 4; i <= NF; i++) printf $i" "; exit 0 }' /proc/cpuinfo`
sed -i "s/\${X_CPU_Model}/${cpu_model}/" ${tmp_conf}

# Default Gateway Interface
gwif=
for i in "1 2 3 4 5"; do
    gwif=`ip route|grep default|awk '{print $5}'`
    if [ x$gwif == x"" || x$gwif == x"\n" ]; then
        sleep 1;
    else
        break;
    fi
done
sed -i "s/template9 = .*/template9 = \[\[\${\\\\1 ${gwif}}\]\]/" ${tmp_conf}

conky -d -c ${tmp_conf}
