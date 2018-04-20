# Shell脚本编程基础
### shell概念:
 shell是一个用C语言编写的程序,他是用户使用Linux的桥梁,它是一种命令语言,同事也是一种编程语言.用户可以通过Shell访问操作系统和内核服务.Linux的Shell种类众多,Bash是大多数Linux系统默认的Shell,所以我以Bash为例学习shell脚本编程.
* * *
### shell变量:
**变量的命名**
>1.  命名只能使用,字母/数字/下划线
>2.  中间不能有空格
>3.  不能使用标点符号
>4.  不能与关键字重合
**变量操作**
>1. 使用: $变量名 或者 ${变量名}
'''
	#!/bin/bash
	a=4
	b=5
	c=\`expr $a + $b\`
	echo $c
'''
>2. 设置只读变量: 变量名 readonly
>3. 删除变量: unset 变量名
**shell中常用数据类型**
>1. 字符串: 
*  可以使用单引号也可以使用双引号,单引号表示原样字符串,单引号中变量或者转义符都会无效,单引号里也不能出现单引号;
*  提取字符串长度 ${#变量名}
*  字符串切片 ${变量名:开始位置:结束位置}
'''
	str1='abc'  
	str2="$str1"
	str3='$str1'
	echo $str1 $str2 $str3 #输出abc abc $str1
	echo ${#str1} #输出3
	echo ${str1:1:2} #输出bc 开始位置1 结束位置2 编程语言中一般都是以0是开始的
'''
>2. 数组:
*  数组的定义: 变量名=(值1 值2... 值n)
*  数组的读取: ${变量名[下标]} 或 取所有元素用${变量名[@]}
*  数组的长度: ${#变量名}
'''
	array1=(1 3 5 7 9) #注意数组中每个值用空格隔开而不是逗号
	echo $array1  #输出1 默认下标0
	echo ${array[4]}  #输出9
	echo ${array1[@]}  #输出1 3 5 7 9
	echo ${#array1[@]} #输出5
	echo ${#array1}  # 输出1 取的是单个元素 默认的下标是0 单个元素长度为1
''' 
>3. 注释:
*  以#开头的就是注释,会被解释器直接忽略

**shell传参**
<table>
<tr><td>参数处理</td><td>说明</td> 	</tr>
<tr><td>$# </td><td>	传递到脚本的参数个数</td></tr>
<tr><td>$\*</td><td>以一个单字符串显示所有向脚本传递的参数。如"$\*"用「"」括起来的情况、以"$1 $2 … $n"的形式输出所有参数。</td></tr>
<tr><td>$$ </td><td>脚本运行的当前进程ID号</td></tr>
<tr><td>$! </td><td>后台运行的最后一个进程的ID号</td></tr>
<tr><td>$@ </td>	<td>与$\*相同，但是使用时加引号，并在引号中返回每个参数。如"$@"用「"」括起来的情况、以"$1" "$2" … "$n" 的形式输出所有参数。</td></tr>
<tr> <td>$-</td><td>显示Shell使用的当前选项，与set命令功能相同。</td></tr>
<tr><td>$?</td><td>显示最后命令的退出状态。0表示没有错误，其他任何值表明有错误。</td></tr>
</table>

**shell运算符**
由于原声bash不支持简单的数学运算,但是可以通过其他命令实现,例如awk/expr,其中expr最常用,expr是一款表达式计算工具,使用时要用撇号\`包起来(撇号就是键盘上1左边的那个),而且需要注意的是它有严格的语法规范,表达式与运算符之间一定要有空格!例如\`expr $a + $b\`是对的,但是\`expr $a+$b\`是错误的!
>1. 算数运算符:

<table>
<tr>
	<td>运算符</td>
	<td>说明</td>
	<td>举例</td>
</tr>
<tr>
	<td>+</td>
	<td>加法</td>
	<td>`expr $a + $b`</td>
</tr>
<tr>
	<td>-</td>
	<td>减法</td>
	<td>`expr $a - $b`</td>
</tr>
<tr>
	<td>*</td>
	<td>乘法</td>
	<td>`expr $a \* $b`</td>
</tr>
<tr>
	<td>/</td>
	<td>除法</td>
	<td>`expr $a / $b`</td>
</tr>
<tr>
	<td>%</td>
	<td>取余</td>
	<td>`expr $a % $b`</td>
</tr>
<tr>
	<td>=</td>
	<td>赋值</td>
	<td>a=$b</td>
</tr>
<tr>
	<td>==</td>
	<td>相等</td>
	<td>$a == $b 判断是否相等 相等返回true 不相等返回false</td>
</tr>
<tr>
	<td>!=</td>
	<td>不相等</td>
	<td>$a != $b 相等返回false 不相等返回true</td>
</tr>
</table>

>2. 关系运算符
关系运算符只支持数字,不支持字符串,除非字符串的值是数字.

<table>
<tr>
	<td>运算符</td>
	<td>说明</td>
</tr>
<tr>
	<td>-eq</td>
	<td>检测两个数是否相等,相等返回true</td>
</tr>
<tr><td>-ne</td>
	<td>检测两个数是否不等于,不等返回true</td>
</tr>
<tr>
	<td>-gt</td>
	<td>检测左边的数是否大于右边的,是就返回true</td>
</tr>
<tr>
	<td>-lt</td>
	<td>检测左边的数是否小于右边的,是就返回true</td>
</tr>
<tr>
	<td>-ge</td>
	<td>检测左边的数是否大于等于右边的,是就返回true</td>
</tr>
<tr>
	<td>-le</td>
	<td>检测左边的数是否小于等于右边的,是就返回true</td>
</tr>
</table>
>3. 布尔运算:
	! : 非运算符,[!true] 返回false
	-o: 或运算符,任一true 返回true 
	-a: 与运算符,任一为false 返回false


>4. 逻辑运算符:
	&& 逻辑的AND
	|| 逻辑的OR

>5. 字符串运算符
	= 	检测两个字符串是否相等，相等返回 true。 
	!= 	检测两个字符串是否相等，不相等返回 true。 	
	-z 	检测字符串长度是否为0，为0返回 true。 
	-n 	检测字符串长度是否为0，不为0返回 true。 
	str 检测字符串是否为空，不为空返回 true。 举例 a='abc' [$a]返回ture

**shell命令**
>1. shell echo命令: 用于字符串的输出
*  echo abc 和 echo "abc" 是一样的
*  可以显示普通字符串\转义字符\变量
	echo "Hello world"  #返回Hello world
	text="Hello world"  
	echo $text          #返回Hello world
	echo \"Hello world\"#返回"Hello world"
*  可以定向至文件
	echo "Hello world" > test.log   会将"Hello world"定向输出到test.log中
*  可以显示命令执行结果
	echo `data`    #注意是撇号,结果将显示目前的日期

>2. shell printf命令:
*  可以格式化字符串输出 格式替代符(%s %c %d %f)
*  可以转义序列
	\a 警告字符
	\b 后退
	\c 抑制,结尾不换行且后面的格式字符串中的字符都会被忽略
	\f 换页
	\n 换行
	\r 回车
	\t 水平制表符
	\v 垂直制表符
	\\ 一个\


**shell 循环与分支**
>1. 分支: if 和 if else 和 if elif else
	if 条件语句
	then
		条件为真执行语句
	fi
	也可以这样写为一行:if 条件语句; then 条件为真执行语句;fi

	if 条件语句
	then 
		条件为真执行语句
	else
		条件为假执行语句
	fi

	if 条件1语句
	then
		条件1为真执行语句
	elif 条件2语句
	then
		条件2为真执行语句
	else
		条件1与条件2都为假执行语句
	fi

>2. 循环语句 for循环 while循环 until循环 case循环
跳出循环break 跳出本次循环 continue

	举例说明:返回0到100的整数和
	#! /bin/bash
	sum=0
	for ((i=0; i<=100; i++))
	do
		sum=`expr $sum + $i`
	done
	echo $sum  #返回5050

	#! /bin/bash
	i=0
	while(($i<=3))
	do
		echo $i
		let "i++"
	done
	运行脚本,输出:
	0
	1
	2
	3

