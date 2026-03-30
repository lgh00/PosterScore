# 这个项目实现了对一个海报从内容，组织，认知效用等多个维度进行评估。

## 使用前的准备工作
* 创建一个.env文件，放入API Key和Base URL
* 在data目录下放入海报图片，论文文件
  
## 使用方法
```bash
python src/main.py --paper_path data/paper.pdf --poster_path data/poster.png --model doubao-seed-2-0-lite-260215
```