# png2heic 自动转换图片到heic
因为在网上没有找到将图片转为heic的工具，都是将heic转为jpg或是png的  
写了一个python3的脚本，方便放在性能强大的m1 mac上和linux上跑，同时也支持Window  
会保留原目录树，修改日期以及exif图片信息，保留图片细节的情况下大量的减少空间占用，jpg的大小，png的画质  
几乎无损的压缩，肉眼无法分辨  

### 仅需安装依赖，修改路径，默认的配置即可达到全平台完美的兼容性和极致的大小，并且拥有非常棒的质量  
依赖ffmpeg mp4box exiftool 这三个命令行程序，如何安装请看py文件顶部注释

色域使用yuv444 10bit，这样图片细线就不会模糊整体不会偏白，yuv420则可以保证全平台兼容性  
crf提升到10，0效果最好也最大，推荐5或者10，原图质量差的建议数字小点不然灰暗区域有色块  
另外可以多开实现多线程处理，加快处理速度，会自动跳过已处理好的，临时文件也会自动区分  
gif会转成webp，能节省一半空间，用浏览器打开会动，而且支持透明度  
heic不支持透明，因为hevc没有透明，后续考虑支持检测透明png直接复制或是转成支持透明的webp（因为主要转的都是视频截图所以问题不是很大）  
使用cpu压缩，保证最好的画质，硬件加速虽然快但是会使文件更大，质量更差

另外使用golang写了个有损图片压缩工具，支持png和jpg，无需任何依赖  
https://github.com/zanjie1999/mecopy

# 安装依赖
看png2heic.py文件头部，想必没什么人真的会看文档，如果你看了，那还[有个视频教你如何在Windows下安装](https://www.bilibili.com/video/BV1jefDYfEiB)  
配置好了直接运行就会自动转换

# windows的heic支持
在微软自带的商店安装heif插件  
在cmd运行 `start ms-windows-store://pdp/?ProductId=9n4wgh0z6vhq` 安装hevc插件  
即可用自带的图片来查看，缩略图也有  
ltsc可以自行把商店补上再进行这些操作
