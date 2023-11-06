# Quick Start ROS Custom Resource

查看服务实例部署在线文档，请访问 [服务实例部署文档](https://aliyun-computenest.github.io/quickstart-demo)

本文档通过 [MkDocs](https://github.com/mkdocs/mkdocs) 生成，请参考[使用文档](https://www.mkdocs.org/getting-started/#installation) 

1）安装和使用：

```shell
$ pip install mkdocs # or use pip3 安装文档工具
$ pip install --upgrade mkdocs-aliyun-computenest # or use pip3 安装计算巢主题
$ mkdocs serve # in root folder
```
2）本地预览：本地在浏览器打开 [http://localhost:8000/](http://localhost:8000/) 。

3）本地新建分支后，提交 `Pull request` 到 `main`分支。

4）合并至 `main` 分支后，查看 pages 部署结果。

## Example

### custom_resource.example.Example1
- Shows how to customize resources, including creating, updating, deleting, and returning resource output.
- Shows how to obtain resource input properties, resource physical ID, etc.

### custom_resource.example.Example2:
Simulate a scenario:
- When creating resources, register a certain SshKey to your own service.
- When deleting, unregister the SshKey.

## How to customize resources
Similar to Example1 and Example2, you can implement custom resources by inheriting common.BaseCustomResource and implementing the corresponding interface.

## How to use custom resources
- Use the build_fc.sh script to generate a deployment package and deploy it as a function in Alibaba Cloud Function Compute.
- Use it in the template with the resource type [ALIYUN::ROS::CustomResource](https://www.alibabacloud.com/help/en/resource-orchestration-service/latest/aliyun-ros-customresource).
   - Specify Type as Custom::XXX, where XXX is the class name of the common.BaseCustomResource subclass. For example, Custom::Example1, Custom::Example2.
   - Specify the ServiceToken in Properties as the ARN of the function.
   - Specify Parameters in Properties as input properties of the corresponding custom resource class.

## Related documents
- [ROS Document](https://www.alibabacloud.com/help/en/resource-orchestration-service/latest/custom-resources)
