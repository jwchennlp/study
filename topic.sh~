#!/bin/bash

echo 现在处理topic文件

echo 将两个train.tsv 和 test.tsv 合并，写入到total.txt中

cd ~/kaggle/class/

python ~/kaggle/class/readfile.py

echo 合并完成

echo mallet读入数据

cd ~/study/mallet-2.0.7/

./bin/mallet import-file --input ~/kaggle/class/total.txt --output topic-input.mallet --keep-sequence --remove-stopwords 

echo 读取数据完成

echo 开始建立topic文件

./bin/mallet train-topics --input topic-input.mallet --optimize-interval 10 --optimize-burn-in 30 --num-topics 35 --num-iterations 400 --output-state topic-state.gz --output-doc-topics ~/kaggle/class/class.topic --output-model ~/kaggle/class/shabi.txt

echo topic文件建立完毕

echo 分割成两个文件

cd ~/kaggle/class/

python readtopic.py

echo 分成两个文件完毕

python lda.py
