#!/usr/bin/env bash

CRONTAB_CMD="*/5 * * * * flock -xn /home/emall/echo_test.lock -c 'sh /home/emall/echo_test.sh >>/home/emall/echo_test.log'"

#新增
crontab_add() {
  if ! crontab -l | grep -F "$CRONTAB_CMD"; then
  {
    crontab -l
    echo "$CRONTAB_CMD"
  }|crontab -
  else
    echo "crontab已经存在：$CRONTAB_CMD"
  fi
}


#删除
crontab_del() {
  crontab -l | grep -Fv "$CRONTAB_CMD" | crontab -
}

#注释
crontab_comment() {
  if crontab -l | grep -F "$CRONTAB_CMD"; then
  {
    crontab -l|grep -Fv "$CRONTAB_CMD"
    echo "#$CRONTAB_CMD"
  }|crontab -
  else
    echo "crontab不存在：$CRONTAB_CMD"
  fi
}

#取消注释
crontab_umcomment() {
  if crontab -l | grep -F "#$CRONTAB_CMD"; then
  {
    crontab -l|grep -Fv "#$CRONTAB_CMD"
    echo "$CRONTAB_CMD"
  }|crontab -
  else
    echo "crontab不存在：#$CRONTAB_CMD"
  fi
}
#crontab_add
#crontab_del
#crontab_comm
#crontab_umcomment


