from wtforms.fields import Field
from wtforms.widgets import TextInput
from jobplus.models import Jtag, Jcity



class ListField(Field):

    widget = TextInput()

    def __init__(self, label=None, validators=None, **kwargs):
        super(ListField, self).__init__(label, validators, **kwargs)


    def _value(self):
        if self.data:
            r = u''
            for obj in self.data:
                r += self.obj_to_str(obj)
            return u''
        else:
            return u''


    def process_formdata(self, valuelist):
        print('process_formdata..')
        print(valuelist)
        if valuelist:
            names = self._remove_duplicates([x.strip() for x in valuelist[0].split(',')])
            self.data = [self.str_to_obj(name) for name in names]
        else:
            self.data = None


    def pre_validate(self, form):
        pass



    @classmethod
    def _remove_duplicates(cls, seq):
        """去重"""
        d = {}
        for item in seq:
            if item.lower() not in d:
                d[item.lower()] = True
                yield item


    @classmethod
    def obj_to_str(cls, obj):
        """将对象转换为字符串"""
        if obj:
            return obj.name
        else:
            return u''




class TagListField(ListField):

    @classmethod
    def str_to_obj(cls, name):
        """将字符串转换位obj对象"""
        tag_obj = Jtag.query.filter_by(name=name).first()
        if tag_obj is None:
            tag_obj = Jtag(name=name)
        return tag_obj




class CityListField(ListField):

    @classmethod
    def str_to_obj(cls, name):
        """将字符串转换位obj对象"""
        city_obj = Jcity.query.filter_by(name=name).first()
        if city_obj is None:
            city_obj = Jcity(name=name)
        return city_obj

