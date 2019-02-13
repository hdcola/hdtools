# Google Cloud Vision Request

这是帮一个朋友把文档OCR出来的一个小工具，使用了Google Cloud来进行转换，它主要有几个特性：

* 只输出识别出来的txt
* 在当前目录下建议一个缓存，按图片的文件名将OCR后的JSON缓存下来，缓存目录就是你运行程序的当前目录，你可以设置优先使用缓存

## 环境

* Python 3
* pip安装 request

## 运行方法

```python gvisionreq.py [-ct] [-k key]  [file ...]```

参数说明：

-c --cache 优先使用缓存中的文件进行识别

-t --text 不再输出JSON格式，只输出纯文本内容

-k --key 设置你的google cloud access token key

## 示例

* 使用mykey请求转换IMG_1024.JPG

```python gvisionreq.py -k mykey IMG_1024.JPG```

* 使用mykey请求转换IMG_1024.JPG只输出识别的文本

```python gvisionreq.py -t -k mykey IMG_1024.JPG```

* 使用mykey请求转换IMG目录下的所有文件，如果有已经请求过缓存就使用本地缓存，并将文本存入 out.txt 文件中去。

```python gvisionreq.py -t -c -k mykey ./IMG/* > out.txt```

我就是使用上面这个方法来识别了几百页的一份文件，省心省力！

## 已知问题

* 照片模糊或者无法识别

这时你会得到一个错误提示：

```Traceback (most recent call last):
  File "/Users/hd/work/hdtools/gvisionreq/gvisionreq.py", line 99, in <module>
    t = resp['textAnnotations'][0]
KeyError: 'textAnnotations'
```

去你的```jsons```缓存目录中找到最后一个文件，这时你会看到文件里只有一个空的 ```{}``` ，去源目录删除对应的文件和生成的json文件，利用已有的cache继续工作就好。