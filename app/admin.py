from django.contrib import admin
from app import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.apps import apps
from django.db.models import QuerySet
import tablib

# Register your models here.
admin.site.site_header = "大佬管理"
admin.site.site_title = "大佬管理后台管理"


class bossInfoResource(resources.ModelResource):
    def __init__(self):
        super(bossInfoResource, self).__init__()

        field_list = models.bossInfo._meta.fields
        self.vname_dict = {}
        self.fkey = []
        customeFields = (
            "id", "age", "gender", "likeFruit", "userUrl", "name", "desc",)
        for i in field_list:
            if i.name in customeFields:
                self.vname_dict[i.name] = i.verbose_name.lower()
                self.fkey.append(i.name)

    # 默认导入导出field的column_name为字段的名称，这里修改为字段的verbose_name
    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        print("after_import")

    def after_import_instance(self, instance, new, **kwargs):
        print("after_import_instance")

    # 重载resources.py的export方法，修改将要导出的data的某些外键相关数据。默认导出外键id，这里修改为导出外键对应的值
    def export(self, queryset=None, *args, **kwargs):
        self.before_export(queryset, *args, **kwargs)
        if queryset is None:
            queryset = self.get_queryset()
        headers = self.get_export_headers()
        headers.append("创建时间")
        headers.append("修改时间")
        headers.append("创建者")
        headers.append("修改者")
        data = tablib.Dataset(headers=headers)
        # 获取所有外键名称在headers中的位置
        fk_index = {}
        for fk in self.fkey:
            fk_index[fk] = headers.index(self.vname_dict[fk])
        # --------------------- #

        if isinstance(queryset, QuerySet):
            # Iterate without the queryset cache, to avoid wasting memory when
            # exporting large datasets.
            iterable = queryset.iterator()
        else:
            iterable = queryset
        for obj in iterable:
            # --------------------- #
            # 获取将要导出的源数据，这里export_resource返回的是列表，便于更改。替换到外键的值
            # 可以对所有字段值进行二次处理
            res = self.export_resource(obj)
            res[fk_index['id']] = obj.id
            res[fk_index['age']] = obj.age
            res[fk_index['gender']] = obj.gender
            res[fk_index['likeFruit']] = obj.likeFruit
            res[fk_index['userUrl']] = obj.userUrl
            res[fk_index['name']] = obj.name
            res[fk_index['desc']] = obj.desc
            res.append(obj.createTime)
            res.append(obj.lastTime)
            res.append(obj.creator.username)
            res.append(obj.editor.username)
            data.append(res)
            # --------------------- #
        self.after_export(queryset, data, *args, **kwargs)
        return data

    class Meta:
        model = models.bossInfo
        skip_unchanged = True
        report_skipped = True
        fields = (
            "id", "age", "gender", "likeFruit", "userUrl", "name", "desc",)


@admin.register(models.bossInfo)
class bossInfoAdmin(ImportExportModelAdmin):
    fields = (
        "name", "age", "gender",
        "likeFruit", "userUrl", "desc")
    list_display = (
        "name", "age", "gender",
        "likeFruit", "userUrl",
        "createTime",
        "lastTime",
        "creator", "editor")
    list_display_links = ("name",)
    exclude = ("createTime", "creator", "editor")
    search_fields = ("name",)
    list_filter = ("gender", "likeFruit")
    model_icon = "fa fa-tag"
    list_per_page = 20
    ordering = ["-id"]
    resource_class = bossInfoResource

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if change:
                obj.editor = request.user
            else:
                obj.creator = request.user
                obj.editor = request.user
                obj.save()
        super().save_model(request, obj, form, change)

# Register your models here.
class commodityResource(resources.ModelResource):

    def __init__(self):
        super(commodityResource, self).__init__()

        field_list = models.commodity._meta.fields
        self.vname_dict = {}
        for i in field_list:
            self.vname_dict[i.name] = i.verbose_name

    def get_import_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    # 默认导入导出field的column_name为字段的名称，这里修改为字段的verbose_name
    def get_export_fields(self):
        fields = self.get_fields()
        for field in fields:
            field_name = self.get_field_name(field)
            # 如果我们设置过verbose_name，则将column_name替换为verbose_name。否则维持原有的字段名
            if field_name in self.vname_dict.keys():
                field.column_name = self.vname_dict[field_name]
        return fields

    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        print("after_import")

    def after_import_instance(self, instance, new, **kwargs):
        print("after_import_instance")

    class Meta:
        model = models.commodity
        skip_unchanged = True
        report_skipped = True
        fields = ("id", "name", "desc")


@admin.register(models.commodity)
class AppTypeAdmin(ImportExportModelAdmin):
    list_display = ("name", "desc")
    list_display_links = ("name", "desc")
    search_fields = ('name', 'desc')
    model_icon = "fa fa-tag"
    list_per_page = 50
    resource_class = commodityResource

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)