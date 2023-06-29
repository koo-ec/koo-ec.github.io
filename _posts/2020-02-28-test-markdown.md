---
layout: post
title: SafeML
subtitle: Exploring techniques for safety monitoring of machine learning classifiers
gh-repo: ISorokos/SafeML
gh-badge: [star, fork, follow]
tags: [SafeML]
comments: false
---

Ensuring safety and explainability of machine learning (ML) is a topic of increasing relevance as data-driven applications venture into safety-critical application domains, traditionally committed to high safety standards that are not satisfied with an exclusive testing approach of otherwise inaccessible black-box systems. Especially the interaction between safety and security is a central challenge, as security violations can lead to compromised safety. The contribution of this project to addressing both safety and security within a single concept of protection applicable during the operation of ML systems is active monitoring of the behaviour and the operational context of the data-driven system based on distance measures of the Empirical Cumulative Distribution Function (ECDF). We investigate abstract datasets such as XOR, Spiral, and Circle and some well-known security-specific datasets for intrusion detection of simulated network traffic, using distributional shift detection measures including the Kolmogorov-Smirnov, Kuiper, Anderson-Darling, Wasserstein and mixed Wasserstein-Anderson-Darling measures. Our preliminary findings indicate that the approach can provide a basis for detecting whether the application context of an ML component is valid in the safety-security.
<!--
This is a demo post to show you how to write blog posts with markdown.  I strongly encourage you to [take 5 minutes to learn how to write in markdown](https://markdowntutorial.com/) - it'll teach you how to transform regular text into bold/italics/headings/tables/etc.

**Here is some bold text**

## Here is a secondary heading

Here's a useless table:

| Number | Next number | Previous number |
| :------ |:--- | :--- |
| Five | Six | Four |
| Ten | Eleven | Nine |
| Seven | Eight | Six |
| Two | Three | One |


How about a yummy crepe?

![Crepe](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg)

It can also be centered!

![Crepe](https://s3-media3.fl.yelpcdn.com/bphoto/cQ1Yoa75m2yUFFbY2xwuqw/348s.jpg){: .mx-auto.d-block :}

Here's a code chunk:

~~~
var foo = function(x) {
  return(x + 5);
}
foo(3)
~~~

And here is the same code with syntax highlighting:

```javascript
var foo = function(x) {
  return(x + 5);
}
foo(3)
```

And here is the same code yet again but with line numbers:

{% highlight javascript linenos %}
var foo = function(x) {
  return(x + 5);
}
foo(3)
{% endhighlight %}

## Boxes
You can add notification, warning and error boxes like this:

### Notification

{: .box-note}
**Note:** This is a notification box.

### Warning

{: .box-warning}
**Warning:** This is a warning box.


### Error

{: .box-error}
**Error:** This is an error box.

-->
