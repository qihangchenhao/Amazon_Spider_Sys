# Amazon_Spider_Sys
Amazon Spider 亚马逊商品信息抓取系统，包含商品监控模块，商品评价监控模块，商品库存监控系统，评论词云模块，用户管理模块

### 初始版本说明，爬虫采用Selenium，模块化设计不够完善，需要手动增加代理IP。

### 最新版本介绍,采用全API无cookies用户抓取，毫秒级识别验证码，摒弃所有selenium抓取（多用户隔离版本），无需代理IP，节点一键动态部署。
#### 公有云地址www.awscrawl.com
#### 作者WX:572346030
* 用户模块：（管理员可增删改查子账号）

* 商品监控模块：商品基本信息监控（包含名称、五点特征、价格、Q&A）信息均每日更新，支持导出excel

* 商品评价监控功能（包含评价者、评价时间、评价星级）信息均为手动维护更新说白了就是自己想更新一下a商品的OneStar在相应页面提交即可，支持导出excel

* 商品库存监控系统（包括商品每日的库存信息跟抓，因为有部分商品库存超过1000只显示1000，以及部分商品限购x件，即只显示x件，含有商品每日的评价数量，价格，星级监控）支持导出excel

* 评论词云功能 可选定指定商品，指定星级生成评论词云（词越大，出现频率越高）


excel示例报表链接:
Q&A：https://pan.baidu.com/s/1Dkjhjap8W7yaGnsbxfQzhw
Rete：https://pan.baidu.com/s/1HVWE0OQ8-1J-efpZpoJfSg
Base-Info：https://pan.baidu.com/s/1ax3tYm_QNsqWJcoek4O7cw
