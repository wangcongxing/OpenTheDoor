from django import template
from django.apps import apps

register = template.Library()  # 这一句必须这样写


@register.simple_tag(takes_context=True)
def import_head_tag(context):
    verbose_names = []
    fieldlists = context.dicts[3]["fields"]
    opts = str(context.dicts[3]["opts"]).split(".")
    for f in fieldlists:
        fields = apps.get_model(opts[0], opts[1])._meta.fields
        for fs in fields:
            if (str(fs).split(".")[-1] == str(f)):
                verbose_names.append(fs.verbose_name)
                break

    return "，".join(verbose_names)
