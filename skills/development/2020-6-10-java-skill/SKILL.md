---
layout: wiki
title: Java 语言积累
categories: Java
description: Java 语言积累
keywords: linux, Java
---

积累一些在使用 Java 语言编程中常用到的一些方法:

# List中元素不重复比对

```java

class test {

    public static void main(String[] args) {

        List<Integer> tem = new ArrayList<>();
        tem.add(0);
        tem.add(1);
        tem.add(2);
        tem.add(3);
        tem.add(4);
        tem.add(5);
        int first = tem.get(0);
        tem.remove(0);
        while (!tem.isEmpty()) {
            for (int j = 0; j < tem.size(); j++) {
                System.out.println(first + "--------->" + tem.get(j));
            }
            first = tem.get(0);
            tem.remove(0);
        }
    }
}

```

***

**2020-6-10更新**

***