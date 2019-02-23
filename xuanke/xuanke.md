# pku选课

## 项目介绍：
选课系统

## 总体设计
- 只有根目录下config允许从local_config导入配置，其余必须从config而非local_config导入配置 

##  目录说明    
├── xuanke //选课系统       
│   ├── utils  //相关工具     
│   │   ├── chromedriver_mac //chrome mac驱动            
│   │   ├── chromedriver_win //chrome windows驱动            
│   │   └── phantomjs_linux //phantomjs linux驱动           
│   ├── config.py  //配置文件  
│   ├── info.py  //信息通知    
│   ├── local_config.py  //本地配置，密码等私密信息    
│   ├── manage.py  //入口文件   
│   ├── validcode.py  //验证码识别   
│   ├── xuanke.md  //说明文档  
│   └── xuanke.py  //选课系统主逻辑 


## 部署
      新建 xuanke/utils目录，下载相应平台的 phantomjs或者 chromedriver
      并将名字改为config文件指定名
      pip install -r requirements.txt
      

## 运行
     将账号密码修改为自己的
     python3 manage.py

