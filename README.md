# Quick Start: ROS Custom Resource

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
