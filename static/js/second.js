//var occupantsInput;
document.addEventListener("DOMContentLoaded", function () {
    // 当页面加载完成时显示提示窗口
    var overlay = document.getElementById("overlay");
    overlay.style.display = "flex";
    // 获取 Confirm 按钮并添加点击事件处理程序
    document.getElementById("confirmButton").addEventListener("click", function () {
        // 获取输入框的值
        var occupantsInput = document.getElementById("occupantsInput").value;
        // 触发自定义事件，传递数据
        var event = new CustomEvent('occupantsUpdated', { detail: occupantsInput });
        document.dispatchEvent(event);
        //document.querySelector('.con').innerHTML+='Number of occupants: '+occupantsInput;
        //localStorage.setItem('occupantsInputValue', occupantsInput);// 将值存储到 localStorage
        //document.body.setAttribute('occupants-num', occupantsInput);// 将值存储在 body 的自定义属性中
        overlay.style.animation = "fadeOutDown 0.5s ease-out forwards";
        setTimeout(function() {overlay.style.display = "none";}, 500);
    });
});
