$(function () {
    $(this).bind("contextmenu", function (e) {
        e.preventDefault();
    });
});
function includeHTML() {
    var z, i, elmnt, file, xhttp;
    /*loop through a collection of all HTML elements:*/
    z = document.getElementsByTagName("*");
    for (i = 0; i < z.length; i++) {
        elmnt = z[i];
        /*search for elements with a certain atrribute:*/
        file = elmnt.getAttribute("w3-include-html");
        if (file) {
            /*make an HTTP request using the attribute value as the file name:*/
            xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function () {
                if (this.readyState == 4) {
                    if (this.status == 200) {
                        elmnt.innerHTML = this.responseText;
                    }
                    if (this.status == 404) {
                        elmnt.innerHTML = "Page not found.";
                    }
                    /*remove the attribute, and call this function once more:*/
                    elmnt.removeAttribute("w3-include-html");
                    includeHTML();
                }
            };
            xhttp.open("GET", file, true);
            xhttp.send();
            /*exit the function:*/
            return;
        }
    }
}
function strToBool(myValue) {
    return String(myValue).toLowerCase() === "true";
}
function toastError(x) {
    toastr.error(x);
}
function toastSuccess(x) {
    toastr.success(x);
}
function toastWarning(x) {
    toastr.warning(x);
}
function toastInfo(x) {
    toastr.info(x);
}
function removeCssSelector(cssSelector) {
    $(cssSelector).remove();
}
function pythonToJS(x) {
    const txtArea = document.getElementById("nhatkyhoatdong");
    txtArea.value = x + "\r\n" + txtArea.value;
}
function setHtmlCssSelector(cssSelector, html) {
    $(cssSelector).html(html);
}
function setValueCssSelector(cssSelector, value) {
    $(cssSelector).val(html);
}
eel.expose(removeCssSelector);
eel.expose(addRowTable);
eel.expose(pythonToJS);
eel.expose(setHtmlCssSelector);
eel.expose(setValueCssSelector);
eel.expose(toastError);
eel.expose(toastSuccess);
eel.expose(toastWarning);
eel.expose(toastInfo);

function reloadUrl() {
    location.reload();
}
function httpGet(theUrl, authorization = "") {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", theUrl, false); // false for synchronous request
    if (authorization != "") {
        xmlHttp.setRequestHeader("Authorization", authorization);
    }
    xmlHttp.send(null);
    return xmlHttp.responseText;
}
function getValue(cssSelector) {
    return $(cssSelector).val();
}
function getText(cssSelector) {
    return $(cssSelector).text();
}
function getTextSelect(cssSelector) {
    return $(cssSelector + " option:selected").text();
}
function getCheckboxChecked(cssSelector) {
    return $(cssSelector).is(":checked");
}

function setCheckboxCssSelector(cssSelector, check) {
    $(cssSelector).prop("checked", check);
}

function setValueCssSelector(cssSelector, html) {
    $(cssSelector).val(html);
}
function setSelectByText(cssSelector, text) {
    $(cssSelector)
        .find('option[text="' + text + '"]')
        .val();
}
function httpGetJson(theUrl, authorization = "") {
    var html = httpGet(theUrl, authorization);
    return JSON.parse(html);
}
function httpPost(theUrl, data, authorization = "") {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", theUrl, true);
    if (authorization != "") {
        xhr.setRequestHeader("Authorization", authorization);
    }
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.send(JSON.stringify(data));
    return xhr.responseText;
}
function httpPostReturnJson(theUrl, data, authorization = "") {
    var html = httpPost(theUrl, data, authorization);
    console.log("_______" + html);
    return JSON.parse(html);
}
function CopyTextareaToClipboard(idtextarea) {
    let textarea = document.getElementById(idtextarea);
    textarea.select();
    document.execCommand("copy");
    toastr.success("Sao chép thành công");
}

function Regex(html, regex) {
    var myArray = regex.exec(html);
    return myArray;
}

function Contains(html, str) {
    var n = html.indexOf(str);
    if (n >= 0) {
        return true;
    }
    return false;
}

function escapeRegExp(str) {
    return str.replace(/([.*+?^=!:${}()|\[\]\/\\])/g, "\\$1");
}

function replaceAll(str, find, replace) {
    return str.replace(new RegExp(escapeRegExp(find), "g"), replace);
}

