# ![logo](copyEsIndex.ico)欢迎使用 copyEsIndex

------

我们在使用elaticsearch的时候，经常需要依据正式环境搭建一套测试环境的ES，如果线上环境的es有大量索引的时候，手工创建将会是非常麻烦的事情；
**copyEsIndex** 就是专门为了复制和删除ES索引结构而生的，经过简单的配置你就可以快速的复制一套跟来源ES一样的索引结构，通过配置它具备以下功能：

> * 复制所有索引
> * 复制部分索引
> * 删除目标ES的全部索引
> * 删除目标ES的部分索引

### 使用说明

> * 1.下载源码运行，程序使用的是python3
> * 2.下载编译好的EXE可执行文件运行（推荐，可以省去安装依赖的过程）


------

## 一、下载源码运行

1. 使用git clone下载源码
2. 进入源码目录，运行pip install -r requirements.txt
3. 编辑配置文件 config.ini
4. 运行CopyEsIndex.py

## 二、下载可执行文件运行

1. 下载地址：
2. 编辑配置文件 config.ini
3. 运行copyEsIndex.exe


## 三、配置文件

```ini
#来源ES
[sourceES]
host = 
port = 9200

#是否需要复制目标ES现有的索引,默认复制,不复制请设置为0
isCopyIndex=1

#需要复制的索引,不设置默认为全部索引,多索引用","分隔
include=

#需要排除复制的索引,多索引用","分隔
exclude=_river

#目标ES
[targetES]
host = 
port = 9200

#是否删除目标ES现有的索引,默认不删除,需要删除请设置为1
isDeleteIndex=0

#需要删除的索引,不设置默认为全部索引,多索引用","分隔
include=

#需要排除删除的索引,多索引用","分隔
exclude=
```