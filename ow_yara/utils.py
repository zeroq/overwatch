from django.conf import settings

from .models import YaraRule, YaraImport


import yara
import os
import codecs

def verify_rule(rule):
    """ get yara rule in string format and try to compile it
    """
    try:
        r = yara.compile(source=rule)
    except Exception as e:
        return False, e
    return True, None


def compile_all_rules():
    counter = 0
    temp_file = os.path.join(settings.FILE_TEMP_PATH, 'all_yara.yar')
    fp = codecs.open(temp_file, 'w', encoding='utf8')
    imports = YaraImport.objects.all()
    for imp in imports:
        fp.write('import "%s"\n' % imp.name)
    fp.write('\n\n')
    rules = YaraRule.objects.filter(enabled=True)
    for rule in rules:
        fp.write('rule %s { %s }\n\n' % (rule.name, rule.body))
        counter += 1
    fp.close()
    os.chmod(temp_file, 0o666)
    if counter > 0:
        try:
            cyr = yara.compile(filepath=temp_file)
            return cyr, None
        except Exception as e:
            return None, e
    return None, None

