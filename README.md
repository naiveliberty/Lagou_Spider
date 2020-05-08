# 拉钩网职位爬虫

### 声明：项目内容不得用于商业用途，仅做学习交流，如果侵犯了您的利益和权益,请邮箱联系我，我将删除该项目。

| 作者    | 邮箱                                                |
| ------- | --------------------------------------------------- |
| liberty | [fthemuse@foxmail.com](mailto:fthemuse@foxmail.com) |

以下我爬拉钩网时遇到的问题和解决办法，希望能帮助到大家：
拉钩网的反爬措施：

- js 反爬；
- ip 地址反爬；



## 拉钩网 js 反爬分析过程：

1. 在访问拉勾职位详情页面时，拉钩服务器后端会校验 cookie 中键值为 X_HTTP_TOKEN 的值，检验通过后返回正确的页面，失败返回 302 页面;
2. 当我们用浏览器访问详情页面的时候，浏览器会自动运行页面中的 js 代码，动态生成这个值，并添加到请求头的 cookie 中;
3. 当我们用 requests 或者 scrapy 框架爬取时，不会动态加载执行页面中的 js 代码，所有 request 头部的 cookie 中没有生成这个字段，请求拉钩后端时，校验不通过，返回 302 页面；



## js反扒爬：

1. 逆向分析页面中 js 代码，找到 X_HTTP_TOKEN 生成的过程，使用 python 代码复现这个过程；
2. 每次请求之前在 cookie 中加上这个字段。



## ip 反爬：

1.购买代理池或使用免费代理，但是网上免费的IP代理可用度比较差；

2.在未使用代理的情况下，可以降低并发数量。



稳定的解决方法就是：代理池 + 动态生成 X_HTTP_TOKEN

