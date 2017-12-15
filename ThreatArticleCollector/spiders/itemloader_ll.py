#_*_coding:utf-8_*_
from scrapy.loader import ItemLoader
from collections import defaultdict
import six

from scrapy.item import Item
from scrapy.selector import Selector
from scrapy.utils.decorators import deprecated
from scrapy.utils.deprecate import create_deprecated_class
from scrapy.utils.misc import arg_to_iter, extract_regex
from scrapy.utils.python import flatten

from scrapy.loader.common import wrap_loader_context
from scrapy.loader.processors import Identity


class itemloader_ll(ItemLoader):
    '''
    添加了一个新的add_to_ariginal方法，因为官方说add是append而不是覆盖原来的数据，而结果代码中是覆盖原来的数据，所以这里添加了一个自己写的函数
    '''

    def __init__(self, item=None, selector=None, response=None, parent=None, **context):
        if selector is None and response is not None:
            selector = self.default_selector_class(response)
        self.selector = selector
        context.update(selector=selector, response=response)
        if item is None:
            item = self.default_item_class()
        self.context = context
        self.parent = parent
        self._local_item = context['item'] = item
        self._local_values = defaultdict(list)
        self.values_added={}


    def add_value_to_original(self, field_name, value, *processors, **kw):
        value = self.get_value(value, *processors, **kw)
        if value is None:
            return
        if not field_name:
            for k, v in six.iteritems(value):
                # self._add_value(k, v)
                self.values_added[k]=v
        else:
            if field_name not in self.values_added.keys():
                self.values_added[field_name]=[value]
            else:
                self.values_added[field_name].append(value)
            # self._add_value(field_name, value)


    def load_item(self):
        item = self.item
        for field_name in tuple(self._values):
            value = self.get_output_value(field_name)
            if value is not None:
                item[field_name] = value

        for field_name in tuple(self.values_added):
            value = self.get_output_value(field_name)
            if value is not None:
                if field_name in self.item.keys():
                    self.item[field_name].append(value)
                else:
                    self.item[field_name]=value

        return item