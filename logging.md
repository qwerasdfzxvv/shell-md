## python logging 使用总结

### 主要注意事项

- 如果开发代码包为基础公共资源，例如开源包，禁止使用`logging.basicConfig()` 因为它只初始化一次，全局的引用 ，一旦定制其它人就没折定制样式；
- 官方推荐使用：`logger = logging.getLogger(__name__)`, 原因：`__name__` 当前模块名称，实例对象以命名空间来区分，单 例不会产生冲突；

# 常见使用方式

- 简单明确，官方推荐，开源项目爱用的方式。
  [apache/superset](https://github.com/apache/superset/blob/master/superset/app.py)

```python
import logging
import os

from flask import Flask

from superset.initialization import SupersetAppInitializer

logger = logging.getLogger(__name__)
```

 一句声明就够用。它的精髓：胡里花哨的日志格式，自个定义，我不参与，我只关注自己的代码质量。

- 某些有洁癖开发者自己也爱胡里花哨日志格式，又不想影响引用者，也可自定义一段格式。

```python
import logging

logger = logging.getLogger(__name__)

# handler = logging.FileHandler(filename='app.log', mode='a', encoding='utf-8')
handler = logging.StreamHandler()
handler.setFormatter(
    logging.Formatter('[%(asctime)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s'))
logger.addHandler(handler)

logger.warning("warning")
```

```python
[2023-06-03 19:23:57,733] [WARNING] [ dd.py:11 - __main__ ] warning
```

  这样的格式日志能满足大部分开发者，同时不影响引用者，引用者还是可以根据自己的洁癖美化日志 

- 超强扩展字段

```python
import logging
import socket

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='app.log', mode='a', encoding='utf-8')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] [%(hostname)s] [%(levelname)s] [ %(filename)s:%(lineno)s - %(name)s ] %(message)s '))
logger.addHandler(handler)

hostname = socket.gethostname()

factory = logging.getLogRecordFactory()


def record_factory(*args, **kwargs):
    record = factory(*args, **kwargs)
    record.hostname = hostname
    return record


logging.setLogRecordFactory(record_factory)

logger.info('log-info')
logger.error('log-error')
```

  在分布式架构，日志添加服务器名称`hostname`标识至关重要。`LogRecordFactory` 方式就很好满足要求，谁用谁知道。



# 小结

 日志重要，记住上面几点足够。
