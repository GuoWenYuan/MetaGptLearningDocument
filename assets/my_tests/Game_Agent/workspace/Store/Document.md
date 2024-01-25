# 游戏商城系统技术文档

## 1. 概述

本文档旨在指导开发人员实现游戏内的商城系统，包括魔石商城和兑换商店。系统将允许玩家使用不同的货币购买商品，支持商品搜索、历史购买快捷回购、商品详情展示等功能。

## 2. 系统架构

### 2.1 MVC架构

- **Model**：负责数据的存储、检索和管理，包括商品信息、货币信息和玩家购买历史等。
- **View**：负责展示用户界面，包括商城界面、商品展示、购买弹窗等。
- **Controller**：负责处理用户输入，执行业务逻辑，如购买商品、搜索商品等。

### 2.2 类和接口设计

#### 2.2.1 商城管理器（ShopManager）

- 负责商城的整体逻辑控制。
- 方法：
  - `OpenShop(ShopType type)`：打开指定类型的商城。
  - `CloseShop()`：关闭当前商城。
  - `PurchaseItem(int itemId, int quantity)`：购买指定商品。
  - `SearchItems(string keyword)`：搜索商品。

#### 2.2.2 商品类（Commodity）

- 存储商品的基本信息和状态。
- 属性：
  - `int id`：商品ID。
  - `string stringId`：商品字符串ID，用于国际化。
  - `string name`：商品名称。
  - `string description`：商品描述。
  - `float price`：商品价格。
  - `int stock`：商品库存。
  - `bool isOnSale`：商品是否在售。
  - `DateTime saleEndTime`：销售结束时间。

#### 2.2.3 货币类（Currency）

- 存储货币的基本信息。
- 属性：
  - `int id`：货币ID。
  - `string stringId`：货币字符串ID，用于国际化。
  - `string name`：货币名称。
  - `int amount`：玩家持有的货币数量。

#### 2.2.4 商城界面（ShopView）

- 负责商城界面的显示和用户交互。
- 方法：
  - `ShowShop(ShopType type)`：展示指定类型的商城。
  - `UpdateCommodityList(List<Commodity> commodities)`：更新商品列表。
  - `ShowPurchasePopup(Commodity commodity)`：显示购买弹窗。

#### 2.2.5 网络协议

- 使用Protobuffer定义网络协议。
- 协议内容：
  - `ShopRequest`：请求打开商城、购买商品等。
  - `ShopResponse`：返回商城数据、购买结果等。

### 2.3 配置文件

#### 2.3.1 商品表（Commodity_商品表）

- 包含所有商品的配置信息。
- 字段：
  - `int id`：商品ID。
  - `string stringId`：商品字符串ID。
  - `string name`：商品名称。
  - `string description`：商品描述。
  - `float price`：商品价格。
  - `int stock`：商品库存。
  - `DateTime saleEndTime`：销售结束时间。

#### 2.3.2 商城页签表（ShopType_商城页签表）

- 配置商城页签信息。
- 字段：
  - `int id`：页签ID。
  - `string stringId`：页签字符串ID。
  - `string name`：页签名称。
  - `List<int> commodityIds`：该页签下的商品ID列表。

#### 2.3.3 商城表（Shop_商城表）

- 配置商城的基本信息。
- 字段：
  - `int id`：商城ID。
  - `string stringId`：商城字符串ID。
  - `string name`：商城名称。
  - `List<int> shopTypeIds`：商城包含的页签ID列表。

## 3. 功能实现

### 3.1 商城入口

- 实现商城入口的点击事件，根据功能开启表判断并显示对应的商城页签。

### 3.2 商城界面逻辑

- 商城页签的默认显示、商品的点击购买、搜索功能等。

### 3.3 页签功能

- 实现页签的选中、悬浮、未选中状态切换，以及页签下商品的显示逻辑。

### 3.4 商品展示

- 实现商品的基本信息展示、购买条件判断、限购逻辑等。

### 3.5 购买逻辑

- 实现商品购买弹窗的显示、购买操作和购买结果处理。

## 4. 杂项

- 红点规则、死亡复活判断、聊天窗口显示等相关逻辑。

## 5. 附录

### 5.1 Protobuffer定义示例

```protobuf
message ShopRequest {
  required int32 shop_id = 1;
  optional int32 item_id = 2;
  optional int32 quantity = 3;
}

message ShopResponse {
  required int32 result = 1;
  repeated Commodity commodities = 2;
}

message Commodity {
  required int32 id = 1;
  required string stringId = 2;
  required string name = 3;
  required string description = 4;
  required float price = 5;
  required int32 stock = 6;
  required bool isOnSale = 7;
  required string saleEndTime = 8;
}
```

### 5.2 配置文件示例

```json
{
  "Commodity_商品表": [
    {
      "id": 1001,
      "stringId": "item_1001",
      "name": "神秘宝箱",
      "description": "打开可获得随机奖励",
      "price": 99.9,
      "stock": 1000,
      "saleEndTime": "2023-12-31T23:59:59"
    }
  ],
  "ShopType_商城页签表": [
    {
      "id": 1,
      "stringId": "tab_1",
      "name": "热销商品",
      "commodityIds": [1001, 1002]
    }
  ],
  "Shop_商城表": [
    {
      "id": 1,
      "stringId": "shop_1",
      "name": "魔石商城",
      "shopTypeIds": [1, 2]
    }
  ]
}
```

请根据此技术文档进行架构图制作与代码编写。