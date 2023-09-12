function injectEvent() {
    var btns = document.querySelectorAll("button");
    btns.forEach(function (button) {
        button.onclick = function () {
            haction = [];
            haction_get = button.getAttribute("haction");
            if (haction_get != null) {
                if (haction_get.includes(":") > 0) {
                    haction = haction_get.split(":");
                }
            }
            clicked(button.id, haction);
        };
    });
    var selects = document.querySelectorAll("select");
    selects.forEach(function (select) {
        select.onchange = function () {
            change(select.id, [select.value, "text"]);
        };
    });
    var inputs = document.querySelectorAll("input");
    inputs.forEach(function (input) {
        input.onchange = function () {
            type = input.type;
            if (type == "number") {
                type = "text";
            }
            if (type == "radio") {
                change(input.name, [input.value, type]);
            } else if (type == "checkbox") {
                change(input.id, [input.checked, "check"]);
            } else {
                change(input.id, [input.value, type]);
            }
        };
    });
    // for (var btn of btns) {
    //     if (!btn.id || btn.getAttribute("onclick")) continue;

    //     btn.onclick = (evt) => {
    //         // alert(evt.target.id);
    //         console.log(evt.target.id);
    //         haction = [];
    //         haction_get = evt.target.getAttribute("haction");
    //         if (haction_get != null) {
    //             if (haction_get.includes(":") > 0) {
    //                 haction = haction_get.split(":");
    //             }
    //         }
    //         clicked(evt.target.id, haction);
    //     };
    // }
}
function change_language(change_to) {
    var text_vn_en = `Kiểm tra youtube | Check info youtube
Kiểm tra ngày tạo | Check date create
Đổi mật khẩu | Change password
Đổi email khôi phục | Change email recovery
Xóa số điện thoại | Delete phone recovery
Kiểm tra số điện thoại | Check phone recovery
Kiểm tra tên gốc | Check google email
Tắt 2FA | Disable 2FA
Kiểm tra google voice | Check google voice
Kiểm tra thanh toán | Check payment method
Kháng mail disable | Restore disable
Đổi ngôn ngữ | Change language en
Kiểm tra quốc gia | Check country
Kiểm tra youtube premium | Check youtube premium
Đóng thanh toán | Close payment method
Xóa thanh toán | Delete payment method
Lưu profile | Save profile
Xác nhận cảnh báo đăng nhập | Confirm security
Đăng xuất thiết bị | Device logout
Tạo kênh youtube | Create channel youtube
Đổi tên hiển thị | Change display name
Kiểm tra chplay | Check chplay
Kiểm tra số điện thoại ẩn | Check hidden phone
Dừng lại khi đúng mật khẩu | Stop when password ok
Sắp xếp chrome gọn (có thể tăng khả năng chết nick) | Auto move chrome (can lead to account death)
Cài đặt otp | Config otp
Cài đặt captcha | Config captcha
Nội dung kháng disable | Restore disable content
Mail nhận thư kháng disable | Restore disable contact
Email khôi phục ngẫu nhiên | Email recovery random
Đuôi email khôi phục | Email recovery domain
Mật khẩu ngẫu nhiên | Password random
Kích hoạt tài khoản | Active account
Giải captcha | Solve captcha
Nhập khẩu | Import
Bảng điều khiển | Dashboard
Cài đặt | Setting
Nhật ký | Logs
Tài khoản | Account
Thoát chương trình | Quit
Chọn | Select
Sao chép | Copy
Chọn tất cả | Select all mails
Chọn mail chưa chạy | Select mails that has not been run
Chọn mail đã chạy | Select mails has been running
Bỏ chọn tất cả | Deselect all
Xóa tất cả mail đã chọn | Delete selected mails
Xuất tất cả mail đã chọn | Export selected mails
Chạy tất cả mail đã chọn | Run selected mails
Ẩn cột | Hide column
Tạm ngừng | Pause
Đã chọn | Selected
Phiên bản hiện tại | Current version
Cập nhật phiên bản mới | Update new version
Mở file hconfig | Open hconfig`;
    var text_split = text_vn_en.split("\n");
    var translations = {};
    for (var i = 0; i < text_split.length; i++) {
        var text = text_split[i];
        var texts = text.split("|");
        var key = texts[0].trim();
        var value = texts[1].trim();
        translations[key] = value;
    }

    if (change_to == "vietnamese") {
        var reversedTranslations = {};
        for (var key in translations) {
            if (translations.hasOwnProperty(key)) {
                var value = translations[key];
                reversedTranslations[value] = key;
            }
        }
        translations = reversedTranslations;
    }
    var elements = document.querySelectorAll("label");
    elements.forEach(function (element) {
        var text = element.textContent.trim();
        text = text.replace(/[\n\t]/g, "");
        text = text.replace(/\s+/g, " ");

        if (text in translations) {
            var newtext = translations[text];
            element.textContent = " " + newtext;
        } else {
            console.log(text);
        }
    });
    var elements = document.querySelectorAll("input");
    elements.forEach(function (element) {
        var text = element.textContent.trim();
        text = text.replace(/[\n\t]/g, "");
        text = text.replace(/\s+/g, " ");

        if (text in translations) {
            var newtext = translations[text];
            element.textContent = " " + newtext;
        } else {
            console.log(text);
        }
    });
}
function get_mails(skip, limit) {
    return sendMessage({
        action: "get_mails",
        sender: "",
        args: [skip, limit],
        form: formName(),
    });
}
function kich_hoat_tai_khoan(keyactive) {
    return sendMessage({
        action: "kich_hoat_tai_khoan",
        sender: keyactive,
        args: "",
        form: formName(),
    });
}
function handle_account(action, list_account) {
    var _args = [];
    if (!Array.isArray(list_account)) {
        _args = [list_account];
    } else {
        _args = list_account;
    }

    return sendMessage({
        action: action,
        sender: "",
        args: _args,
        form: formName(),
    });
}
function change(id, args = []) {
    var _args = [];
    if (!Array.isArray(args)) {
        _args = [args];
    } else {
        _args = args;
    }

    sendMessage({
        action: "change",
        sender: id,
        args: _args,
        form: formName(),
    });
}
function print(obj) {
    console.log(obj);
}
function clicked(id, args = []) {
    var _args = [];
    if (!Array.isArray(args)) {
        _args = [args];
    } else {
        _args = args;
    }

    sendMessage({
        action: "clicked",
        sender: id,
        args: _args,
        form: formName(),
    });
}
function formName() {
    //   alert(location.pathname);
    return location.pathname.substring(1).split(".")[0];
}
function send_message(data) {
    return sendMessage(data);
}
async function sendMessage(data) {
    if (typeof data == "string") {
        data = {
            action: data,
        };
    }

    data = JSON.stringify(data);
    //   alert(data);
    a = await eel.on_message(data)();
    // alert(a);
    return a;
}
function startApp() {
    injectEvent();
}

