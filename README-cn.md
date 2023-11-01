# 快速开始：ROS自定义资源

## 示例

### custom_resource.example.Example1
- 展示了如何自定义资源，包括创建、更新、删除、返回资源输出。
- 展示了如何获取资源输入属性、资源物理ID等。

### custom_resource.example.Example2：
模拟一个场景：
- 创建资源时，把某个SshKey注册到自己的服务。
- 删除时，反注册该SshKey。

## 如何自定义资源
类似Example1和Example2，继承common.BaseCustomResource并实现相应的接口，即可实现自定义资源。

## 如何使用自定义资源
- 使用build_fc.sh脚本可以生成部署包，并在阿里云函数计算中部署为函数。
- 配合资源类型[ALIYUN::ROS::CustomResource](https://help.aliyun.com/document_detail/145579.html)在模板中使用。
  - 指定Type为Custom::XXX，其中XXX为common.BaseCustomResource子类的类名。例如Custom::Example1、Custom::Example2。
  - 指定Properties中的ServiceToken为函数的ARN。
  - 指定Properties中的Parameters为相应自定义资源类的输入属性。

## 相关文档
- [ROS文档](https://help.aliyun.com/document_detail/145907.html)
- [资源编排ROS之自定制资源（基础篇）](https://developer.aliyun.com/article/740364)
- [资源编排ROS之自定制资源（多云部署AWS篇）](https://developer.aliyun.com/article/740198)
- [资源编排ROS之自定制资源（多云部署Terraform篇）](https://developer.aliyun.com/article/740363)