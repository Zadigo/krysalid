# Krysalid - HTML Page Parser

Krysalid is a modern HTML page parser from which you can query anything on a page.

## Getting started

```python
from krysalid.html_parser.parsers import Extractor

with open('path/page.html', encoding='utf-8') as f:
    extractor = Extractor(f)
```

Krysalid uses Python's default `html.HTMLParser` to read  each lines of the HTML page. Before sending the string to the parser, the page is formatted to a standard format using `lxml.html_from_string`.

Once the string is processed, each html tag on the page is converted into a Python object which will then be used to run all the queries on the page.

## Querying objects on the page

Krysalid interfaces the queries via a `Manager` class which provides a set of default functions. The `Manager` class can be subclassed and additional custom functions can be added as we'll see later on.

### Manager API

Consider that the Manager API deals with queries at the very top level on the html page.

#### Get title

Returns the title of the current page.

```python
extractor.manager.get_title
# Example Website
```

#### Links

Returns all the links present on the current page. Returns a (#QuerySet)[QuerySet].

```python
extractor.manager.links

# QuerySet([<a>, <a>])
```

#### Tables

Returns all the tables present on the current page. Returns a (#QuerySet)[QuerySet].

```python
extractor.manager.tables

# QuerySet([<table>, <table>])
```

#### Find

Returns a specific tag on the page. Returns an (#HTMLTag)[HTMLTag].

```python
extractor.manager.find('a')

# Tag -> <a>
```

You can also specify specific tags such as `ElementData` tags or `NewLine` tags as _data_ or _newline_ respectively.

#### Find all

Returns a specific tag on the page. Returns a (#QuerySet)[QuerySet].

```python
extractor.manager.find_all('a')

# QuerySet([<a>, <a>])
```

#### Save

Saves the html page to a file.

```python
extractor.manager.save('myfile')
```

#### Live update

Fetches a newer version of the html page using a url or a string.

```python
extractor.manager.live_update(url='http://example.com')
```

### QuerySet API

A `QuerySet` is simply just an aggregation of multiple tags under one main interface or API. Many aggregating functions will then return a queryset class.

This class implements additional querying functionnalities but also allows for the original html data to stay untouched.

Each query generates a new queryset of its own with sub data that can also then be queried.

Consider this example:

```python
queryset.find_all('a').find_all('a', attrs={'id': 'test'}).exclude('a', attrs={'id': 'test2'})
```

Each element of the chain returns a new `QuerySet` copy on which we can run additional queries. This can be done until we reach the tag level or that the queryset is not empty.

Note that every time a new `QuerySet` is created, the data that the next element of the chain will use to filter tags will be the result of the previous query stored in the previously created one.

#### First

Returns the first item of the queryset. Returns a Tag.

```python
tags = extractor.manager.find_all('a')
tags.first

# Tag -> <a>
```

#### Last

Returns the last item of the queryset. Returns a Tag.

```python
tags = extractor.manager.find_all('a')
tags.last

# Tag -> <a>
```

#### Count

Returns the number of items in the queryset.

```python
tags = extractor.manager.find_all('a')
tags.count()

# int -> 1
```

#### Save

Saves the queryset to a file.

```python
tags = extractor.manager.find_all('a')
tags.save('myfile')
```

#### Find

Finds an element within the queryset.

```python
tags = extractor.manager.find_all('a')
tag = tags.find('a')

# Tag -> <a>
```

#### Find all

Finds all the elements within the queryset.

```python
queryset = extractor.manager.find_all('a')
tags = queryset.find_all('a')

# QuerySet([<a>, <a>])
```

#### Exclude

Return items that do not contain a given or certain attributes.

```python
queryset = extractor.manager.find_all('a')
tags = queryset.exclude('a', attrs={'id': 'test'})

# QuerySet([<a>, <a>])
```

#### Distinct - Bêta

Return elements that have a very distinct attribute.

```python
queryset = extractor.manager.find_all('a')
tags = queryset.distinct('a', attrs={'id': 'test'})

# QuerySet([<a>, <a>])
```

#### Values

Returns the data or value contained within each tag of the queryset.

When no parameter is provided, the default return value is the string contained within the tag.

```python
queryset = extractor.manager.find_all('a')
tags = queryset.values()

# List -> ['Click', 'Press', ...]
```

```python
queryset = extractor.manager.find_all('a')
tags = queryset.values('id', 'class')

# List -> ['some_id', 'some_class', ...]
```

This functions returns a special (ValuesQueryset)[#values-queryset] that you can see afterwards. 

#### Values list -  Bêta

Returns the data or any attributes value contained within each tag of the queryset. You can specify which attributes to return specifically.

```python
queryset = extractor.manager.find_all('a')
tags = queryset.values('id', 'string')

# List -> [[('id', 'test'), ('data', 'Click)], ...]
```

#### Dates - Bêta

Returns the date within an html tag as Python objects. If no date can be parsed, None will be stored in the return values.

```python
queryset = extractor.manager.find_all('div')
tags = queryset.dates('datetime')

# List -> [datetime.datetime(1, 1, 2000), ...]
```

#### Union

Concatenate two querysets into a third new queryset.

```python
q1 = extractor.manager.find_all('div')
q2 = extractor.lmanager.find_all('a')
q3 = q1.union(q2)

# <QuerySet[<div>, <a>]>
```

The very same result can be obtained by doing the following:

```python
q3 = q1 & q2

# <QuerySet[<div>, <a>]>
```

#### Exists

Checks whether an element exists in the queryset.

```python
queryset = extractor.manager.find_all('div')
if queryset.exists():
    # Do something

# Boolean -> True or False
```

#### Contains

Checks if an element exists wihin the queryset.

```python
queryset = extractor.manager.find_all('div')
if queryset.contains('div'):
    # Do something

# Boolean -> True or False
```

#### Explain

Displays in verbose text what the queryset is composed of.

```python
queryset = extractor.manager.find_all('div')
queryset.explain()

# 1. name: 'div', tag: <div>, children: 1
```

#### Generator

Defers the resolution of the new query to a later stage for eventual optimization purposes.

```python
queryset = extractor.manager.find_all('div')
links = queryset.generator('a', attrs={'id': 'test'})

for link in links:
    # Do something

# Generator -> <QuerySet[<a id="test">]>
```

#### Update

Update all the attribute list of the items within the queryset that goes by the given name.

```python
queryset = extractor.manager.find_all('div')
result = queryset.update('a', 'id', 'test2')

# <QuerySet[<div>]> -> <QuerySet[<div id="test2">]>
```

### Values Queryset

The values implements addiational functionnalities for functions that returns lists as their result. It also keeps track of the relationship between a tag and the value that was parsed from it.

Consider the initial queryset below. We found all the tags called `div` within the document and got all their `id` attributes as seen.

```python
queryset = extractor.manager.find_all('div').values('id')

# <Queryset[[['id'], [None], ['1'], ['2'], [None], ['3'], ['4']]]>

```

#### Find all

Find all values that respect the given constraint.

```python
queryset = queryset.find_all('3')

# <Queryset[['3']]>
```

#### Flatten

Get a 1-Dimensional list from the results.

```python
queryset = queryset.find_all('3')

# <Queryset[[None, '1', '2', None, '3', '4']]>
```

#### Distinct

Only keep distinct values within the list. Note, this changes the order of the list.

```python
queryset = queryset.find_all('3')

# <Queryset[['3', '2', '1', '4', None]]>
```

### BaseTag API

Tags also provide additional query functionnalities for the children within them. Therefore calling one of these functions will only query the child elements of the tag.

#### Parents

Returns all the parents of the tag.

```python
tag = extractor.manager.find('div')
parents = tag.parents

# QuerySet([<html>, <body>])
```

#### Parent

Returns the immediate parent of the tag.

```python
tag = extractor.manager.find('div')
parents = tag.parent

# Tag -> <body>
```

#### Get parent

Get a specific parent from the list of parents of the current tag.

```python
tag = extractor.manager.find('div')
queryset = tag.get_parent('body')

# Tag -> <body>
```

#### Get previous sibling - Bêta

Get the previous sibling of the current tag.

```python
tag = extractor.manager.find('div')
queryset = tag.get_previous_sibling('div')

# Tag -> <div>
```

#### Contents

Get all the content within the tag.

```python
tag = extractor.manager.find('div')
result = tag.contents

# List -> ['Click', 'Kendall', ...]
```

#### Children

Returns all the children of the given tag.

```python
tag = extractor.manager.find('div')
tag.children

# QuerySet([<a>, <a id="test">])
```

#### Get children

Returns all the children of the given tag going by specific names.

```python
tag = extractor.manager.find('div')
tag.get_children('a', 'span')

# QuerySet([<a>, <span>])
```

#### Find

Find a child element within the tag.

```python
tag = extractor.manager.find('div')
tag.find('a')

# Tag -> <a>
```

#### Find all

Find all child element within the tag by a specific name or attribute.

```python
tag = extractor.manager.find('div')
tag.find_all('a')

# QuerySet([<a>, <a>])
```

#### Get attribute

Returns an attribute of the tag as a string

```python
tag = extractor.manager.find('div', attrs={'id': 'test', 'class': 'color'})
tag.get_attr('id')

# str -> "test"
```

#### Delete

Deletes the tag from the global collection list.

```python
tag = extractor.manager.find('div')
tag.delete()

# <html><div></div> -> [<html>, <div>] -> [<html>]
```

## Navigating the DOM

The `BaseTag` API also includes additional functionnalities to navigate the DOM efficiently.

#### Previous element

Get the element directly before the current tag.

```python
tag = extractor.manager.find('div')
new_tag = tag.previous_element

# Tag -> <body>, ...
```

#### Next element

Get the element directly after the current tag.

```python
tag = extractor.manager.find('div')
new_tag = tag.next_element

# Tag -> <div>, <span>, ...
```

#### Get attribute

Get the attribute of a given tag.

```python
tag = extractor.manager.find('div')
queryset = tag.get_attr('div')

# String
```

#### Get previous

Get the previous element before the current tag going by a specific name.

```python
tag = extractor.manager.find('div')
tag.get_previous('div')

# Tag -> <div> or None
```

#### Get next

Get the next element before the current tag going by a specific name.

```python
tag = extractor.manager.find('div')
tag.get_next('div')

# Tag -> <div> or None
```

#### Get all previous

Get the all the previous elements before the current tag going by a specific name.

```python
tag = extractor.manager.find('div')
queryset = tag.get_all_previous('div')

# QuerySet([<div>, <div>])
```

#### Get all next

Get the all the next elements after the current tag going by a specific name.

```python
tag = extractor.manager.find('div')
queryset = tag.get_all_next('div')

# QuerySet([<div>, <a>])
```

#### Get next sibling - Bêta

Get the next sibling of the current tag.

```python
tag = extractor.manager.find('div')
queryset = tag.get_next_sibling('div')

# Tag -> <div>
```

#### String

Get the content within the tag.

```python
tag = extractor.manager.find('div')
tag.string

# <div>Kendall</div> -> Tag -> "Kendall"
```

## Base tags

When the XXX parses the html document, it transforms each of the string tags into Python objects with which you can interract. There are three main categories of tags: `Tag`, `ElementData `, `NewLine `and `Comment`.

### Tag

Represents the majority of HTML tags wihin a document: `a`, `img` etc.

This is the only item on which you can call additional querying functions like `find_all` or `find` because it is the only one that can logically contain children.

### ElementData

Represents the data contained within an HTML tag. For instance, in this tag, `<div>Kendall</div>`, `Kendall` is the element's data.

### NewLine

Reprents a newline marked as `\n` from the HTML document.

### Comment

Reprents a comment form the HTML document. This is similar to the `ElementData` tag.

## Extractors

In certain situations, you might want to extract very specific things in such as images, tables or the whole text on the html page. XXX comes with extractors that can execute these veery specific and often common tasks in parsing a web page.

All extractors are subclasses of the main `Extractor`.

### ImageExtractor

Extracts all the images from a web page.

```python
extractor = ImageExtractor()
images = extractor.get_images()

# QuerySet([<img src="http://website.com/1.jpg">])
```

### TextExtractor

Extracts the whole text from a web page.

```python
extractor = TextExtractor()
images = extractor.get_text()

# List -> ['Some text', ...]
```

### TableExtractor

Extracts the whole text from a web page.

```python
extractor = TableExtractor()
images = extractor.get_values()

# List -> [[], [1, 165], [2, 176], ...]
```

## Doing complexe queries

You can run more complex queries on the page using the `Q` field.

Consider this example:

```python
query = Q(a__id="fast") & Q(a__id__ne="slow") | Q(a__id__in=["medium", "moderate"])

with open(path_to_file, encoding='utf-8') a f:
    parser = HTMLPageParser(html_string)
    queryset = parser.find_all(query)

# QuerySet([<a id="fast">, <a id="slow">])
```

As you can see, we are testing links so that those who have an id of _test_ or _color_ or that those who have an id attribute of _medium_ or _moderate_ from the list appear in the queryset.