function gid(x) {
    return document.getElementById(x);
}
function gselector(x) {
    return document.querySelector(x);
}
function onMessage(data) {
    try {
        if (typeof data == "string") {
            data = JSON.parse(data);
        }
        let action = data.action;

        if (action == "set_html") {
            gid(data.id).innerHTML = data.html;
            return;
        } else if (action == "set_value") {
            gid(data.id).value = data.value;
        } else if (action == "set_checked") {
            gid(data.id).checked = JSON.parse(data.checked);
        } else if (action == "set_checked_radio") {
            gselector(
                "input[type='radio'][name='" +
                    data.name +
                    "'][value='" +
                    data.value_checked +
                    "']"
            ).checked = true;
        } else if (action == "set_style") {
            gid(data.id).style[data.style_name] = data.style_value;
        } else if (action == "set_style_selector") {
            gselector(data.selector).style[data.style_name] = data.style_value;
        } else if (action == "set_display_selector") {
            gselector(data.selector).style["display"] = data.display;
        } else if (action == "toast_success") {
            toastr.success(data.msg);
        } else if (action == "toast_warning") {
            toastr.warning(data.msg);
        } else if (action == "toast_info") {
            toastr.info(data.msg);
        } else if (action == "toast_error") {
            toastr.error(data.msg);
        } else if (action == "get_value") {
            return gid(data.id).value;
        } else if (action == "load_setting") {
            return gid(data.id).value;
        } else if (action == "change_language") {
            change_language(data.change_to);
        } else if (action == "load_url") {
            window.location.href = data.url;
        } else if (action == "load_mail") {
            load_mail(data.action);
        }
    } catch (ex) {
        console.log(ex);
    }
}
eel.expose(onMessage);
startApp();
