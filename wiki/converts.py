import re

string = """# CSS

CSS is a language that can be used to add style to an [HTML](/wiki/HTML) page."""

formatted_list = re.split('\n', string)
new_list = []
count = 1
for each in formatted_list:
    if each.startswith('#'):
        i = each.count('#')
        new_list.append(f"<h{i}>{each[1:]}</h{i}>")
    elif any(each.startswith(op) for op in ['+', '*', '-']):
        lst = 'ul'
        if count == 1:
            new_list.append(f"{lst}")
        new_list.append(f"<li>{each[1:]}</li>")
        count+=1
    elif each.startswith("1."):
        lst = 'ol'
        if count == 1:
            new_list.append(f"{lst}")
        new_list.append(f"<li>{each[1:]}</li>")
        count+=1
    else:
        if count != 1:
            new_list.append(f"</{lst}>")
            count = 1
        each = re.sub(r".?\*\*(.*?)\*\*|__(.*?)__", r"<b>\1\2</b>", each)
        each = re.sub(r".?\*(.*?)\*|_(.*?)_", r"<i>\1\2</i>", each)
        each = re.sub(r".?\~\~(.*?)\~\~", r" <s>\1</s>", each)
        each = re.sub(r".?\[(.*?)\]\(\/(.*?)\/(.*?)\)", r""" <a href="{% url '\2:\3' %}">\1</a>""", each)
        new_list.append(each)
newstr = '\n'.join(new_list)
print(formatted_list)
print(newstr)