function CheckLogin() {
    if (Contains(window.location.pathname, "/post/")) {
        return;
    }
    $.ajax({
        url: "/account/info",
        type: "get",
        dataType: "text",
        success: function (result) {
            const obj = JSON.parse(result);
            var user = obj.user;
            if (
                window.location.pathname == "/login.html" ||
                window.location.pathname == "/signup.html"
            ) {
                if (user != "") {
                    window.location.href = "/index.html";
                }
            } else {
                if (user === "") {
                    window.location.href = "/login.html";
                }
            }
        },
    });
}
// Implementation in ES6
function pagination(c, m) {
    var current = c,
        last = m,
        delta = 2,
        left = current - delta,
        right = current + delta + 1,
        range = [],
        rangeWithDots = [],
        l;

    for (let i = 1; i <= last; i++) {
        if (i == 1 || i == last || (i >= left && i < right)) {
            range.push(i);
        }
    }

    for (let i of range) {
        if (l) {
            if (i - l === 2) {
                rangeWithDots.push(l + 1);
            } else if (i - l !== 1) {
                rangeWithDots.push("...");
            }
        }
        rangeWithDots.push(i);
        l = i;
    }

    return rangeWithDots;
}
function editClassActive() {
    var el = $("ul.yoo-sidebar-nav-list.yoo-mp0 > li");
    var url = window.location.pathname;
    if (url == "/") {
        url = "/index.html";
    }
    for (i = 0; i < el.length; i++) {
        var element = el[i];
        var outerHTML = element.outerHTML;
        var z1 = outerHTML.includes(url);
        if (z1 === true) {
            // if (url == "/index.html") {
            $(
                "ul.yoo-sidebar-nav-list.yoo-mp0 > li:nth-child(" +
                    (i + 1) +
                    ")"
            ).attr("class", "active");
            // } else {
            // $(
            //   "ul.yoo-sidebar-nav-list.yoo-mp0 > li:nth-child(" + (i + 1) + ")"
            // ).attr("style", "color: #007bff");
            // }
        }
    }
}
function getTime() {
    var currentdate = new Date();
    var datetime =
        currentdate.getDate() +
        "/" +
        (currentdate.getMonth() + 1) +
        "/" +
        currentdate.getFullYear() +
        " - " +
        currentdate.getHours() +
        ":" +
        currentdate.getMinutes() +
        ":" +
        currentdate.getSeconds();
    return datetime;
}
function splitLines(subject) {
    var result = subject.split(/\r?\n/);
    return result;
}
function downloadFile(filename, text) {
    var element = document.createElement("a");
    element.setAttribute(
        "href",
        "data:text/plain;charset=utf-8," + encodeURIComponent(text)
    );
    element.setAttribute("download", filename);

    element.style.display = "none";
    document.body.appendChild(element);

    element.click();

    document.body.removeChild(element);
}
function downloadFileCu(filename, content) {
    let csvContent = "data:text;charset=utf-8," + content;
    var encodedUri = encodeURI(csvContent);
    var link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", filename);
    document.body.appendChild(link);
    link.click();
}
function getSelectedCombo(id) {
    var e = document.getElementById(id);
    var strUser = e.options[e.selectedIndex].text;
    return strUser;
}
function openDataNewTab(result) {
    result = result.replace("\n", "<br>");
    result = result.replace("\r", "<br>");
    var myWindow = window.open("", "");
    myWindow.document.write(result);
}
function Sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
}
function sleep(ms) {
    return new Promise((r) => setTimeout(r, ms));
}
includeHTML();
// CheckLogin();
editClassActive();

