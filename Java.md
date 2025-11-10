# 1、语法

**局部变量存储在JVM虚拟机的栈上，实例变量存储在堆上**

**方法重载？方法重写**

**方法的基本数据原理？**

**引用数据类型？**

**静态方法**

```
可以通过类名或接口名直接调用
接口静态方法不能被重写，类中子父类同名的静态方法是同时存在。
静态方法中没有this和super
```

**JavaBean类、测试类、工具类**

**构造方法私有化的意义？**

构造方法就是为了初始化对象

**实例变量**

```
不让创建对象
```

**子类可以继承父类的什么东西？虚方法表？**

**构造方法的特点？**

```
父类的构造方法不会被子类继承.
子类中所有的构造方法默认先访问父类的无参构造，再执行自己的构造方法.
子类的构造方法中有一个默认的super().
父类的有参构造要手动的书写.
```

**this和super？**

```
this和super不仅可以用于访问本类的成员变量和成员方法，也可以用于访问本类的构造方法
```

**堆、栈、方法区？静态变量存储到哪里？**

```
堆：执行的一个个函数和方法是要进栈的，这个通过递归很好理解。
栈：创建的对象是存储在栈里面的。
方法区：跟字节码文件有关，若要使用一个类，就要将这个类的字节码文件加载到方法区。
```

**多态中，使用父类型作为参数，可以接受所有的子类对象？**

```
子类对象可以被当作父类类型来使用
```

**final**

```
修饰方法则该方法不可被子类重写
修饰变量则成为常量
修饰类则该类不能有子类
```

**权限修饰符**

|           | 同一类中 | 同一包中 | 不同包中子类 | 不同包中无关类 |
| :-------: | :------: | :------: | :----------: | :------------: |
|  private  |    ✅️     |          |              |                |
|    空     |    ✅️     |    ✅️     |              |                |
| protected |    ✅️     |    ✅️     |      ✅️       |                |
|  public   |    ✅️     |    ✅️     |      ✅️       |       ✅️        |

**interface**

接口定义的就是一种规则

```
接口中定义方法分为有方法体和没有方法体的
有方法体的是默认default和静态static方法，以及私有private方法，默认方法可以重写，静态方法不能重写，私有方法（分普通和静态）不对外提供。
没有方法体的是abstract抽象方法，必须重写	
```

**适配器设计模式**

**内部类**

```
成员内部类：
内部类也有一系列诸如private的权限修饰符，作用范围的规则不变。
如设置为private后无法被外部创建内部类对象，但可以通过方法来返回一个内部类对象。
外部类和内部类是两个独立的字节码文件
外部类和内部类若有同名属性，则外部类需要outer.this.a

匿名内部类：
接口是实现关系
类则是继承关系

静态内部类：
任何静态类或静态方法里面都只能使用静态属性

局部内部类：
```



# 2、IDEA操作

可以点击文件的项目结构设置JDK，将语言级别设置为和JDK匹配的版本（编译的版本）。

shift + F2 定位到下一个报错的地方

alt+6 当前的错误列表展示

<u>ctrl + N</u> 可以搜索类

ctrl + F12 看到一个类中的详细属性和方法

<u>ctrl +alt + m</u> 快捷设置方法

Ctrl+ b 进入一个方法中

<u>arr.fori</u> 快速生成for循环

快速遍历：

```
for (元素类型 变量名 : 数组或集合) {
    // 循环体
}
```

# 3、实用类

### 1、时间

我们的计算机有时间原点，国际是从1970年1月1日0时0分0秒开始的，咱们东八区是从1970年1月1日8时0分0秒开始。

**创建当前时区时间对象**

    DateTimeFormatter formatter=DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
    ZoneId zoneId = ZoneId.of("Asia/Shanghai");
    ZonedDateTime zonedDateTime = localDateTime.atZone(zoneId);
    String formattedDateTime = zonedDateTime.format(formatter);
    System.out.println("格式化后的时间 (" + zoneId + "): " + formattedDateTime);

**创建当前时间对象**

```
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
LocalDateTime localDateTime = LocalDateTime.parse(dateStr, formatter);
LocalDateTime now = LocalDateTime.now();
String nowStr=now.format(formatter);
```

**将时间字符串实例化为时间对象**

```
String dateStr = "2024-05-15 14:30:25";
DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");
LocalDateTime localDateTime = LocalDateTime.parse(dateStr, formatter);
```

**计算时间间隔**

```
Instant now = Instant.now();  // 获取当前时间戳
System.out.println(now);

try {
    Thread.sleep(3 * 1000);
    } catch (InterruptedException e) {
     	e.printStackTrace();
    }
    
Instant next = Instant.now();  // 获取当前时间戳
System.out.println(next);

Duration duration = Duration.between() //时间间隔
```

**获取当前时间的毫秒值**

```
System.currentTimeMillis();//获取当前时间的毫秒值
Instant now = Instant.now();//获取当前时间戳
```
