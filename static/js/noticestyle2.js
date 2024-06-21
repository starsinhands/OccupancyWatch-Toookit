document.addEventListener("DOMContentLoaded", function () {
    // 当页面加载完成时显示提示窗口
    var overlay = document.getElementById("overlay");
    overlay.style.display = "flex";
    // 获取 Confirm 按钮并添加点击事件处理程序
    var confirmButton = document.getElementById("confirmButton");
    confirmButton.addEventListener("click", function () {
        var overlay = document.getElementById("overlay");
        overlay.style.animation = "fadeOutDown 0.5s ease-out forwards";
        setTimeout(function() {overlay.style.display = "none";}, 500);
    });
});