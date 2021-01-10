`find` 命令查找指定目录路径的当前全部目录

```shell
[root@192 test]# pwd
/root/test
[root@192 test]# ls /root/test
a  b  c  d  e  f  g  h.txt
[root@192 test]#  find /root/test   -maxdepth 1 -mindepth 1  -type d 
/root/test/a
/root/test/b
/root/test/c
/root/test/d
/root/test/e
/root/test/f
/root/test/g
```

同时使用 `-maxdepth 1` 与 ` -mindepth 1 ` 限定当前目录

如果不指定 `` -mindepth 1 `` 会把根目录也查找出来，见下：

```shell
[root@192 test]#   find /root/test   -maxdepth 1 -type d              
/root/test    ##这里多一层根目录
/root/test/a
/root/test/b
/root/test/c
/root/test/d
/root/test/e
/root/test/f
/root/test/g
```



