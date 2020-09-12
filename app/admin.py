import traceback
from copy import deepcopy

from django.contrib import admin
from django.core.exceptions import ValidationError
from django.db.transaction import TransactionManagementError
from django.utils.encoding import force_text
from import_export.results import RowResult
from django.contrib.auth.models import Permission, User
from app import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from django.apps import apps
from django.db.models import QuerySet
import tablib,uuid

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

    # 导入前
    def before_import_row(self, row, **kwargs):
        print(row)

    # 导入后(执行更新创建者修改)
    def after_import_row(self, row, row_result, **kwargs):
        print(row)

    # 导入数据 自动将当前登录用户 赋值给创建者和修改者
    def import_row(self, row, instance_loader, using_transactions=True, dry_run=False, **kwargs):
        print(instance_loader)
        row_result = self.get_row_result_class()()
        try:
            self.before_import_row(row, **kwargs)
            instance, new = self.get_or_init_instance(instance_loader, row)
            self.after_import_instance(instance, new, **kwargs)
            if new:
                row_result.import_type = RowResult.IMPORT_TYPE_NEW
            else:
                row_result.import_type = RowResult.IMPORT_TYPE_UPDATE
            row_result.new_record = new
            original = deepcopy(instance)
            diff = self.get_diff_class()(self, original, new)
            if self.for_delete(row, instance):
                if new:
                    row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                    diff.compare_with(self, None, dry_run)
                else:
                    row_result.import_type = RowResult.IMPORT_TYPE_DELETE
                    self.delete_instance(instance, using_transactions, dry_run)
                    diff.compare_with(self, None, dry_run)
            else:
                import_validation_errors = {}
                try:
                    self.import_obj(instance, row, dry_run)
                except ValidationError as e:
                    # Validation errors from import_obj() are passed on to
                    # validate_instance(), where they can be combined with model
                    # instance validation errors if necessary
                    import_validation_errors = e.update_error_dict(import_validation_errors)
                if self.skip_row(instance, original):
                    row_result.import_type = RowResult.IMPORT_TYPE_SKIP
                else:
                    self.validate_instance(instance, import_validation_errors)
                    print(instance)
                    print("dry_run", dry_run)
                    if instance.creator is None:
                        instance.creator = kwargs["user"]
                    instance.editor = kwargs["user"]
                    self.save_instance(instance, using_transactions, dry_run)
                    self.save_m2m(instance, row, using_transactions, dry_run)
                    # Add object info to RowResult for LogEntry
                    row_result.object_id = instance.pk
                    row_result.object_repr = force_text(instance)
                diff.compare_with(self, instance, dry_run)

            row_result.diff = diff.as_html()
            self.after_import_row(row, row_result, **kwargs)

        except ValidationError as e:
            row_result.import_type = RowResult.IMPORT_TYPE_INVALID
            row_result.validation_error = e
        except Exception as e:
            row_result.import_type = RowResult.IMPORT_TYPE_ERROR
            # There is no point logging a transaction error for each row
            # when only the original error is likely to be relevant
            if not isinstance(e, TransactionManagementError):
                print(e)
            tb_info = traceback.format_exc()
            row_result.errors.append(self.get_error_result_class()(e, tb_info, row))
        return row_result

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


# 应用管理
@admin.register(models.appManager)
class appManagerAdmin(ImportExportModelAdmin):
    fields = (
        "name", "state",
        "contactPerson", "whitelist", "domain")
    list_display = (
        "name", "appid", "secret", "state",
        "createTime",
        "lastTime",
        "creator", "editor")
    list_display_links = ("name",)
    exclude = ("createTime", "creator", "editor")
    search_fields = ("name",)
    list_filter = ("state",)
    model_icon = "fa fa-tag"
    list_per_page = 20
    ordering = ["-id"]

    def save_model(self, request, obj, form, change):
        if form.is_valid():
            if change:
                obj.editor = request.user
            else:
                appid = str(uuid.uuid4())
                secret = str(uuid.uuid4())
                obj.appid = appid
                obj.secret = secret
                obj.creator = request.user
                obj.editor = request.user
                obj.save()
                # 新创建一个授权用户
                User.objects.create_user(username=appid, password=secret, is_staff=True, is_active=True,
                                         first_name=obj.name)
        super().save_model(request, obj, form, change)