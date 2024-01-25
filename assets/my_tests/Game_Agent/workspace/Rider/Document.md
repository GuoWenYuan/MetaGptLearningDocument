# 坐骑系统技术文档

## 概述

本文档旨在详细描述坐骑系统的技术实现方案，包括前端的界面逻辑、后端的数据处理以及网络通信协议。坐骑系统允许玩家解锁、骑乘幻兽坐骑，并进行偏好设置。玩家可以在游戏内通过快捷键快速召唤坐骑。系统需要支持自动骑乘、偏好坐骑选择、坐骑传记查看、限时坐骑处理等功能。

## MVC架构设计

### Model

- `MountModel`
  - `List<MountData> mounts`：所有坐骑的数据列表。
  - `MountData preferredMount`：当前偏好坐骑数据。
  - `bool isAutoRideEnabled`：是否启用自动骑乘。

### View

- `MountView`
  - 展示坐骑列表、坐骑详细信息、骑乘设置等。
  - 提供偏好设置的交互界面。
- `MountRideWheelView`
  - 显示偏好坐骑轮盘，供玩家选择偏好坐骑。

### Controller

- `MountController`
  - 处理玩家的坐骑相关操作请求。
  - 与Model交互更新数据，与View交互更新界面。

## 功能模块

### 坐骑功能入口

- 主界面增加“偏好”按钮，点击后显示子页签“坐骑”。
- 坐骑按钮点击后，默认显示坐骑功能界面。
- 功能开启配置在功能开启表中设置。

### 坐骑列表

- 坐骑列表按照当前骑乘、偏好池、品质、已解锁、未解锁的顺序排序。
- 列表底部提供偏好设置和自动骑乘开关按钮。

### 坐骑展示

- 展示坐骑的基本信息、技能、骑乘设置和动作查看。
- 提供骑乘、收回、前往获取等操作按钮。

### 技能展示

- 通过幻兽配置表中的SkillList字段展示坐骑技能。
- 玩家可将技能拖拽到快捷栏。

### 骑乘设置

- 提供地面和飞行骑乘设置，两者互斥。

### 坐骑传记

- 点击坐骑名称旁的“传记按钮”弹窗显示坐骑传记。

### 偏好设置

- 点击“快捷坐骑”按钮呼出偏好轮盘，玩家可拖拽坐骑到轮盘进行设置。

### 限时坐骑

- 限时坐骑在坐骑栏显示倒计时提示。

### 解锁、骑乘状态变更提示

- 新解锁坐骑或骑乘状态变更时，在主界面通用信息区域显示提示。

### 骑乘规则

- 玩家可通过快捷键执行手动骑乘逻辑。

## 网络协议

使用Protobuf定义以下网络协议：

```protobuf
syntax = "proto3";

package mount;

// 请求骑乘坐骑
message RideMountRequest {
  int32 mountId = 1;
}

// 响应骑乘坐骑
message RideMountResponse {
  bool success = 1;
  string message = 2;
}

// 请求设置偏好坐骑
message SetPreferredMountRequest {
  int32 mountId = 1;
}

// 响应设置偏好坐骑
message SetPreferredMountResponse {
  bool success = 1;
  string message = 2;
}

// 请求坐骑数据
message GetMountDataRequest {
}

// 响应坐骑数据
message GetMountDataResponse {
  repeated MountData mounts = 1;
}

// 坐骑数据
message MountData {
  int32 id = 1;
  string name = 2;
  bool isUnlocked = 3;
  bool isPreferred = 4;
  int32 runSpeed = 5;
  int32 flySpeed = 6;
  repeated string skillList = 7;
  string access = 8;
  string desc = 9;
}
```

## 配置文件

配置文件定义坐骑的属性和获取途径。

```json
[
  {
    "id": 1,
    "stringId": "mount_fire_dragon",
    "name": "火焰龙",
    "isUnlocked": true,
    "isPreferred": false,
    "runSpeed": 120,
    "flySpeed": 150,
    "skillList": ["fire_breath", "wing_flap"],
    "access": "quest_reward",
    "desc": "一只烈焰中诞生的龙，拥有炽热的气息。"
  },
  // 更多坐骑配置...
]
```

## 结语

本技术文档提供了坐骑系统的详细设计方案，包括MVC架构的设计、功能模块的描述、网络协议的定义以及配置文件的格式。开发人员可以根据本文档进行架构图制作和代码编写。