function showDialog(options = {}) {
    return new Promise(function (resolve, reject) {
        var overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100%";
        overlay.style.height = "100%";
        overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        overlay.style.display = "flex";
        overlay.style.justifyContent = "center";
        overlay.style.alignItems = "center";

        var container = document.createElement("div");
        container.style.backgroundColor = "white";
        container.style.borderRadius = "5px";
        container.style.padding = "20px";
        container.style.textAlign = "center";

        var title = document.createElement("h3");
        title.innerText = options.title || "Please enter your name";

        var input = document.createElement("input");
        input.type = "text";
        input.id = "name-input";
        input.value = options.value || "";
        input.style.display = "block";
        input.style.marginBottom = "10px";
        input.style.width = "100%";
        input.style.padding = "5px";
        input.style.border = "1px solid #ccc";
        input.style.borderRadius = "3px";
        input.style.boxSizing = "border-box";
        input.style.fontSize = "16px";

        var submitButton = document.createElement("button");
        submitButton.innerText = options.submitText || "OK";
        submitButton.style.backgroundColor = "#4CAF50";
        submitButton.style.color = "white";
        submitButton.style.padding = "10px";
        submitButton.style.border = "none";
        submitButton.style.borderRadius = "3px";
        submitButton.style.fontSize = "16px";
        submitButton.style.cursor = "pointer";
        submitButton.style.marginRight = "30px";
        submitButton.style.width = "100px"; // Đặt độ rộng của nút OK là 100px

        submitButton.addEventListener("click", function () {
            var name = document.getElementById("name-input").value;
            resolve(name);
            overlay.parentNode.removeChild(overlay);
            // overlay.style.display = "none";
        });

        var cancelButton = document.createElement("button");
        cancelButton.innerText = options.cancelText || "Cancel";
        cancelButton.style.backgroundColor = "#ccc";
        cancelButton.style.color = "white";
        cancelButton.style.padding = "10px";
        cancelButton.style.border = "none";
        cancelButton.style.borderRadius = "3px";
        cancelButton.style.fontSize = "16px";
        cancelButton.style.cursor = "pointer";
        cancelButton.style.width = "100px"; // Đặt độ rộng của nút OK là 100px

        cancelButton.addEventListener("click", function () {
            // reject(new Error("Cancelled"));
            resolve("");
            overlay.parentNode.removeChild(overlay);
            // overlay.style.display = "none";
        });

        container.appendChild(title);
        container.appendChild(input);
        container.appendChild(submitButton);
        container.appendChild(cancelButton);

        overlay.appendChild(container);

        document.body.appendChild(overlay);
    });
}
function showUpdate(options = {}) {
    return new Promise(function (resolve, reject) {
        var overlay = document.createElement("div");
        overlay.style.position = "fixed";
        overlay.style.top = "0";
        overlay.style.left = "0";
        overlay.style.width = "100%";
        overlay.style.height = "100%";
        overlay.style.backgroundColor = "rgba(0, 0, 0, 0.5)";
        overlay.style.display = "flex";
        overlay.style.justifyContent = "center";
        overlay.style.alignItems = "center";

        var container = document.createElement("div");
        container.style.backgroundColor = "white";
        container.style.borderRadius = "5px";
        container.style.padding = "20px";
        container.style.textAlign = "center";

        var title = document.createElement("h3");
        title.id = "updateStatus";
        title.innerText = options.title || "Please enter your name";

        const progressContainer = document.createElement("div");
        progressContainer.classList.add("w3-border");
        progressContainer.id = "progresss";
        progressContainer.style.visibility = "hidden";

        const progressBarContainer = document.createElement("div");
        progressBarContainer.id = "progress";
        progressBarContainer.classList.add(
            "w3-container",
            "w3-padding",
            "w3-blue"
        );
        progressBarContainer.style.width = "0%";
        progressBarContainer.style.visibility = "hidden";

        const progressValueContainer = document.createElement("div");
        progressValueContainer.id = "progressValue";
        progressValueContainer.classList.add("w3-center");
        progressValueContainer.style.visibility = "hidden";
        progressValueContainer.textContent = "0%";

        progressBarContainer.appendChild(progressValueContainer);
        progressContainer.appendChild(progressBarContainer);

        var submitButton = document.createElement("button");
        submitButton.innerText = options.submitText || "OK";
        submitButton.style.backgroundColor = "#4CAF50";
        submitButton.style.color = "white";
        submitButton.style.padding = "10px";
        submitButton.style.border = "none";
        submitButton.style.borderRadius = "3px";
        submitButton.style.fontSize = "16px";
        submitButton.style.cursor = "pointer";
        submitButton.style.marginTop = "30px";
        submitButton.style.marginRight = "30px";
        submitButton.style.width = "100px"; // Đặt độ rộng của nút OK là 100px

        submitButton.addEventListener("click", function () {
            overlay.parentNode.removeChild(overlay);
            // overlay.style.display = "none";
        });

        container.appendChild(title);
        container.appendChild(progressContainer);

        container.appendChild(submitButton);

        overlay.appendChild(container);

        document.body.appendChild(overlay);
    });
}
// Sử dụng hàm showDialog
function addRowTable(selectorTable, listColumnValues, id) {
    var table = $(selectorTable);
    if (table.find("#" + id).length > 0) {
        return;
    }

    // Tạo hàng mới với các ô
    var newRow = $("<tr>").attr("id", id);
    for (var i = 0; i < listColumnValues.length; i++) {
        var col1 = $("<td>").text(listColumnValues[i]);
        newRow.append(col1);
    }

    // Thêm hàng mới vào cuối bảng
    table.append(newRow);
}

// eel.getTitle()(function (callback) {
//     // console.log(callback);
//     document.title = callback;
// });
