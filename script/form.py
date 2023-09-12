import eel
import json
import time
class Form:
    def __init__(self):
        pass
    def send_message(self, data):
        text = json.dumps(data)

        rs = eel.onMessage(text)()
        return rs
    def get_value(self, id) -> str:
        return self.send_message({'action': 'get_value','id': id})
    def set_html_selector(self, selector, html):
        data = {'action': 'set_html_selector','selector': selector,'html': html,}
        self.send_message(data)
    def set_display_selector(self, selector, display):
        self.send_message({'action': 'set_display_selector', 'selector': selector, 'display': display})
    def set_style_selector(self, selector, style_name, style_value):
        self.send_message({'action': 'set_style_selector', 'selector': selector, 'style_name': style_name, 'style_value': style_value})
    def set_style(self, id, style_name, style_value):
        self.send_message({'action': 'set_style', 'id': id, 'style_name': style_name, 'style_value': style_value})
    def set_checked(self, id, checked):
        self.send_message({'action': 'set_checked','id': id,'checked': str(checked).lower()})
    def set_checked_radio(self, name, value_checked):
        self.send_message({'action': 'set_checked_radio','name': name,'value_checked': value_checked})
    def set_value(self, id, value = "", use_ini = False):
        if use_ini:
            from hini import hini
            ini = hini()
            value = ini.read(id)
        self.send_message({'action': 'set_value','id': id,'value': value})
    def set_html(self, id, html):
        self.send_message({'action': 'set_html','id': id,'html': html})
    def load_url(self, url):
        self.send_message({'action': 'load_url','url': url})
    def load_mail(self, page_load):
        self.send_message({'action': 'load_mail','page_load': page_load})
    def toast_success(self, msg):
        self.send_message({'action': 'toast_success','msg': msg})
    def toast_warning(self, msg):
        self.send_message({'action': 'toast_warning','msg': msg})
    def toast_info(self, msg):
        self.send_message({'action': 'toast_info','msg': msg})
    def toast_error(self, msg):
        self.send_message({'action': 'toast_error','msg': msg})
    def change_language(self, change_to):
        self.send_message({'action': 'change_language', "change_to": change_to})

f = Form()

class Combobox:
    def __init__(self, id):
        self.id = id
        self.html = ""
        pass
    def create_combobox(self, dict_value_text: dict):
        selected = "selected"
        for value in dict_value_text:
            text =dict_value_text.get(value)
            self.html = self.html + f'<option value="{value}" {selected}>{text}</option>'
            selected = ""
    def execute(self):
        f.set_html(self.id, self.html)

class Row():
    def __init__(self, id):
        self.id = id
        self.html = ""
        pass
    def add_item(self, value, type="text", id=""):
        if not value:
            value = ""
        if value == "None":
            value = ""
        if not value:
            self.html = self.html + f"<td>{value}</td>"
        else:
            self.html = self.html + f'<td><input type="{type}" id="{id}" value="{value}"></td>'


class Table():
    def __init__(self, id_table):
        self.id_table = id_table
        self.html = ""
        self.f = Form()
        pass
    def create_table(self, dict_name_value_column: dict):
        self.html = '<thead><tr class="w3-light-grey w3-hover-red">'
        for name in dict_name_value_column:
            value =dict_name_value_column.get(name)
            self.html = self.html + f'<th id="{name}">{value}</th>'
        self.html = self.html + '</tr></thead>'
        # self.f.set_html(self.id_table,self.html)
    def add_row(self, row: Row):
        self.html = self.html + f'<tr class="w3-hover-green" id="{row.id}">{row.html}</tr>'
    def execute(self):
        self.f.set_html(self.id_table, self.html)


class Update:
    def __init__(self, url_update):
        self.url_update = url_update

    def check_version(self):
        from hrequest import hrequest
        from hfile import hfile
        from hstr import hstr
        from hthread import hthread
        def run():
            now_version = hfile.read("script/version.txt")
            rq = hrequest()
            project = hstr.regex(self.url_update, "(https://github.com/.*?/.*?)/")
            if not project:
                print("form.Update", "not project")
                return
            urlversion = f"{project}/raw/main/script/version.txt"
            while True:
                time.sleep(1)
                newversion = rq.get_html(urlversion).strip()
                if newversion == now_version or len(newversion) > 10:
                    time.sleep(10)
                    continue
                f.set_html("updateversion",  "Update new version: " + newversion)
                return
        hthread.start(run)

