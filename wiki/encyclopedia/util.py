import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        return (f.read().decode("utf-8"))
    except FileNotFoundError:
        return None

##def markdown_convert(string):
    formatted_list = re.split('\n', string)
    new_list = []
    count = 1
    for each in formatted_list:
        if each.startswith('#'):
            i = each.count('#')
            if i == 2:
                new_list.append('<br><br>')
            new_list.append(f"<h{i}>{each[i:]}</h{i}>")
            if i == 1:
                new_list.append("<br>")
        elif any(each.startswith(op) for op in ['+', '*', '-']):
            lst = 'ul'
            if count == 1:
                new_list.append(f"<{lst}>")
            new_list.append(f"<li>{each[1:]}</li>")
            count+=1
        elif each.startswith("1."):
            lst = 'ol'
            if count == 1:
                new_list.append(f"<{lst}>")
            new_list.append(f"<li>{each[1:]}</li>")
            count+=1
        else:
            if count != 1:
                new_list.append(f"</{lst}>")
                count = 1
            each = re.sub(r".?\*\*(.*?)\*\*|__(.*?)__", r" <b>\1\2</b>", each)
            each = re.sub(r".?\*(.*?)\*|_(.*?)_", r" <i>\1\2</i>", each)
            each = re.sub(r".?\~\~(.*?)\~\~", r" <s>\1</s>", each)
            each = re.sub(r".?\[(.*?)\]\(\/(.*?)\/(.*?)\)", r""" <a href="/\2/\3">\1</a>""", each)
            new_list.append(each)
    newstr = '\n'.join(new_list)
    return newstr