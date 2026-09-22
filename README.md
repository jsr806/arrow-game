# 一箭又一箭小游戏
## 项目简介
本项目是基于Python + Pygame开发的点击式箭头解谜小游戏。玩家点击箭头，程序检测箭头前进方向；前方无障碍物则箭头飞出棋盘消除；有阻挡则触发碰撞提示并扣除失误次数。清除所有箭头通关，失误耗尽本关失败。包含3个可通关关卡，支持重开关卡、关卡切换。

## 开发环境
- Python 3.8及以上
- Pygame库

## 安装与运行
1. 安装依赖库
```bash
pip install pygame
git clone https://github.com/JSR806/arrow-game.git
python main.py

## 游戏操作说明
1. 打开程序，在开始界面点击【开始游戏】进入关卡
2. 使用鼠标点击棋盘上的箭头
3. 箭头前方无阻挡：箭头飞出消失
4. 箭头前方有阻挡：箭头晃动提示，扣除1次失误机会
5. 界面会显示：当前关卡、剩余箭头数量、剩余失误次数
6. 点击【重新开始】按钮重置当前关卡
7. 清空所有箭头自动通关，进入下一关；失误次数用完游戏失败

## 游戏截图
![开始界面](screenshots/start.png)
![游戏界面](screenshots/game.png)
![通关界面](screenshots/win.png)
![失败界面](screenshots/lose.png)
