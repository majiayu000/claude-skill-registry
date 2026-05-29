---
layout: post
title: STL必会
categories: CPP
---
C++ STL技巧
==========
1 使用`copy`算法来输出数组
`copy(vec.begin(),vec.end(),ostream_iterator<string>(cout," "));`  
2 使用自定义`split`来分割字符串  
{% highlight c++ %}
//字符串分割函数,str表示被分割的字符串,pattern是分隔符  
vector<std::string> split(std::string str,std::string pattern)  
{  
     std::string::size_type pos;  
     std::vector<std::string> result;  
     str+=pattern;//扩展字符串以方便操作  
     int size=str.size();  
     for(int i=0; i<size; i++)  
     {  
         pos=str.find(pattern,i);  
         if(pos<size)  
         {  
             std::string s=str.substr(i,pos-i);  
             result.push_back(s);  
             i=pos+pattern.size()-1;  
         }  
     }  
     return result;  
}  
{% endhighlight %}
3 使用`transform`算法转换元素  
如以下代码将coll中元素转换为负数，并存储到coll2中  
`transform(coll1.begin(),coll1.end(),coll2.begin(),negate<int>());`  
4 善用`vector<vector<int>>`形式的二维数组  
普通new和delete出二维数组，麻烦不易维护，内存泄漏  
{% highlight c++ %}
int** ary = new int*[row_num];  
for(int i = 0; i < row_num; ++i)  
	ary[i] = new int[col_num];  
{% endhighlight %}
而使用`vector<vector<int>>` 则很方便，且内存连续  
`vector<vector<int> > ary(row_num, vector<int>(col_num, 0))；`  
5 使用`for_each`算法来作用于容器的每个元素  
常用于输出打印：  

```
for_each(coll.begin(),coll.end(), [](const int ele){ cout<<elem<<" ");
```

也可以接受一个操作,该操作可以改变接受的实参，但要求`by reference`方式传递
如：  
```
void square(int &elem)
{
	elem = elem*elem;
}
....
for_each(coll.begin(),coll.end(),square);
```   
6 `max_element`和`min_element`算法来查找最小值与最大值  
7 `equal`算法来判断两个区间是否相等  
如：以下代码将判断coll1,coll2是否相等  
```
equal(coll1.begin(),coll1.end(),coll2.begin(),[](int elem1,int elem2){return elem1 == elem2})
```  
8 `lexicographical...`判断字典书序是否小于另一个序列  
9 `generate_n`对元素赋予新生值  
如：  
`genrate(coll.begi(),coll.end(),rand);`使用rand函数来生成随机值，并赋值给coll  
10 `fill`和`fill_n`对元素进行赋值  
如：
`fill_n(coll.begin(),coll.end(),0);` 将coll中所有元素赋值为0  
`fill_n(coll.begin(),coll.size(),0);` 将coll中所有元素赋值为0  
11 `iota`将所有元素以一系列的递增值取代  
如下面代码将coll以10为起点，递增  
`iota(coll.begin(),iota.end(),10);`  
12 `merge`合并连个区间  
13 `remove`将等于某个值的全部元素去除  
14 `unique`移除毗邻的重复元素,如果需要去除数组中全部重复元素，则应该先排序，且注意返回的是迭代器  
15 `reverse`将元素的次序逆转  
16 `rotate`旋转元素次序  
17 `prev_permutation`和`next_permutation`得到元素的下一个全排列  
如以下代码将打印coll中的全排列  
```  
while(next_permutation(coll.begin(),coll.end()))  
        PRINT_ELEMENTS(coll," ");//该函数自定义，打印coll中的所有元素  
```  
18 `binary_search`判断某个区间是否存在某个元素  
19 `include`判断一个区间的每个元素是否包含于另一个区间  
20 `lower_bound`查找第一个“大于等于给定值”的元素  
21 `upper_bound`查找第一个“大于某给定值”的元素  
22 `accumulate`结合所有元素，如求和、乘积等操作   
加法：  
`accumulate(coll.begin(),coll.end(),0);`  
乘法：  
`accumulate(coll.begin(),coll.end(),1,multiplies<int>());`  
23 `range_based for`循环来打印、操作元素  
如  
```
for(const auto& elem : coll)
	cout<< elem << " ";
```
24 `count`和`count_if`用来计算元素个数  
如以下代码将返回coll中元素大于4的个数  
{% highlight c++ %}
num = count_if(coll.cbegin(),coll.cend(),
				[](int elem){
				return elem >4;	
				});
{% endhighlight %}
25 `shuffle`对元素重新洗牌  
26 `heap`相关算法：  
* `make_heap`将某区间的元素转换为heap  
* `pop_heap`对heap增加一个元素  
* `push_heap`对heap取出一个元素  
* `sort_heap`将heap转换为一个已排序集群，从此后它就不再是heap了  

27 字符串与数值之间的转换  
使用`to_string`将数值转换为字符串  
使用`stoi`,`stof`,`stod`等将字符串转为数值  
尽量少使用C风格的`atoi(string.c_str())`;  

28 使用`stoi`等函数，来做进制转换  
stoi函数原型为：int stoi (const string&  str, size_t* idx = 0, int base = 10);其中`base`指定了进制  

```
string str_hex = "0xA";  
int number_dec = stoi(str_hex,nullptr,16);  
```

29 使用`sstream`来处理C++中字符串分割的问题  

```
#include<string>
#include<algorithm>
#include<iostream>
#include <sstream>
#include <vector>
using namespace std;
int main()
{
	string str;
	getline(cin, str);
	stringstream ss(str);
	string temp;
	vector<string> ret;
	while (ss>>temp)
	{
		ret.push_back(temp);
	}
	system("pause");
}
```